#!/usr/bin/env python3
"""
empacotar.py — gerador de empacotamento portável dos prompts da trilha doc-sauro.

FONTE CANÔNICA ÚNICA:
    doc-sauro-btg/prompts/*.md   (exceto README.md — é a doc da cadeia, não um prompt)

ALVOS (GERADOS — nunca editados à mão):
    dist/.amazonq/prompts/<nome>.md          Amazon Q  — prompt on-demand (Markdown puro)
    dist/.github/prompts/<nome>.prompt.md    Copilot   — prompt file  (invocado /<nome>)
    dist/.kiro/steering/<nome>.md            Kiro      — steering inclusion: manual (#<nome>)

PRINCÍPIO (o que torna a paridade trivial e o drift impossível):
    o CORPO de cada alvo é BYTE-A-BYTE o prompt canônico. A ÚNICA adição é o
    frontmatter que cada ferramenta exige para invocação-manual. Tirar o
    frontmatter de qualquer alvo tem que devolver o canônico, caractere a caractere.

    Isso é o preço da portabilidade paga uma vez: o texto (princípio-norte,
    disciplina de citação, handoff) já vem embutido em cada prompt canônico; aqui
    só empacotamos, nunca reescrevemos.

USO:
    python3 empacotar.py            # (re)gera dist/ a partir de prompts/
    python3 empacotar.py --verify   # verifica paridade + frontmatter (não escreve nada)

Repetível: descobre os prompts por glob. Quando novos geradores da trilha
entrarem em prompts/, são empacotados sem tocar neste arquivo.
"""

from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path

# --- localização (este script vive em doc-sauro-btg/tools/) ---
ROOT = Path(__file__).resolve().parent.parent   # doc-sauro-btg/
PROMPTS_DIR = ROOT / "prompts"
DIST_DIR = ROOT / "dist"
EXCLUDE = {"README.md"}                          # não é prompt

# ---------------------------------------------------------------------------
# 1) Leitura do canônico + metadados derivados (nada é hardcoded fora do fonte)
# ---------------------------------------------------------------------------

def read_prompts():
    """[(nome, texto_canônico)] por prompt, em ordem estável (alfabética)."""
    out = []
    for p in sorted(PROMPTS_DIR.glob("*.md")):
        if p.name in EXCLUDE:
            continue
        out.append((p.stem, p.read_text(encoding="utf-8")))
    return out


_SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý])")


def derive_description(text):
    """Primeira frase do primeiro parágrafo de prosa — derivada do canônico (sem drift).

    Pula o H1 e a(s) blockquote(s) de intro; pega o primeiro parágrafo de prosa,
    corta na primeira fronteira de frase, remove marcação. Usada só onde a
    ferramenta tem campo de descrição (Copilot). Regerada a cada run.
    """
    para = []
    for line in text.splitlines():
        s = line.strip()
        if not para:
            if s == "" or s.startswith("#") or s.startswith(">"):
                continue
            para.append(s)
        else:
            if s == "" or s.startswith(("#", ">", "```", "-", "|", "*", "1.")):
                break
            para.append(s)
    paragraph = " ".join(para)
    first = _SENTENCE.split(paragraph)[0] if paragraph else ""
    return _strip_markdown(first)


def _strip_markdown(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)   # [txt](url) -> txt
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<!\*)\*(?!\*)", "", s)            # ênfase * simples
    s = re.sub(r"\s+", " ", s).strip()
    return s


def yaml_sq(s):
    """Escalar YAML entre aspas simples (estilo dos exemplos oficiais do Copilot)."""
    return "'" + s.replace("'", "''") + "'"


# ---------------------------------------------------------------------------
# 2) Alvos — cada um: (nome, texto, desc) -> (caminho relativo, conteúdo)
#    Frontmatter é a ÚNICA diferença entre alvo e canônico.
# ---------------------------------------------------------------------------

def build_amazonq(name, text, desc):
    # Amazon Q Developer — prompt on-demand. Markdown puro, SEM frontmatter.
    # (as .amazonq/rules/* são always-on e NÃO servem para invocável — ver README/dist)
    return f".amazonq/prompts/{name}.md", text


