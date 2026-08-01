#!/usr/bin/env python3
"""
audit-content.py — Auditoria determinística do acervo em content/.

Verifica o que uma máquina consegue verificar sozinha; a auditoria didática e de
rigor matemático é feita por /content-audit, math-reviewer e i18n-steward.

Checagens:
  * estrutura do nó (arquivos obrigatórios presentes)
  * meta.json: campos, tipos, id == caminho, stage/area válidos, difficulty 1..5
  * bilinguismo pt-BR/en-US (arquivos e campos localizados)
  * status "published" só com teoria + exercícios + referências completos
  * exercises.json/assessments.json contra o schema (docs/content/exercise-schema.md)
  * grafo de pré-requisitos: alvos existentes, sem ciclo, dificuldade não crescente
  * references.json: autor, ano, url, idioma e licença presentes
  * trilhas em content/paths/*.json apontando para nós existentes

Uso:
  python3 scripts/audit-content.py [caminho-relativo-dentro-de-content]
Saída: linhas "ERRO"/"AVISO" e um resumo. Código 1 se houver erro.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT = REPO_ROOT / "content"
PATHS_DIR = CONTENT / "paths"

LANGS = ("pt-BR", "en-US")

STAGES = {
    "early-childhood", "elementary", "middle-school", "high-school",
    "undergraduate", "graduate", "research",
}
AREAS = {
    "arithmetic", "algebra", "geometry", "trigonometry", "precalculus", "calculus",
    "linear-algebra", "analysis", "abstract-algebra", "topology", "probability",
    "statistics", "discrete-math", "number-theory", "logic-foundations",
    "differential-equations", "numerical-methods", "optimization",
}
STATUSES = {"draft", "review", "published"}
ITEM_TYPES = {
    "multiple-choice", "true-false", "numeric", "short-answer",
    "ordering", "matching", "step-by-step", "proof",
}

errors: list[str] = []
warnings: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"ERRO\t{where}\t{msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"AVISO\t{where}\t{msg}")


def load_json(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        err(str(path.relative_to(REPO_ROOT)), f"JSON inválido: {exc}")
        return None


def is_localized(value: object) -> bool:
    return (
        isinstance(value, dict)
        and all(lang in value for lang in LANGS)
        and all(isinstance(value[lang], str) and value[lang].strip() for lang in LANGS)
    )


def check_localized(where: str, field: str, value: object) -> None:
    if not isinstance(value, dict):
        err(where, f"campo '{field}' deve ser objeto localizado {{pt-BR, en-US}}")
        return
    for lang in LANGS:
        if lang not in value or not str(value.get(lang, "")).strip():
            err(where, f"campo '{field}' sem conteúdo em {lang}")


def find_nodes(scope: Path) -> list[Path]:
    """Nó = diretório contendo meta.json."""
    return sorted(p.parent for p in scope.rglob("meta.json"))


# --------------------------------------------------------------------------- #


def check_meta(node: Path, rel: str) -> dict:
    meta = load_json(node / "meta.json")
    if meta is None:
        err(rel, "meta.json ausente ou ilegível")
        return {}
    if not isinstance(meta, dict):
        err(rel, "meta.json deve ser um objeto")
        return {}

    for field in ("id", "stage", "area", "title", "summary", "difficulty", "status", "languages"):
        if field not in meta:
            err(rel, f"meta.json sem o campo obrigatório '{field}'")

    if meta.get("id") != rel:
        err(rel, f"meta.json.id ('{meta.get('id')}') diferente do caminho do nó ('{rel}')")

    stage = meta.get("stage")
    if stage not in STAGES:
        err(rel, f"stage inválido: '{stage}' (ver docs/content/taxonomy.md)")
    elif not rel.startswith(f"{stage}/"):
        err(rel, f"stage '{stage}' não corresponde à pasta do nó")

    area = meta.get("area")
    if area not in AREAS:
        err(rel, f"area inválida: '{area}' (ver docs/content/taxonomy.md)")

    diff = meta.get("difficulty")
    if not isinstance(diff, int) or not 1 <= diff <= 5:
        err(rel, f"difficulty deve ser inteiro de 1 a 5 (encontrado: {diff!r})")

    status = meta.get("status")
    if status not in STATUSES:
        err(rel, f"status inválido: '{status}' (draft | review | published)")

    for field in ("title", "summary"):
        if field in meta:
            check_localized(rel, field, meta[field])

    langs = meta.get("languages")
    if not isinstance(langs, list) or set(langs) != set(LANGS):
        err(rel, f"languages deve ser exatamente {list(LANGS)} (encontrado: {langs!r})")

    for field in ("prerequisites", "tags", "skills"):
        if field in meta and not isinstance(meta[field], list):
            err(rel, f"campo '{field}' deve ser lista")

    if "updatedAt" not in meta:
        warn(rel, "meta.json sem 'updatedAt' (data absoluta AAAA-MM-DD)")

    return meta


def check_theory(node: Path, rel: str) -> bool:
    complete = True
    for lang in LANGS:
        f = node / f"theory.{lang}.md"
        if not f.exists():
            err(rel, f"theory.{lang}.md ausente (bilinguismo obrigatório — ADR-0002)")
            complete = False
        elif not f.read_text(encoding="utf-8").strip():
            err(rel, f"theory.{lang}.md vazio")
            complete = False
    return complete


def check_exercises(node: Path, rel: str, meta: dict, filename: str) -> bool:
    path = node / filename
    if not path.exists():
        return False
    data = load_json(path)
    if data is None:
        return False
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        err(f"{rel}/{filename}", "deve ser objeto com a lista 'items'")
        return False

    declared_skills = set(meta.get("skills") or [])
    seen_ids: set[str] = set()
    covered: set[str] = set()

    for idx, item in enumerate(data["items"]):
        where = f"{rel}/{filename}[{idx}]"
        if not isinstance(item, dict):
            err(where, "item deve ser objeto")
            continue

        item_id = item.get("id")
        if not item_id:
            err(where, "item sem 'id'")
        elif item_id in seen_ids:
            err(where, f"id duplicado: '{item_id}'")
        else:
            seen_ids.add(item_id)

        itype = item.get("type")
        if itype not in ITEM_TYPES:
            err(where, f"type inválido: '{itype}' (ver docs/content/exercise-schema.md)")

        diff = item.get("difficulty")
        if not isinstance(diff, int) or not 1 <= diff <= 5:
            err(where, f"difficulty deve ser inteiro de 1 a 5 (encontrado: {diff!r})")

        skills = item.get("skills")
        if not isinstance(skills, list) or not skills:
            err(where, "item sem 'skills' (pelo menos uma habilidade)")
        else:
            covered.update(skills)
            unknown = [s for s in skills if declared_skills and s not in declared_skills]
            if unknown:
                err(where, f"skills não declaradas em meta.json: {unknown}")

        if "stem" not in item:
            err(where, "item sem 'stem'")
        else:
            check_localized(where, "stem", item["stem"])

        if "solution" not in item:
            err(where, "item sem 'solution' (solução passo a passo)")
        else:
            check_localized(where, "solution", item["solution"])

        hints = item.get("hints")
        if not isinstance(hints, list) or len(hints) < 2:
            warn(where, "recomendado ao menos 2 dicas progressivas")
        elif not all(is_localized(h) for h in hints):
            err(where, "todas as dicas devem ser bilíngues {pt-BR, en-US}")

        if itype in ("multiple-choice", "true-false", "matching"):
            options = item.get("options")
            if not isinstance(options, list) or len(options) < 2:
                err(where, "item de escolha precisa de 'options' com ao menos 2 alternativas")
            else:
                correct = [o for o in options if isinstance(o, dict) and o.get("correct")]
                if len(correct) == 0:
                    err(where, "nenhuma alternativa marcada como correta")
                if itype == "multiple-choice" and len(correct) > 1:
                    err(where, f"{len(correct)} alternativas corretas em multiple-choice")
                for oi, opt in enumerate(options):
                    ow = f"{where}.options[{oi}]"
                    if not isinstance(opt, dict):
                        err(ow, "alternativa deve ser objeto")
                        continue
                    check_localized(ow, "text", opt.get("text"))
                    if not opt.get("correct"):
                        if "feedback" not in opt:
                            err(ow, "alternativa errada sem 'feedback' diagnóstico")
                        else:
                            check_localized(ow, "feedback", opt["feedback"])
        elif itype in ("numeric", "short-answer", "ordering"):
            if "answer" not in item:
                err(where, f"item do tipo '{itype}' sem 'answer'")
            if itype == "numeric" and "tolerance" not in item:
                warn(where, "item numeric sem 'tolerance' declarada")
        elif itype in ("proof", "step-by-step"):
            if "rubric" not in item:
                warn(where, f"item '{itype}' sem 'rubric' de avaliação")

        if meta.get("status") == "published" and not item.get("verified"):
            err(where, "gabarito sem 'verified' (verificação obrigatória — lição L-002)")

    missing = declared_skills - covered
    if declared_skills and missing and filename == "exercises.json":
        warn(f"{rel}/{filename}", f"skills declaradas sem exercício: {sorted(missing)}")

    return True


def check_references(node: Path, rel: str) -> bool:
    path = node / "references.json"
    if not path.exists():
        return False
    data = load_json(path)
    if data is None:
        return False
    items = data.get("items") if isinstance(data, dict) else data
    if not isinstance(items, list):
        err(f"{rel}/references.json", "deve ser lista de referências (ou objeto com 'items')")
        return False
    for idx, ref in enumerate(items):
        where = f"{rel}/references.json[{idx}]"
        if not isinstance(ref, dict):
            err(where, "referência deve ser objeto")
            continue
        for field in ("author", "year", "url", "language", "license"):
            if not str(ref.get(field, "")).strip():
                err(where, f"referência sem '{field}' (fonte gratuita com licença registrada)")
    return True


def check_prerequisites(metas: dict[str, dict]) -> None:
    for rel, meta in metas.items():
        for pre in meta.get("prerequisites") or []:
            if pre not in metas:
                err(rel, f"pré-requisito inexistente: '{pre}'")
                continue
            pre_diff = metas[pre].get("difficulty")
            cur_diff = meta.get("difficulty")
            if isinstance(pre_diff, int) and isinstance(cur_diff, int):
                if metas[pre].get("stage") == meta.get("stage") and pre_diff > cur_diff:
                    err(rel, f"pré-requisito '{pre}' tem dificuldade maior ({pre_diff} > {cur_diff})")

    # detecção de ciclo (DFS com marcação de estado)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {rel: WHITE for rel in metas}

    def visit(rel: str, stack: list[str]) -> None:
        color[rel] = GRAY
        for pre in metas[rel].get("prerequisites") or []:
            if pre not in metas:
                continue
            if color[pre] == GRAY:
                cycle = " → ".join(stack[stack.index(pre):] + [pre]) if pre in stack else f"{rel} → {pre}"
                err(rel, f"ciclo de pré-requisitos: {cycle}")
            elif color[pre] == WHITE:
                visit(pre, stack + [pre])
        color[rel] = BLACK

    for rel in metas:
        if color[rel] == WHITE:
            visit(rel, [rel])


def check_paths(metas: dict[str, dict]) -> None:
    if not PATHS_DIR.exists():
        return
    for path_file in sorted(PATHS_DIR.glob("*.json")):
        rel = str(path_file.relative_to(REPO_ROOT))
        data = load_json(path_file)
        if not isinstance(data, dict):
            err(rel, "descritor de trilha deve ser objeto")
            continue
        for field in ("id", "title", "goal", "modules"):
            if field not in data:
                err(rel, f"trilha sem o campo obrigatório '{field}'")
        for field in ("title", "goal"):
            if field in data:
                check_localized(rel, field, data[field])
        for mi, module in enumerate(data.get("modules") or []):
            for node_id in module.get("nodes") or []:
                if node_id not in metas:
                    err(rel, f"módulo {mi}: nó inexistente '{node_id}'")


# --------------------------------------------------------------------------- #


def main() -> int:
    if not CONTENT.exists():
        print("AVISO\tcontent/\tdiretório não existe — nada a auditar")
        return 0

    scope = CONTENT
    if len(sys.argv) > 1:
        candidate = (CONTENT / sys.argv[1]).resolve()
        if not candidate.exists():
            candidate = (REPO_ROOT / sys.argv[1]).resolve()
        if not candidate.exists():
            print(f"ERRO\t{sys.argv[1]}\tcaminho não encontrado", file=sys.stderr)
            return 1
        scope = candidate

    nodes = find_nodes(scope)
    if not nodes:
        print(f"AVISO\t{scope.relative_to(REPO_ROOT)}\tnenhum nó de conteúdo encontrado")
        print("\nResumo: 0 nós · 0 erros · 0 avisos")
        return 0

    # metas de TODO o acervo (necessário para validar pré-requisitos entre nós)
    all_metas: dict[str, dict] = {}
    for node in find_nodes(CONTENT):
        rel = str(node.relative_to(CONTENT))
        data = load_json(node / "meta.json")
        if isinstance(data, dict):
            all_metas[rel] = data

    for node in nodes:
        rel = str(node.relative_to(CONTENT))
        meta = check_meta(node, rel)
        theory_ok = check_theory(node, rel)
        exercises_ok = check_exercises(node, rel, meta, "exercises.json")
        if (node / "assessments.json").exists():
            check_exercises(node, rel, meta, "assessments.json")
        refs_ok = check_references(node, rel)

        if meta.get("status") == "published":
            if not theory_ok:
                err(rel, "status 'published' com teoria incompleta")
            if not exercises_ok:
                err(rel, "status 'published' sem exercises.json")
            if not refs_ok:
                err(rel, "status 'published' sem references.json")

    check_prerequisites(all_metas)
    check_paths(all_metas)

    for line in errors:
        print(line)
    for line in warnings:
        print(line)

    print(f"\nResumo: {len(nodes)} nós · {len(errors)} erros · {len(warnings)} avisos")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
