# Avaliação e métricas

Execute os testes automatizados com `python -m unittest discover -s tests -v` na raiz do projeto.

| Métrica | Como foi medida | Resultado |
| --- | --- | --- |
| Assertividade | Seis perguntas, uma por lição. Cada resposta deve conter o conceito ou resultado esperado. | 6/6 |
| Rastreabilidade | Cada uma das seis respostas deve trazer um exemplo e o link esperado. | 6/6 |
| Limite de cobertura | Pergunta fora de Python, pergunta de Python sem lição e entrada vazia. Nenhuma consulta deve chegar ao modelo. | 3/3 |
| Integração e recuperação | Resposta HTTP simulada e serviço indisponível. A aplicação mantém as fontes e usa a base quando a consulta falha. | 2/2 |

Os resultados cobrem uma amostra pequena. A integração HTTP foi testada com respostas simuladas. A qualidade das respostas de um modelo Ollama em execução e o desempenho em paráfrases novas permanecem por avaliar.