def build_copilot(name, text, desc):
    # GitHub Copilot — prompt file. `agent` (novo; `mode` foi depreciado) + `description`.
    fm = f"---\ndescription: {yaml_sq(desc)}\nagent: 'agent'\n---\n\n"
    return f".github/prompts/{name}.prompt.md", fm + text


def build_kiro(name, text, desc):
    # Kiro — steering com inclusion manual. Modo manual = SÓ a diretiva inclusion.
    fm = "---\ninclusion: manual\n---\n\n"
    return f".kiro/steering/{name}.md", fm + text


TARGETS = [build_amazonq, build_copilot, build_kiro]


# ---------------------------------------------------------------------------
# 3) Geração
# ---------------------------------------------------------------------------

def generate(base=DIST_DIR, quiet=False):
    if base.exists():
        shutil.rmtree(base)
    prompts = read_prompts()
    n = 0
    for name, text in prompts:
        desc = derive_description(text)
        for build in TARGETS:
            rel, contents = build(name, text, desc)
            dest = base / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(contents, encoding="utf-8")
            n += 1
    write_readme(base, prompts)
    if not quiet:
        rel_base = base if base.is_absolute() else base
        try:
            shown = rel_base.relative_to(ROOT.parent)
        except ValueError:
            shown = rel_base
        print(f"OK · {len(prompts)} prompts × {len(TARGETS)} alvos = {n} arquivos em {shown}/")
        for name, _ in prompts:
            print(f"     - {name}")
    return prompts


# ---------------------------------------------------------------------------
# 4) Verificação — paridade de conteúdo + frontmatter válido por convenção
# ---------------------------------------------------------------------------

def split_frontmatter(contents):
    """(corpo, {chave: valor}). Sem bloco `---` no topo => frontmatter vazio."""
    if not contents.startswith("---\n"):
        return contents, {}
    end = contents.index("\n---\n", 4)
    block = contents[4:end]
    body = contents[end + 5:]
    if body.startswith("\n"):
        body = body[1:]           # remove a linha em branco separadora que adicionamos
    fm = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = _unquote(v.strip())
    return body, fm


def _unquote(v):
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        inner = v[1:-1]
        return inner.replace("''", "'") if v[0] == "'" else inner
    return v


def _validate_frontmatter(rel, fm, body):
    """Regras por ferramenta. Retorna lista de problemas (vazia = ok)."""
    probs = []
    parts = Path(rel).parts
    tool = parts[0]
    if tool == ".amazonq":
        if fm:
            probs.append(f"{rel}: Amazon Q não deve ter frontmatter (achei {sorted(fm)})")
        if not body.lstrip().startswith("#"):
            probs.append(f"{rel}: corpo não começa com título Markdown")
    elif tool == ".github":
        if "description" not in fm or not fm["description"].strip():
            probs.append(f"{rel}: Copilot exige `description` não vazio")
        if "mode" in fm:
            probs.append(f"{rel}: `mode` está depreciado — use `agent`")
        if "agent" in fm and fm["agent"] not in {"ask", "agent", "plan"}:
            probs.append(f"{rel}: `agent` inválido: {fm['agent']!r}")
    elif tool == ".kiro":
        if fm.get("inclusion") != "manual":
            probs.append(f"{rel}: Kiro manual exige `inclusion: manual` (achei {fm!r})")
        extra = set(fm) - {"inclusion"}
        if extra:
            probs.append(f"{rel}: modo manual do Kiro não usa campos extras: {sorted(extra)}")
    else:
        probs.append(f"{rel}: alvo desconhecido")
    return probs


