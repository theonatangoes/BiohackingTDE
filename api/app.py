from flask import Flask, request, send_file, send_from_directory
from cryptography.fernet import Fernet, InvalidToken
import io
import base64
import hashlib
from collections import defaultdict
import os

app = Flask(__name__)

# Armazena a contagem de tentativas por IP
tentativas_por_ip = defaultdict(int)

def gerar_chave(senha):
    hash_senha = hashlib.sha256(senha.encode()).digest()
    return base64.urlsafe_b64encode(hash_senha)

# Serve o index.html
@app.route("/")
def index():
    return send_from_directory("../public", "index.html")

# Serve o favicon corretamente
@app.route("/iconebiohacking.svg")
def favicon():
    return send_from_directory("../public", "iconebiohacking.svg")

@app.route("/processar", methods=["POST"])
def processar():
    arquivo = request.files.get("arquivo")
    senha = request.form.get("senha")
    acao = request.form.get("acao")
    ip = request.remote_addr

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
            if tentativas_por_ip[ip] >= 5:
                return "Limite de tentativas excedido. Tente novamente mais tarde.", 429
            resultado = fernet.decrypt(conteudo)
            nome_saida = arquivo.filename.replace(".cripto", "")
            tentativas_por_ip[ip] = 0
        else:
            return "Ação inválida.", 400
    except InvalidToken:
        tentativas_por_ip[ip] += 1
        restantes = 5 - tentativas_por_ip[ip]
        return f"Senha incorreta. Tentativas restantes: {restantes}", 400
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}", 500

    return send_file(
        io.BytesIO(resultado),
        as_attachment=True,
        download_name=nome_saida,
        mimetype="application/octet-stream"
    )
