# Gera a seção Tecnologias Emergentes do Notion a partir de tecnologias.json: toggle por eixo, toggle por folha.
import json, pathlib, sys, tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "core" / "tools" / "notes"))
import notion_lines  # noqa: E402

PAGINA = "0bd17453-ea83-4019-ba38-22a79d0114ce"
TITULO = "1591656e-2069-803b-9cce-f5fb5b839f09"   # o H1 "Tecnologias Emergentes"

# Os treze blocos da lista plana que esta árvore substitui. Nomeados, nunca varridos por padrão:
# a página carrega calendário, processo e avaliação, e um delete por prefixo levaria tudo junto.
ANTIGOS = [
    "32a1656e-2069-80ad-853d-e810a73229f3", "32a1656e-2069-8098-b5c4-d8ad22590da5",
    "32a1656e-2069-80b7-8ad6-e758d45665d0", "32a1656e-2069-802f-b62e-c42cdd001a0b",
    "32a1656e-2069-800d-9288-c479c89040e5", "32a1656e-2069-80c5-a093-f71b2776b153",
    "32a1656e-2069-8060-94e1-ef544f4757d0", "32a1656e-2069-8026-bf71-e3cd642b9c24",
    "32a1656e-2069-80ae-9061-cb01825ba9cd", "32a1656e-2069-801d-9f48-c82e3a61a12d",
    "3c81656e-2069-81cb-b610-f88c1e46cb46", "3c81656e-2069-812b-bd5d-cad9dbd2bd48",
]

MARCA = {"4090": "[desktop 4090]", "Quest": "[Quest 3]",
         "licenca": "[licença]", "peca": "[peça ~R$30]"}


def par(texto):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": notion_lines.runs(texto)}}


def toggle(texto, filhos):
    return {"object": "block", "type": "toggle",
            "toggle": {"rich_text": notion_lines.runs(texto), "children": filhos}}


def folha(f):
    """Uma folha é um toggle: o nome fora, a explicação e os dois links dentro.

    O nome carrega as marcas porque é a única linha que a equipe lê ao ordenar — se o custo de
    equipamento só aparecesse aberto, a ordenação sairia sem ele.
    """
    marcas = "".join(" " + MARCA[f["precisa"]] for _ in (1,) if f["precisa"])
    titulo = f"**{f['nome']}**{marcas}" + ("  ⚡" if f["novo"] else "")
    estrelas = f"{f['estrelas']:,}".replace(",", ".")   # milhar em ponto, só no número
    dentro = [par(f["oque"]),
              par(f"[▶ vídeo]({f['video']})  ·  "
                  f"[⌘ {f['repo'].split('github.com/')[-1]}]({f['repo']})  "
                  f"{estrelas}★, último commit {f['push']}")]
    return toggle(titulo, dentro)


def blocos(dado):
    """A seção inteira: uma abertura, doze eixos, um fecho que devolve a busca à turma."""
    out = [par("**Ordene esta árvore**, da tecnologia que a equipe mais quer usar para a que menos "
               "quer. Abra o toggle do eixo, abra o da folha: cada folha tem um vídeo e um "
               "repositório. Sem marca = roda no laptop de vocês. ⚡ = pouca gente usou ainda, e é "
               "por isso que rende artigo.")]
    for e in dado["eixos"]:
        fs = e["folhas"]
        out.append(toggle(f"**{e['eixo']}** · {len(fs)} tecnologias",
                          [folha(f) for f in fs]))
    d = dado["depois_da_arvore"]
    out.append(par(f"Esta árvore é ponto de partida, não teto — foi conferida em "
                   f"{dado['conferido']} e envelhece. O que a aula ensinou vale mais que ela: "
                   f"[papers em alta]({d['papers']}) e [repositórios em alta]({d['repos']})."))
    return out


def ops(dado):
    """Escrever ANTES de apagar. Se o append falhar, a página velha continua inteira."""
    return ([{"op": "append", "parent": PAGINA, "after": TITULO, "children": blocos(dado)}]
            + [{"op": "delete", "block": b} for b in ANTIGOS])


def main():
    dado = json.loads((AQUI / "tecnologias.json").read_text(encoding="utf-8"))
    # Fora da árvore por padrão: o plano é descartável, regenera do JSON, e versioná-lo deixaria
    # dois lugares dizendo a mesma coisa — um deles sempre atrasado.
    destino = (pathlib.Path(sys.argv[1]) if len(sys.argv) > 1
               else pathlib.Path(tempfile.gettempdir()) / "notion-ops-tecnologias.json")
    plano = ops(dado)
    destino.write_text(json.dumps(plano, ensure_ascii=False, indent=1),
                       encoding="utf-8", newline="\n")
    n = sum(len(e["folhas"]) for e in dado["eixos"])
    print(f"{len(dado['eixos'])} eixos, {n} folhas -> {destino}")
    print(f"  aplicar: core/run tools/notes/notion apply --account personal {destino}")


if __name__ == "__main__":
    main()