def _validate_canonical_prompt(name, text):
    """Invariantes arquiteturais mínimos de cada prompt standalone."""
    probs = []
    expected_title = f"# Prompt · `{name}`\n"
    if not text.startswith(expected_title):
        probs.append(f"prompts/{name}.md: título canônico esperado {expected_title.strip()!r}")
    required = {
        "marcador standalone": "**standalone**",
        "critério verificável": "## Critério de conclusão",
        "handoff explícito": "## Handoff",
    }
    for label, marker in required.items():
        if marker not in text:
            probs.append(f"prompts/{name}.md: falta {label} ({marker!r})")
    if not any(marker in text for marker in (
        "## Contrato de execução",
        "## Contrato e saída",
        "## Pré-condições",
    )):
        probs.append(f"prompts/{name}.md: falta contrato de execução ou pré-condições")
    if name.startswith("grill-") and f".arquitetura/gates/{name}" not in text:
        probs.append(f"prompts/{name}.md: gate não declara saída persistente")
    semantic_markers = {
        "bootstrap-contexto": ("ARC-###", "CON-###", "PERG-CTX-###", "Cobertura das lentes"),
        "mapear-estrutura": ("ENTRY-###", "FLUXO-<slug>", "PERG-CTX-###", ".arquitetura/grills/contexto.md"),
        "documentar-fluxo": ("PASSO-###", "ARESTA-###", "FRONTEIRA-###", "PERG-TEC-###", "Cobertura das lentes"),
        "grill-doc": ("CITACAO-NAO-SUSTENTA", "RISCO-OCULTO", "PERG-TEC-###"),
        "grill-mermaid": ("SETA-INVENTADA", "ARESTA-AUSENTE", "snapshot"),
        "revisar-arquitetura": (
            "OPORT-ARQ-###",
            "PERG-ARQ-###",
            "deletion test",
            "Top recommendation",
            "$TMPDIR",
            "Strong",
            "Worth exploring",
            "Speculative",
            ".arquitetura/revisoes/arquitetura.<escopo>.md",
            "Qual dessas oportunidades você quer explorar?",
        ),
        "contexto-produto": ("PER-###", "JOB-###", "TERMO-###", "REGRA-###"),
        "documentar-negocio": ("NEG-###", "PERG-NEG-###", "Cobertura das lentes"),
        "grill-negocio": ("INFERENCIA-PROMOVIDA", "PERG-NEG-###", "PERGUNTA-GENERICA"),
        "documentar-visao": ("VISAO-###", "PERG-VISAO-###", "Cobertura das lentes"),
        "grill-visao": ("UNIDADE-MISTURADA", "PERG-VISAO-###", "PERGUNTA-GENERICA"),
    }
    for marker in semantic_markers.get(name, ()):
        if marker not in text:
            probs.append(f"prompts/{name}.md: falta marcador semântico {marker!r}")
    dynamic_grill_paths = {
        "bootstrap-contexto": ".arquitetura/grills/contexto.md",
        "documentar-fluxo": ".arquitetura/grills/tecnico.<slug>.md",
        "revisar-arquitetura": ".arquitetura/grills/arquitetura.<escopo>.<OPORT-ID>.md",
        "documentar-negocio": ".arquitetura/grills/negocio.<slug>.md",
        "documentar-visao": ".arquitetura/grills/visao.md",
    }
    grill_path = dynamic_grill_paths.get(name)
    if grill_path and grill_path not in text:
        probs.append(f"prompts/{name}.md: não persiste o grill dinâmico em {grill_path}")
    if grill_path:
        protocol_markers = (
            "perguntas prontas",
            "Cobertura das lentes",
            "Gatilho",
            "Jurisdição",
            "Por que importa",
            "Critério de encerramento",
            "Derivada de",
            "Estado",
        )
        for marker in protocol_markers:
            if marker not in text:
                probs.append(
                    f"prompts/{name}.md: grill dinâmico incompleto; falta {marker!r}"
                )
    gate_grill_inputs = {
        "grill-doc": ".arquitetura/grills/tecnico.<slug>.md",
        "grill-negocio": ".arquitetura/grills/negocio.<slug>.md",
        "grill-visao": ".arquitetura/grills/visao.md",
    }
    required_grill = gate_grill_inputs.get(name)
    if required_grill and required_grill not in text:
        probs.append(f"prompts/{name}.md: gate não audita o grill {required_grill}")
    if required_grill:
        for marker in ("PERGUNTA-GENERICA", "PERGUNTA-SEM-GATILHO"):
            if marker not in text:
                probs.append(f"prompts/{name}.md: gate não bloqueia {marker}")
    return probs


