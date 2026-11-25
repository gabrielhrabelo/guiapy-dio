import io
import json
import unittest
from unittest.mock import patch
from urllib.error import URLError

from src.app import SEM_COBERTURA, carregar_licoes, responder


class TestGuia(unittest.TestCase):
    def setUp(self):
        self.licoes = carregar_licoes()

    def test_assertividade_e_fontes(self):
        casos = {
            "Como uso compreensão para filtrar pares?": ("[0, 4, 16]", "#list-comprehensions"),
            "Posso alterar uma tupla?": ("imutável", "#tuples-and-sequences"),
            "Como remover duplicatas?": ("dict.fromkeys", "#sets"),
            "Como tratar uma chave ausente em um dicionário?": ("None", "#dictionaries"),
            "Uma função pode devolver valores?": ("devolve uma tupla", "#defining-functions"),
            "Como uso *args e **kwargs?": ("argumentos posicionais", "#more-on-defining-functions"),
        }
        for pergunta, (trecho, fonte) in casos.items():
            with self.subTest(pergunta=pergunta):
                resposta = responder(pergunta, self.licoes)
                self.assertIn(trecho, resposta)
                self.assertIn(fonte, resposta)
                self.assertIn("Exemplo:", resposta)

    @patch("src.app.urlopen")
    def test_fora_da_base_nao_consulta_modelo(self, abrir):
        for pergunta in ["Qual é a capital da Islândia?", "Como escrever metaclasses?", "   "]:
            with self.subTest(pergunta=pergunta):
                self.assertEqual(responder(pergunta, self.licoes, "teste"), SEM_COBERTURA)
        abrir.assert_not_called()

    @patch("src.app.urlopen")
    def test_envio_do_prompt_e_contexto_ao_modelo(self, abrir):
        abrir.return_value = io.BytesIO(b'{"message":{"content":"Uma tupla tem tamanho fixo."}}')
        resposta = responder("Posso alterar uma tupla?", self.licoes, "modelo-teste")
        pedido = abrir.call_args.args[0]
        payload = json.loads(pedido.data)
        contexto = json.loads(payload["messages"][1]["content"])
        self.assertEqual(pedido.full_url, "http://127.0.0.1:11434/api/chat")
        self.assertEqual(payload["model"], "modelo-teste")
        self.assertIn("Você é o GuiaPy", payload["messages"][0]["content"])
        self.assertEqual([licao["tema"] for licao in contexto["licoes"]], ["Tuplas"])
        self.assertIn("Explicação do modelo:", resposta)
        self.assertIn("#tuples-and-sequences", resposta)

    @patch("src.app.urlopen", side_effect=URLError("indisponível"))
    def test_falha_do_modelo_preserva_a_resposta_da_base(self, abrir):
        resposta = responder("O que é um conjunto?", self.licoes, "modelo-teste")
        self.assertIn("Modelo indisponível", resposta)
        self.assertIn("elementos distintos", resposta)
        self.assertIn("#sets", resposta)
