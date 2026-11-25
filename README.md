# GuiaPy

GuiaPy é um tutor de Python para iniciantes. Ele conversa pelo terminal, consulta uma base com seis temas e mostra uma explicação curta, um exemplo e a fonte oficial. A base inclui compreensão de listas, tuplas, conjuntos, dicionários, funções e argumentos.

## Executar

Com Python 3.10 ou superior, na raiz do projeto:

```bash
python src/app.py
```

Experimente perguntar `Posso alterar uma tupla?` ou `Como uso *args e **kwargs?`. Digite `sair` para encerrar. A consulta direta à base funciona sem instalar pacotes ou configurar uma conta.

Para habilitar a explicação generativa, instale o [Ollama](https://ollama.com/), baixe o modelo e deixe o serviço local em execução:

```bash
ollama pull qwen2.5:1.5b
python src/app.py --modelo qwen2.5:1.5b
```

## Etapas do desafio

1. [Documentação do agente](docs/01-agente.md)
2. [Base de conhecimento](docs/02-base.md)
3. [Prompts](docs/03-prompts.md)
4. [Aplicação funcional](src/app.py)
5. [Avaliação e métricas](docs/04-metricas.md)
6. [Pitch](docs/05-pitch.md)

Projeto desenvolvido a partir do [roteiro oficial da DIO](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).
