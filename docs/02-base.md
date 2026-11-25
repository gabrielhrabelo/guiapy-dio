# Base de conhecimento

A base [`data/licoes.json`](../data/licoes.json) contém seis lições escritas para o projeto. Cada registro tem um identificador, título, termos de busca, explicação, exemplo e fonte na documentação oficial do Python.

A busca ignora maiúsculas e acentos. Ela pontua termos inteiros e seleciona até duas lições. Sem correspondência, o agente apresenta os assuntos disponíveis. Com o Ollama ativado, a requisição inclui somente a pergunta, o título e o texto das lições encontradas. Os exemplos e links são exibidos diretamente do JSON.

Uma pergunta sobre `kwargs`, por exemplo, recupera a lição de argumentos posicionais e nomeados. A aplicação mostra o exemplo `registrar('Ana', 2, curso='Python')` e aponta para a seção sobre definição de funções da documentação oficial.
