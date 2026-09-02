# rodrigoroque.dev

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-db61a2?logo=githubsponsors&logoColor=white&style=for-the-badge)](https://github.com/sponsors/roquerodrigo)

Portfólio e currículo de **Rodrigo Roque** — Engenheiro de Software Sênior / Especialista.

Publicado via **GitHub Pages** em [rodrigoroque.dev](https://rodrigoroque.dev).

## Estrutura

```
.
├── cv/                       # Currículo em LaTeX (fonte da verdade)
│   ├── resume.cls            # Classe minimalista ATS-friendly (Fira Sans)
│   ├── cv-pt.tex             # Conteúdo em português
│   └── cv-en.tex             # Conteúdo em inglês
├── site/                     # Portfólio estático servido no Pages
│   ├── index.html            # single-page: hero, sobre, experiência, skills, contato
│   ├── styles.css            # design "telemetria/blueprint" · claro+escuro
│   ├── app.js                # tema, count-up, reveal on scroll, nav ativa
│   ├── favicon.svg           # monograma "RR"
│   └── assets/fonts/         # fontes self-hosted (subset · woff2)
├── .github/workflows/        # CI: compila o LaTeX e faz deploy no Pages
├── Makefile                  # Build local
└── CNAME                     # Domínio (rodrigoroque.dev)
```

## Build local

Requer o [Tectonic](https://tectonic-typesetting.github.io/) (engine LaTeX):

```bash
brew install tectonic      # macOS

make            # gera cv/cv-pt.pdf e cv/cv-en.pdf
make site       # gera os PDFs e monta o site em _site/
make serve      # serve _site/ em http://localhost:8000
make clean      # remove artefatos de build
```

## Deploy

Todo push na branch `main` dispara o workflow **Build & Deploy**, que:

1. instala o Tectonic;
2. compila `cv-pt.tex` e `cv-en.tex` em PDF;
3. monta `_site/` (landing + PDFs + `CNAME`);
4. publica no GitHub Pages.

> No repositório, em **Settings → Pages**, a origem (**Source**) deve estar como
> **GitHub Actions**.

Os PDFs ficam disponíveis em:

- `https://rodrigoroque.dev/rodrigo-roque-cv-pt.pdf`
- `https://rodrigoroque.dev/rodrigo-roque-cv-en.pdf`

## Apoie o projeto

Este projeto é desenvolvido e mantido em tempo pessoal. Se for útil para você, considere [patrocinar o trabalho](https://github.com/sponsors/roquerodrigo) — é o que mantém o desenvolvimento, os testes e as publicações acontecendo.
