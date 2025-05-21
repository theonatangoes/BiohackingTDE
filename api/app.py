from flask import Flask, render_template, request, send_file
from cryptography.fernet import Fernet, InvalidToken
from io import BytesIO
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)

# SAL -> pode ser fixo ou gerar aleatório e armazenar junto (aqui fixo para exemplo)
SALT = b'meu_salt_fixo_1234'  # SALT tem que ser bytes e ter tamanho adequado

def gerar_chave(senha: str) -> bytes:
    """
    Deriva uma chave Fernet a partir da senha usando PBKDF2HMAC
    """
    senha_bytes = senha.encode()  # transforma a senha em bytes

    # Configuração do KDF
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100_000,
    )

    chave = kdf.derive(senha_bytes)  # gera a chave derivada da senha
    chave_fernet = base64.urlsafe_b64encode(chave)  # Fernet precisa da chave base64 urlsafe

    return chave_fernet

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
    dados = arquivo.read()

    chave = gerar_chave(senha)
    fernet = Fernet(chave)

    try:
        if acao == 'criptografar':
            dados_processados = fernet.encrypt(dados)
            nome_saida = nome_arquivo + '.enc'

        elif acao == 'descriptografar':
            dados_processados = fernet.decrypt(dados)
            if nome_arquivo.endswith('.enc'):
                nome_saida = nome_arquivo[:-4]
            else:
                nome_saida = 'descriptografado_' + nome_arquivo
        else:
            return "Ação inválida.", 400

        arquivo_saida = BytesIO(dados_processados)
        arquivo_saida.seek(0)

        return send_file(
            arquivo_saida,
            as_attachment=True,
            download_name=nome_saida,
            mimetype='application/octet-stream'
        )

    except InvalidToken:
        return "Senha incorreta ou arquivo inválido para descriptografia.", 400
    except Exception as e:
        return f"Erro: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