def _name_from_rel(rel):
    stem = Path(rel).name
    for suffix in (".prompt.md", ".md"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def verify():
    prompts = dict(read_prompts())
    problems = []
    contract_problems = []
    for name, text in prompts.items():
        contract_problems.extend(_validate_canonical_prompt(name, text))
    problems.extend(contract_problems)

    # (a) prova "sem edição à mão": regera em tmp e compara byte-a-byte com dist/.
    with tempfile.TemporaryDirectory() as tmp:
        tmp_base = Path(tmp) / "dist"
        generate(base=tmp_base, quiet=True)
        dist_files = _tree(DIST_DIR)
        tmp_files = _tree(tmp_base)
        if dist_files.keys() != tmp_files.keys():
            only_dist = sorted(dist_files.keys() - tmp_files.keys())
            only_tmp = sorted(tmp_files.keys() - dist_files.keys())
            if only_dist:
                problems.append(f"dist/ tem arquivos que o gerador não produz (editado à mão?): {only_dist}")
            if only_tmp:
                problems.append(f"dist/ está desatualizado — falta regerar: {only_tmp}")
        for rel in sorted(dist_files.keys() & tmp_files.keys()):
            if dist_files[rel] != tmp_files[rel]:
                problems.append(f"{rel}: difere da saída do gerador (editado à mão ou stale)")

    # (b) paridade de conteúdo + frontmatter, alvo a alvo.
    targets = [p for p in _tree(DIST_DIR) if p != "README.md"]
    parity_ok = 0
    for rel in sorted(targets):
        contents = (DIST_DIR / rel).read_text(encoding="utf-8")
        body, fm = split_frontmatter(contents)
        name = _name_from_rel(rel)
        if name not in prompts:
            problems.append(f"{rel}: sem canônico correspondente `{name}`")
            continue
        if body != prompts[name]:
            problems.append(f"{rel}: CORPO diverge do canônico prompts/{name}.md (drift!)")
        else:
            parity_ok += 1
        problems.extend(_validate_frontmatter(rel, fm, body))

    # relatório
    n_prompts = len(prompts)
    n_targets = len(targets)
    print("=" * 68)
    print("VERIFY · empacotamento portável (paridade + frontmatter)")
    print("=" * 68)
    print(f"Canônicos (prompts/*.md, sem README): {n_prompts}")
    print(f"Alvos gerados (dist/, sem README):    {n_targets}  "
          f"(esperado {n_prompts} × {len(TARGETS)} = {n_prompts * len(TARGETS)})")
    print(f"Corpos idênticos ao canônico:         {parity_ok}/{n_targets}")
    print(f"Contratos canônicos válidos:          "
          f"{n_prompts - len({p.split(':', 1)[0] for p in contract_problems})}/{n_prompts}")
    print("-" * 68)
    if problems:
        print(f"RESULTADO: FAIL — {len(problems)} problema(s):")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    print("RESULTADO: PASS")
    print("  ✓ dist/ é exatamente a saída do gerador (nenhum alvo editado à mão)")
    print("  ✓ todo corpo de alvo == prompt canônico (zero drift)")
    print("  ✓ todo prompt cumpre o contrato arquitetural mínimo")
    print("  ✓ frontmatter válido pela convenção de cada ferramenta")
    return 0


def _tree(base):
    """{caminho_relativo_posix: bytes} de todos os arquivos sob base."""
    out = {}
    if not base.exists():
        return out
    for p in base.rglob("*"):
        if p.is_file():
            out[p.relative_to(base).as_posix()] = p.read_bytes()
    return out


# ---------------------------------------------------------------------------
# 5) README do dist/ (deploy + smoke-test) — também gerado, também descartável
# ---------------------------------------------------------------------------

def write_readme(base, prompts):
    names = [n for n, _ in prompts]
    lines = []
    A = lines.append
    A("# `dist/` — empacotamento portável dos prompts (GERADO)\n")
    A("> **Não edite nada aqui à mão.** Tudo em `dist/` é saída de "
      "`tools/empacotar.py`\n> a partir da fonte canônica `prompts/*.md`. "
      "Editar um alvo é drift garantido.\n> Para mudar um prompt, edite o "
      "canônico e rode `python3 tools/empacotar.py`.\n")
    A(f"Prompts empacotados ({len(names)}) — a ordem da cadeia está na seção de "
      "smoke-test abaixo e em `../prompts/README.md`:\n")
    for n in names:
        A(f"- `{n}`")
    A("")
    A("## Como implantar no projeto-alvo\n")
    A("Copie a pasta da ferramenta que você usa para a **raiz do repositório-alvo**:\n")
    A("| Ferramenta | Copie | Vira |")
    A("|---|---|---|")
    A("| Amazon Q Developer | `dist/.amazonq/` | `<repo>/.amazonq/` |")
    A("| GitHub Copilot | `dist/.github/` | `<repo>/.github/` |")
    A("| Kiro | `dist/.kiro/` | `<repo>/.kiro/` |")
    A("")
    A(SMOKE_TEST_MD.rstrip() + "\n")
    (base / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# Invocação por ferramenta — confirmada nos docs/fonte oficiais (ver tools/README.md).
SMOKE_TEST_MD = '''## Como invocar cada prompt (+ smoke-test manual)

A cadeia roda **em sequência, um prompt por vez** — cada prompt termina imprimindo o
próximo comando (handoff); `.arquitetura/grills/` mantém as perguntas específicas, o
mapa mantém o ledger e `.arquitetura/gates/` mantém aprovações entre sessões:

    bootstrap-contexto → mapear-estrutura → documentar-fluxo → grill-doc → grill-mermaid
    [opcional] revisar-arquitetura
    contexto-produto → documentar-negocio → grill-negocio → documentar-visao → grill-visao

Por isso os prompts da cadeia são **invocáveis (inclusão manual)**, não always-on: always-on
injetaria todos em toda interação — bloat de contexto e quebra da sequência.

> Rodar os prompts de ponta a ponta dentro de cada ferramenta é **passo humano**. Este
> checklist só confirma que cada prompt está **invocável** no runtime certo.

### Amazon Q Developer — `.amazonq/prompts/`
Markdown puro, sem frontmatter: o arquivo inteiro é o prompt. Nome invocado = arquivo sem `.md`.

- **CLI `q chat`** (lê a pasta do projeto): na raiz do repo, rode `q chat` e invoque `@bootstrap-contexto`.
- **IDE plugin (VS Code/JetBrains)**: lê **só a pasta global** — copie os `.md` para `~/.aws/amazonq/prompts/` (ou cole o conteúdo à mão). Requer um `q`/plugin atual.

- [ ] `/prompts list` (CLI) ou o menu `@` (IDE) mostra os nomes da cadeia.
- [ ] `@bootstrap-contexto` injeta o prompt e ele começa a rodar.

### GitHub Copilot — `.github/prompts/`
Arquivo `<nome>.prompt.md`; frontmatter `agent: 'agent'` (modo agente, para os prompts que escrevem arquivos) + `description`.

- Em **VS Code / Visual Studio / JetBrains**, abra o Copilot Chat e digite `/bootstrap-contexto` (nome = arquivo sem `.prompt.md`). Recurso em public preview.

- [ ] Digitar `/` no chat lista os prompts da cadeia.
- [ ] `/bootstrap-contexto` roda e produz `.arquitetura/contexto.md`.

### Kiro — `.kiro/steering/`
Frontmatter `inclusion: manual` — o doc só entra quando você o chama (não é always-on).

- No chat do **Kiro**, referencie `#bootstrap-contexto` (nome sem `.md`) ou escolha o slash-command `/bootstrap-contexto`.

- [ ] `#` (ou `/`) no chat mostra `bootstrap-contexto` entre os manuais.
- [ ] Referenciar `#bootstrap-contexto` injeta o conteúdo na conversa.
'''


# ---------------------------------------------------------------------------

def main(argv):
    if "--verify" in argv:
        return verify()
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
