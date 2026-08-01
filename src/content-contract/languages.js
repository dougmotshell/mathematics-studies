/**
 * Mapa único idioma <-> segmento de URL.
 *
 * Há duas grafias no projeto, de propósito (ADR-0007 §7):
 *   - `pt-BR` / `en-US` — identificador do dado: nome de arquivo
 *     (`theory.pt-BR.md`), chave de campo localizado e atributo `lang` do
 *     documento HTML;
 *   - `pt-br` / `en-us` — grafia da URL pública, minúscula porque host de
 *     arquivos estáticos é sensível a maiúsculas e canonicalizar caixa mista
 *     exigiria regra de redirect do fornecedor.
 *
 * Este arquivo é o único lugar do repositório que conhece as duas ao mesmo
 * tempo. Duplicar o mapa é o defeito que ele existe para evitar.
 *
 * ESM puro: nenhuma dependência, nem do gerador de site.
 */

/** Idiomas do contrato, em ordem de apresentação. Paridade é obrigatória (ADR-0002). */
export const LANGUAGES = Object.freeze(['pt-BR', 'en-US']);

const URL_SEGMENT_BY_LANGUAGE = Object.freeze({
  'pt-BR': 'pt-br',
  'en-US': 'en-us',
});

const LANGUAGE_BY_URL_SEGMENT = Object.freeze(
  Object.fromEntries(Object.entries(URL_SEGMENT_BY_LANGUAGE).map(([lang, seg]) => [seg, lang])),
);

/** `true` se o valor é um identificador de idioma do contrato (`pt-BR`, `en-US`). */
export function isLanguage(value) {
  return LANGUAGES.includes(value);
}

/** `pt-BR` -> `pt-br`. Lança se o idioma não pertence ao contrato. */
export function urlSegmentOf(language) {
  const segment = URL_SEGMENT_BY_LANGUAGE[language];
  if (segment === undefined) {
    throw new Error(
      `[content-contract] idioma fora do contrato: ${JSON.stringify(language)} — ` +
        `esperado um de ${LANGUAGES.join(', ')}`,
    );
  }
  return segment;
}

/** `pt-br` -> `pt-BR`. Lança se o segmento não pertence ao contrato. */
export function languageOfUrlSegment(segment) {
  const language = LANGUAGE_BY_URL_SEGMENT[segment];
  if (language === undefined) {
    throw new Error(
      `[content-contract] segmento de URL fora do contrato: ${JSON.stringify(segment)} — ` +
        `esperado um de ${Object.values(URL_SEGMENT_BY_LANGUAGE).join(', ')}`,
    );
  }
  return language;
}

/** Segmentos de URL de idioma, na ordem de `LANGUAGES`. */
export function urlSegments() {
  return LANGUAGES.map(urlSegmentOf);
}
