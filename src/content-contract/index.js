/**
 * Leitor do acervo `content/` — o único ponto da aplicação que conhece o
 * formato do dado (ADR-0007 §5).
 *
 * RESTRIÇÃO DURA (ADR-0003, independência do contrato de dados): este diretório
 * não importa nada do gerador de site — só `node:*`. Trocar de gerador tem de
 * custar reescrever `src/pages`, `src/layouts` e `src/components`, nunca o
 * acervo nem este módulo.
 *
 * O teste do ADR-0007 é um `grep` pelo nome do gerador neste diretório, e ele
 * tem de sair **vazio** — por isso o nome não aparece aqui, nem em comentário.
 * O CI executa esse `grep` (`.github/workflows/ai-surface-audit.yml`).
 *
 * Também não usa o mecanismo de coleções de conteúdo do gerador: coleções
 * pediriam frontmatter no formato da ferramenta, e os metadados do acervo vivem
 * em `meta.json` (ADR-0001).
 *
 * Divisão de responsabilidade com o validador (`scripts/validate-content.sh`,
 * TCK-0014): o validador é o **portão** normativo do RF-18 e roda antes da
 * build (script `prebuild`); este módulo é a **rede de segurança** — encontrou
 * chave ausente, ele derruba a build em vez de emitir página incompleta.
 */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { dirname, join, posix, resolve, sep } from 'node:path';

import { LANGUAGES, isLanguage, urlSegmentOf } from './languages.js';

export { LANGUAGES, isLanguage, urlSegmentOf, languageOfUrlSegment, urlSegments } from './languages.js';

/** Falha do contrato de carga: sempre interrompe a build, nunca degrada em silêncio. */
export class ContentContractError extends Error {
  constructor(message) {
    super(`[content-contract] ${message}`);
    this.name = 'ContentContractError';
  }
}

function fail(message) {
  throw new ContentContractError(message);
}

function toPosix(relativePath) {
  return relativePath.split(sep).join(posix.sep);
}

function readJsonFile(file, what) {
  let raw;
  try {
    raw = readFileSync(file, 'utf8');
  } catch (cause) {
    fail(`${what}: não foi possível ler ${file} — ${cause.message}`);
  }
  try {
    return JSON.parse(raw);
  } catch (cause) {
    fail(`${what}: JSON inválido em ${file} — ${cause.message}`);
  }
  return undefined;
}

function isDirectory(path) {
  try {
    return statSync(path).isDirectory();
  } catch {
    return false;
  }
}

function fileExists(path) {
  try {
    return statSync(path).isFile();
  } catch {
    return false;
  }
}

/**
 * Raiz do acervo, encontrada subindo a partir do diretório de trabalho até o
 * primeiro diretório que tenha `package.json` **e** `content/`.
 *
 * Por que não `import.meta.url`: o empacotador do gerador de site move este
 * módulo para dentro do diretório de build, e a URL do módulo passa a apontar
 * para o pacote, não para o código-fonte — o acervo "somem" sem que nada no
 * contrato tenha mudado. Procurar a raiz pelo marcador do repositório não
 * depende de onde o módulo foi empacotado, o que é justamente a independência
 * que o ADR-0003 exige.
 *
 * Não há variável de ambiente para trocar a raiz: um leitor que aponte para
 * lugar diferente do que o portão de validação inspecionou transforma o portão
 * em enfeite.
 */
function findContentRoot() {
  let directory = resolve(process.cwd());
  for (;;) {
    const candidate = join(directory, 'content');
    if (fileExists(join(directory, 'package.json')) && isDirectory(candidate)) {
      return candidate;
    }
    const parent = dirname(directory);
    if (parent === directory) break;
    directory = parent;
  }
  fail(
    `acervo não encontrado: nenhum diretório entre '${process.cwd()}' e a raiz do sistema ` +
      `tem 'package.json' e 'content/' ao mesmo tempo`,
  );
  return undefined;
}

