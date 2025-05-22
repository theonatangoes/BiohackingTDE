from flask import Flask, request, send_file
from cryptography.fernet import Fernet, InvalidToken
import io
import base64
import hashlib

# Inicializa o aplicativo Flask corretamente com _name_
app = Flask(_name_)

def gerar_chave(senha):
    """
    Gera uma chave de criptografia baseada em uma senha usando SHA-256.
    Essa chave será usada com o algoritmo Fernet.
    """
    hash_senha = hashlib.sha256(senha.encode()).digest()
    chave = base64.urlsafe_b64encode(hash_senha)
    return chave

@app.route("/processar", methods=["POST"])
def processar():
    """
    Rota para criptografar ou descriptografar um arquivo enviado via formulário.
    Espera três parâmetros no formulário: arquivo, senha e ação (criptografar ou descriptografar).
    """
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

# Correção do bloco principal para rodar o servidor
if __name__ == "_main_":
    app.run(debug=True)