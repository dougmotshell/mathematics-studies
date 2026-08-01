// Configuração do gerador de site estático (ADR-0003 aceito, ADR-0007 §1).
//
// Deliberadamente mínima: tudo que não está aqui é decisão de ticket futuro
// (biblioteca de UI, renderização de Markdown/KaTeX, camada offline, testes).
import { defineConfig } from 'astro/config';

export default defineConfig({
  // URL pública atual. É usada apenas para gerar URLs absolutas; trocar de host
  // custa reescrever esta linha (ADR-0003: o artefato é um diretório estático).
  site: 'https://mathematics-studies.vercel.app',

  // `directory` emite dist/<rota>/index.html — a convenção que qualquer host de
  // arquivos estáticos serve sem configuração própria. É o que mantém a URL
  // portátil (ADR-0007 §7).
  build: {
    format: 'directory',
  },

  // Nenhuma barra de ferramentas injetada em desenvolvimento: o produto não
  // carrega script que o repositório não escreveu (RNF-7).
  devToolbar: {
    enabled: false,
  },
});
