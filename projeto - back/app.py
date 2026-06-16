
#dicionários e funções
# from typing import final

# IMPORTADO flask import para trasformar em um servidor web
#no terminal digitado : pip3 install flask

# from crypt import methods
# from pydoc import doc
from flask import Flask, request, jsonify;
from flask_cors import CORS #importação para HTML

app = Flask(__name__)
CORS(app) #libera o acesso para o Front-End bater na API


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

#salvar em arquivo
    # Função do Back-end para criar e escrever em um arquivo físico
    #with open: abre o arquivo. o "w" significa 'write' (escrever/subescrever)
    #'enconding="utf-8", serve para não quebrar os acentos em portugues
def salvar (arquivo, conteudo):

    with open(arquivo, "w", encoding="utf-8") as arquivo_fisico:
        arquivo_fisico.write(conteudo)
        print(f"\nArquivo salvo na pasta '{arquivo}'")

#criando rota de API

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

    
print(f"O valor de __name__ é: {__name__}"

)
if __name__ == '__main__':
        app.run(debug=True, port=5000)

