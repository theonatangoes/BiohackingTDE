from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

PASTA_ARQUIVOS = 'arquivos'

# Certifique-se de que a pasta existe
os.makedirs(PASTA_ARQUIVOS, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    arquivo = request.files.get('arquivo')
    senha = request.form.get('senha')
    acao = request.form.get('acao')

    if not arquivo or not senha or not acao:
        return "Arquivo, senha e ação são obrigatórios.", 400

    nome_arquivo = arquivo.filename
    caminho_salvar = os.path.join(PASTA_ARQUIVOS, nome_arquivo)
    arquivo.save(caminho_salvar)

    if acao == 'criptografar':
        # TODO: Substituir com a função real de criptografia
        print(f'Criptografando {nome_arquivo} com a senha: {senha}')
        return f"Arquivo {nome_arquivo} enviado para criptografia com a senha fornecida."
    elif acao == 'descriptografar':
        # TODO: Substituir com a função real de descriptografia
        print(f'Descriptografando {nome_arquivo} com a senha: {senha}')
        return f"Arquivo {nome_arquivo} enviado para descriptografia com a senha fornecida."
    else:
        return "Ação inválida.", 400

if __name__ == '__main__':
    app.run(debug=True)