let cachedContentRoot;

/**
 * Raiz do acervo, calculada **na primeira chamada** e memorizada.
 *
 * Avaliação preguiçosa de propósito (S4 do REJECT [006]): se fosse constante de
 * módulo, importar este arquivo com o `cwd` fora do repositório já lançaria — e
 * o parâmetro `root` de `listNodeIds`/`loadNode`/`loadAllNodes`, que existe para
 * apontar outro acervo, ficaria inutilizável antes de ser usado.
 */
export function contentRoot() {
  if (cachedContentRoot === undefined) {
    cachedContentRoot = findContentRoot();
  }
  return cachedContentRoot;
}

/**
 * Ids de todos os nós do acervo, em ordem estável.
 * Nó = diretório que contém `meta.json` (AGENTS.md §3). A varredura é recursiva:
 * um tópico pode ter subtópicos, e ambos são nós.
 */
export function listNodeIds(root = contentRoot()) {
  const found = [];

  const walk = (directory, relative) => {
    if (fileExists(join(directory, 'meta.json'))) {
      found.push(toPosix(relative));
    }
    for (const entry of readdirSync(directory, { withFileTypes: true }).sort((a, b) =>
      a.name.localeCompare(b.name, 'en'),
    )) {
      if (!entry.isDirectory() || entry.name.startsWith('.')) continue;
      walk(join(directory, entry.name), relative === '' ? entry.name : join(relative, entry.name));
    }
  };

  if (!isDirectory(root)) {
    fail(`acervo não encontrado em ${root}`);
  }
  walk(root, '');
  return found;
}

function requireField(meta, field, nodeId) {
  if (!(field in meta)) {
    fail(`meta.json do nó '${nodeId}' sem o campo obrigatório '${field}'`);
  }
  return meta[field];
}

function requireLocalized(value, field, nodeId, languages) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    fail(`campo localizado '${field}' do nó '${nodeId}' não é um objeto {${LANGUAGES.join(', ')}}`);
  }
  for (const language of languages) {
    const text = value[language];
    if (typeof text !== 'string' || text.trim() === '') {
      fail(`campo localizado '${field}' do nó '${nodeId}' sem texto em '${language}'`);
    }
  }
  return value;
}

/**
 * Carrega um nó pelo id (o caminho da taxonomia, ex.:
 * `high-school/algebra/quadratic-equations`).
 *
 * Devolve, sem interpretar: metadados de `meta.json`, o Markdown **bruto** de
 * `theory.<lang>.md` e os itens de `exercises.json`. Transformar Markdown em
 * HTML é apresentação, não contrato (ADR-0007 §5).
 */
