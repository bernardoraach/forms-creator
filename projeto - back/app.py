# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import os  # IMPORTANTE: Biblioteca nativa para gerenciar pastas

app = Flask(__name__)
CORS(app)  # Libera o acesso para o Front-End bater na API

def gerar_doc(dados, tipo): 
    """Função que centraliza a lógica de qual formulário gerar"""
    if tipo == "1":
        return f"DECLARAÇÃO DE RESPONSÁVEIS: Eu, {dados['nome']}, portador do CPF {dados['cpf']}, autorizo meu filho a participar da viagem escolar com destino à Disney"
    elif tipo == "2":
        return f"DECLARAÇÃO DE RESIDÊNCIA: Eu, {dados['nome']}, portador do CPF {dados['cpf']}, declaro que resido no endereço {dados['endereco']} referente ao trabalho de autônomo de desenvolvedor."
    elif tipo == "3":
        return f"DECLARAÇÃO DE RENDA: Eu, {dados['nome']}, portador do CPF {dados['cpf']}, declaro que recebo o valor médio de {dados['renda']} referente ao trabalho de autônomo de desenvolvedor."
    elif tipo == "4":
        return f"DECLARAÇÃO DE DOADOR DE MEDULA ÓSSEA: EU, {dados['nome']}, portador do CPF {dados['cpf']}, residente na rua {dados['endereco']}, declaro para os devidos fins que sou doador voluntário de medula óssea."
    else:
        return "!Erro: Esse formulário ainda não existe!"

def salvar(arquivo, conteudo):
    # CORREÇÃO CHAVE: Cria uma pasta chamada 'documentos_exportados' fora do alcance do recarregamento do Flask
    # Ela será criada de forma invisível e segura no seu sistema
    pasta_segura = os.path.expanduser("~/Desktop/documentos_gerados")
    if not os.path.exists(pasta_segura):
        os.makedirs(pasta_segura)
        
    caminho_completo = os.path.join(pasta_segura, arquivo)

    with open(caminho_completo, "w", encoding="utf-8") as arquivo_fisico:
        arquivo_fisico.write(conteudo)
        print(f"\n[SUCESSO] Arquivo salvo no seu Desktop na pasta: 'documentos_gerados/{arquivo}'")

# Criando rota de API
@app.route('/gerar-documento', methods=['POST'])
def api_gerar_documento():
    requisicao = request.get_json()

    dados_pessoa = requisicao.get('pessoa')
    selecionar = requisicao.get('opcao_formulario')

    doc_final = gerar_doc(dados_pessoa, selecionar)

    if "Erro:" not in doc_final:
        nome_arquivo = f"documento_{dados_pessoa['nome'].lower().replace(' ', '-')}.txt"
        
        # Salva na pasta isolada para não resetar o servidor
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

print(f"O valor de __name__ é: {__name__}")
if __name__ == '__main__':
    # Ligamos o servidor de forma limpa
    app.run(debug=False, port=5000)