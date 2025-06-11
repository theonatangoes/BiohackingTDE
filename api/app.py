from flask import Flask, request, send_file, send_from_directory
from cryptography.fernet import Fernet, InvalidToken
import io
import base64
import hashlib
from collections import defaultdict
from datetime import datetime, timedelta
import os

app = Flask(__name__)

tentativas_por_ip = defaultdict(lambda: {"tentativas": 0, "bloqueado_ate": None})

def gerar_chave(senha):
    hash_senha = hashlib.sha256(senha.encode()).digest()
    return base64.urlsafe_b64encode(hash_senha)

@app.route("/")
def index():
    return send_from_directory("../public", "index.html")

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

    info = tentativas_por_ip[ip]

    if info["bloqueado_ate"]:
        if datetime.now() < info["bloqueado_ate"]:
            return "Limite de tentativas excedido. Tente novamente mais tarde.", 429
        else:
            
            info["tentativas"] = 0
            info["bloqueado_ate"] = None

    try:
        if acao == "criptografar":
            resultado = fernet.encrypt(conteudo)
            nome_saida = arquivo.filename + ".cripto"
        elif acao == "descriptografar":
            resultado = fernet.decrypt(conteudo)
            nome_saida = arquivo.filename.replace(".cripto", "")
            info["tentativas"] = 0  # reset em caso de sucesso
        else:
            return "Ação inválida.", 400
    except InvalidToken:
        info["tentativas"] += 1
        if info["tentativas"] >= 2:
            info["bloqueado_ate"] = datetime.now() + timedelta(minutes=5)
            return "Limite de tentativas excedido. Tente novamente em 5 minutos.", 429
        restantes = 2 - info["tentativas"]
        return f"Senha incorreta. Tentativas restantes: {restantes}", 400
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}", 500

    return send_file(
        io.BytesIO(resultado),
        as_attachment=True,
        download_name=nome_saida,
        mimetype="application/octet-stream"
    )
