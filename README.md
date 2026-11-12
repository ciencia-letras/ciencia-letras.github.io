# ciencia-letras.github.io

**[English](#english)** · **[Português](#português)**

---

## English

Source of the Ciência e Letras Research & Innovation home page: **https://ciencia-letras.github.io** (English) and **https://ciencia-letras.github.io/pt/** (Portuguese).

The page is generated from the YAML files in [`data/`](data/). Every push to `main` rebuilds and publishes the site automatically (GitHub Actions).

### Adding content

You can edit the files directly on GitHub (pencil icon) — no local setup needed.

| To add… | Edit |
|---|---|
| A teaching resource used in class | [`data/resources.yml`](data/resources.yml) |
| An R&D artefact ready to share | [`data/artifacts.yml`](data/artifacts.yml) |
| A publication | [`data/publications.yml`](data/publications.yml) |
| A news item | [`data/news.yml`](data/news.yml) |
| A course | [`data/courses.yml`](data/courses.yml) |
| Interface text | [`data/site.yml`](data/site.yml) |

Each file has the fields and an example at the top. Rules:

- Every text has an English (`en`) and a Portuguese (`pt`) version — **English first**.
- The build fails, and the site is not updated, if a text is missing one language or a field has an invalid value. The error message in the Actions tab says which entry to fix.

### Building locally

```bash
pip install pyyaml jinja2
python build.py
python -m http.server 8765 --directory _site
```

---

## Português

Código da página de Investigação e Inovação do Ciência e Letras: **https://ciencia-letras.github.io** (inglês) e **https://ciencia-letras.github.io/pt/** (português).

A página é gerada a partir dos ficheiros YAML em [`data/`](data/). Cada alteração em `main` reconstrói e publica o site automaticamente (GitHub Actions).

### Acrescentar conteúdos

Pode editar os ficheiros diretamente no GitHub (ícone do lápis), sem instalar nada.

| Para acrescentar… | Editar |
|---|---|
| Um recurso pedagógico usado nas aulas | [`data/resources.yml`](data/resources.yml) |
| Um artefacto de I&D pronto a partilhar | [`data/artifacts.yml`](data/artifacts.yml) |
| Uma publicação | [`data/publications.yml`](data/publications.yml) |
| Uma notícia | [`data/news.yml`](data/news.yml) |
| Um curso | [`data/courses.yml`](data/courses.yml) |
| Textos da interface | [`data/site.yml`](data/site.yml) |

Cada ficheiro tem os campos e um exemplo no topo. Regras:

- Cada texto tem versão em inglês (`en`) e em português (`pt`) — **inglês primeiro**.
- Se faltar um dos idiomas ou um campo tiver um valor inválido, a construção falha e o site não é atualizado. A mensagem de erro no separador Actions indica a entrada a corrigir.

### Construir localmente

```bash
pip install pyyaml jinja2
python build.py
python -m http.server 8765 --directory _site
```
