# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

def gerar_doc(dados, tipo): 
    """Função que centraliza a lógica e formata o documento como folha oficial"""
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
    hoje = datetime.now()
    cidade_usuario = dados.get('cidade', 'Curitiba - PR')
    data_formatada = f"{cidade_usuario}, {hoje.day} de {meses[hoje.month - 1]} de {hoje.year}."

    titulo = ""
    corpo = ""

    # CORRIGIDO: Substituídos os 'returns' por atribuição de variáveis para o layout executar completo
    if tipo == "1":
        titulo = "DECLARAÇÃO DE RESPONSÁVEIS"
        corpo = f"Eu, {dados['nome']}, portador do CPF {dados['cpf']}, autorizo meu filho a participar da viagem escolar com destino à Disney."
    elif tipo == "2":
        titulo = "DECLARAÇÃO DE RESIDÊNCIA"
        corpo = f"Eu, {dados['nome']}, portador do CPF {dados['cpf']}, declaro que resido no endereço {dados['endereco']} referente ao trabalho de autônomo de desenvolvedor."
    elif tipo == "3":
        titulo = "DECLARAÇÃO DE RENDA"
        corpo = f"Eu, {dados['nome']}, portador do CPF {dados['cpf']}, declaro que recebo o valor médio de R$ {dados['renda']} referente ao trabalho de autônomo de desenvolvedor."
    elif tipo == "4":
        titulo = "DECLARAÇÃO DE DOADOR DE MEDULA ÓSSEA"
        corpo = f"EU, {dados['nome']}, portador do CPF {dados['cpf']}, residente na rua {dados['endereco']}, declaro para os devidos fins que sou doador voluntário de medula óssea."
    else:
        return "!Erro: Esse formulário ainda não existe!"

    # estrutura para imprimir o documento
    documento_oficial = (
        f"\n"
        f"                                             {titulo}\n"
        f"-------------------------------------------------------------------------------------------------------\n\n\n\n"
        f"{corpo}\n\n\n\n\n"
        f"Por ser a expressão da verdade, firmo a presente.\n\n\n"
        f"{data_formatada}\n\n\n\n\n\n\n"
        f"                                      _________________________________________\n"
        f"                                      Assinatura do(a) Declarante: {dados['nome']}\n"
    )
    
    return documento_oficial

def salvar(arquivo, conteudo):
    pasta_segura = os.path.join(os.getcwd(), "documentos_gerados")
    if not os.path.exists(pasta_segura):
        os.makedirs(pasta_segura)
        
    caminho_completo = os.path.join(pasta_segura, arquivo)

    with open(caminho_completo, "w", encoding="utf-8") as arquivo_fisico:
        arquivo_fisico.write(conteudo)
        print(f"\n[SUCESSO] Arquivo salvo no seu Desktop na pasta: 'documentos_gerados/{arquivo}'")

@app.route('/gerar-documento', methods=['POST'])
def api_gerar_documento():
    requisicao = request.get_json()
    dados_pessoa = requisicao.get('pessoa')
    selecionar = requisicao.get('opcao_formulario')

    doc_final = gerar_doc(dados_pessoa, selecionar)

    if "Erro:" not in doc_final:
        nome_arquivo = f"documento_{dados_pessoa['nome'].lower().replace(' ', '-')}.txt"
        salvar(nome_arquivo, doc_final)

        return jsonify({
            "status": "sucesso",
            "documento": doc_final,
            "arquivo_salvo": nome_arquivo
        }), 200
    else: 
        return jsonify({
            "status": "erro",
            "mensagem": doc_final
        }), 400

if __name__ == '__main__':
    porta = int (os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=porta, debug=False)  # pyright: ignore[reportUndefinedVariable]