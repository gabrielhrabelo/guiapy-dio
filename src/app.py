import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

RAIZ = Path(__file__).resolve().parents[1]
SEM_COBERTURA = (
    "Não encontrei essa dúvida na base do GuiaPy. "
    "Posso ajudar com compreensão de listas, tuplas, conjuntos, dicionários, funções e argumentos."
)


def carregar_licoes():
    return json.loads((RAIZ / "data" / "licoes.json").read_text(encoding="utf-8"))


def normalizar(texto):
    decomposto = unicodedata.normalize("NFKD", texto.casefold())
    sem_acentos = "".join(letra for letra in decomposto if not unicodedata.combining(letra))
    return " ".join(re.findall(r"\w+", sem_acentos))


def buscar_licoes(pergunta, licoes):
    texto = f" {normalizar(pergunta)} "
    pontuadas = []
    for licao in licoes:
        pontos = sum(
            len(termo.split()) for termo in licao["termos"] if f" {normalizar(termo)} " in texto
        )
        if pontos:
            pontuadas.append((pontos, licao))
    pontuadas.sort(key=lambda item: item[0], reverse=True)
    return [licao for _, licao in pontuadas[:2]]


def explicar_com_ollama(modelo, pergunta, licoes):
    prompt = (RAIZ / "docs" / "03-prompts.md").read_text(encoding="utf-8").split("```", 2)[1]
    contexto = [{"tema": licao["titulo"], "conteudo": licao["explicacao"]} for licao in licoes]
    payload = {
        "model": modelo,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 220},
        "messages": [
            {"role": "system", "content": prompt.removeprefix("text\n").strip()},
            {"role": "user", "content": json.dumps({"pergunta": pergunta, "licoes": contexto}, ensure_ascii=False)},
        ],
    }
    pedido = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(pedido, timeout=30) as resposta:
        texto = json.load(resposta)["message"]["content"].strip()
    if not texto:
        raise ValueError("O modelo retornou uma resposta vazia.")
    return texto


def responder(pergunta, licoes, modelo=None):
    encontradas = buscar_licoes(pergunta, licoes)
    if not encontradas:
        return SEM_COBERTURA

    if modelo:
        try:
            explicacao = explicar_com_ollama(modelo, pergunta, encontradas)
            return "\n\n".join([f"Explicação do modelo: {explicacao}", *formatar_licoes(encontradas)])
        except (URLError, TimeoutError, KeyError, TypeError, AttributeError, ValueError):
            return "\n\n".join(["Modelo indisponível. Segue a consulta direta à base.", *formatar_licoes(encontradas)])

    return "\n\n".join(formatar_licoes(encontradas))


def formatar_licoes(licoes):
    return [
        f'{item["titulo"]}\n{item["explicacao"]}\nExemplo:\n{item["exemplo"]}\nFonte: {item["fonte"]}'
        for item in licoes
    ]


def main():
    parser = argparse.ArgumentParser(description="GuiaPy, tutor de Python para iniciantes")
    parser.add_argument("--modelo", help="Nome de um modelo instalado no Ollama local")
    args = parser.parse_args()
    licoes = carregar_licoes()
    print("GuiaPy | Tire uma dúvida de Python. Digite 'sair' para encerrar.")
    while True:
        try:
            pergunta = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if pergunta.casefold() == "sair":
            break
        if pergunta:
            print(f"\nGuiaPy: {responder(pergunta, licoes, args.modelo)}")


if __name__ == "__main__":
    main()