export function loadNode(nodeId, root = contentRoot()) {
  const directory = join(root, ...nodeId.split(posix.sep));
  const metaFile = join(directory, 'meta.json');

  if (!fileExists(metaFile)) {
    fail(`nó '${nodeId}' sem meta.json — sem ele não há identidade nem idioma declarado`);
  }

  const meta = readJsonFile(metaFile, `nó '${nodeId}'`);
  if (meta === null || typeof meta !== 'object' || Array.isArray(meta)) {
    fail(`meta.json do nó '${nodeId}' não é um objeto`);
  }

  const declaredId = requireField(meta, 'id', nodeId);
  if (declaredId !== nodeId) {
    fail(
      `meta.json.id é '${declaredId}' mas o nó está em '${nodeId}' — o caminho da taxonomia ` +
        `é a URL pública (RF-17), não pode divergir`,
    );
  }

  const declaredLanguages = requireField(meta, 'languages', nodeId);
  if (!Array.isArray(declaredLanguages) || declaredLanguages.length === 0) {
    fail(`meta.json do nó '${nodeId}': 'languages' deve ser uma lista não vazia`);
  }
  for (const language of declaredLanguages) {
    if (!isLanguage(language)) {
      fail(`meta.json do nó '${nodeId}': idioma fora do contrato em 'languages': ${JSON.stringify(language)}`);
    }
  }

  // PARIDADE BILÍNGUE, NO CAMINHO DE PUBLICAÇÃO (B1 do REJECT [006]).
  // `ADR-0002` e `AGENTS.md` §2b proíbem publicar conteúdo monolíngue, e o
  // `ADR-0006` exige que nó sem paridade fique fora das rotas publicadas. Pular
  // o nó em silêncio seria o "fallback silencioso" que a mesma regra proíbe:
  // o acervo continuaria com um nó que ninguém vê e nada acusa. Então é falha
  // alta — a build cai e a rota monolíngue não chega a existir.
  const missingLanguages = LANGUAGES.filter((language) => !declaredLanguages.includes(language));
  if (missingLanguages.length > 0) {
    fail(
      `nó '${nodeId}' declara apenas [${declaredLanguages.join(', ')}] em 'languages' — ` +
        `falta ${missingLanguages.join(', ')}. Paridade bilíngue é obrigatória e não há ` +
        `fallback (ADR-0002, AGENTS.md §2b); nó sem paridade não pode virar rota publicada ` +
        `(ADR-0006). Complete a tradução ou tire o nó do acervo.`,
    );
  }
  // A partir daqui, o nó tem os dois idiomas do contrato. A ordem de
  // apresentação vem do contrato, não da ordem em que o nó declarou.
  const languages = [...LANGUAGES];

  const status = requireField(meta, 'status', nodeId);
  if (typeof status !== 'string' || status.trim() === '') {
    fail(`meta.json do nó '${nodeId}': 'status' deve ser texto não vazio`);
  }

  // `title` e `summary` são os dois campos localizados que a página usa; o
  // validador do RF-18 exige os dois, e aqui eles são exigidos nos DOIS idiomas.
  requireLocalized(requireField(meta, 'title', nodeId), 'title', nodeId, languages);
  requireLocalized(requireField(meta, 'summary', nodeId), 'summary', nodeId, languages);

  const theory = {};
  for (const language of languages) {
    const theoryFile = join(directory, `theory.${language}.md`);
    if (!fileExists(theoryFile)) {
      fail(`nó '${nodeId}' declara o idioma '${language}' mas não tem theory.${language}.md`);
    }
    try {
      theory[language] = readFileSync(theoryFile, 'utf8');
    } catch (cause) {
      fail(`nó '${nodeId}': não foi possível ler theory.${language}.md — ${cause.message}`);
    }
  }

  let exercises = [];
  const exercisesFile = join(directory, 'exercises.json');
  if (fileExists(exercisesFile)) {
    const payload = readJsonFile(exercisesFile, `nó '${nodeId}'`);
    if (payload === null || typeof payload !== 'object' || Array.isArray(payload)) {
      fail(`exercises.json do nó '${nodeId}' não é um objeto`);
    }
    if (!Array.isArray(payload.items)) {
      fail(`exercises.json do nó '${nodeId}' sem a lista 'items'`);
    }
    exercises = payload.items;
  }

  return Object.freeze({
    id: nodeId,
    directory,
    meta,
    status,
    languages,
    theory,
    exercises,
  });
}

/** Todos os nós do acervo, carregados. Uma chamada por build. */
export function loadAllNodes(root = contentRoot()) {
  return listNodeIds(root).map((nodeId) => loadNode(nodeId, root));
}

/**
 * Rotas de um nó: uma por idioma do contrato — `loadNode` já garantiu que o nó
 * tem os dois —, com o caminho da taxonomia intacto.
 * `/pt-br/high-school/algebra/quadratic-equations` — sem tradução, sem
 * normalização, sem maiúscula (RNF-5, L-003).
 */
export function routesOf(node) {
  return node.languages.map((language) => ({
    language,
    urlSegment: urlSegmentOf(language),
    path: `/${urlSegmentOf(language)}/${node.id}`,
  }));
}
