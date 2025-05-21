from flask import Flask, request, send_file
from cryptography.fernet import Fernet, InvalidToken
import io
import base64
import hashlib

app = Flask(__name__)

def gerar_chave(senha):
    hash_senha = hashlib.sha256(senha.encode()).digest()
    chave = base64.urlsafe_b64encode(hash_senha)
    return chave

@app.route("/processar", methods=["POST"])
def processar():
    arquivo = request.files.get("arquivo")
    senha = request.form.get("senha")
    acao = request.form.get("acao")

    if not arquivo or not senha or not acao:
        return "Dados ausentes no formulário.", 400

    conteudo = arquivo.read()
    chave = gerar_chave(senha)
    fernet = Fernet(chave)

    try:
        if acao == "criptografar":
            resultado = fernet.encrypt(conteudo)
            nome_saida = arquivo.filename + ".cripto"
        elif acao == "descriptografar":
            resultado = fernet.decrypt(conteudo)
            nome_saida = arquivo.filename.replace(".cripto", "")
        else:
            return "Ação inválida.", 400
    except InvalidToken:
        return "Senha incorreta ou arquivo inválido.", 400
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}", 500

    return send_file(
        io.BytesIO(resultado),
        as_attachment=True,
        download_name=nome_saida,
        mimetype="application/octet-stream"
    )

if __name__ == "__main__":
    app.run(debug=True)
