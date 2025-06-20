# Biblioteca Flask
from flask import Flask, request, send_file, send_from_directory
from cryptography.fernet import Fernet, InvalidToken
import io
import base64
import hashlib
from collections import defaultdict
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Dicionário para controlar tentativas de acesso por IP
tentativas_por_ip = defaultdict(lambda: {"tentativas": 0, "bloqueado_ate": None})

# Função que gera uma chave segura a partir da senha fornecida
def gerar_chave(senha):
    # Cria um hash SHA-256 da senha (32 bytes)
    hash_senha = hashlib.sha256(senha.encode()).digest()
    # Codifica o hash em Base64 no formato aceito pelo Fernet
    return base64.urlsafe_b64encode(hash_senha)

# Rota principal que serve o arquivo HTML da interface
@app.route("/")
def index():
    return send_from_directory("../public", "index.html")

# Rota para servir o ícone do site
@app.route("/iconebiohacking.svg")
def favicon():
    return send_from_directory("../public", "iconebiohacking.svg")

# Rota que processa a criptografia e descriptografia do arquivo enviado
@app.route("/processar", methods=["POST"])
def processar():
    # Recebe o arquivo, senha e ação (criptografar ou descriptografar) do formulário
    arquivo = request.files.get("arquivo")
    senha = request.form.get("senha")
    acao = request.form.get("acao")
    ip = request.remote_addr  # IP do usuário para controle de tentativas

    # Validação básica: verificar se todos os dados estão presentes
    if not arquivo or not senha or not acao:
        return "Dados ausentes no formulário.", 400

    # Lê o conteúdo do arquivo enviado
    conteudo = arquivo.read()

    # Gera a chave criptográfica a partir da senha
    chave = gerar_chave(senha)

    # Inicializa o objeto Fernet com a chave gerada
    fernet = Fernet(chave)

    # Obtém as informações de tentativas para o IP atual
    info = tentativas_por_ip[ip]

    # Verifica se o IP está temporariamente bloqueado por muitas tentativas erradas
    if info["bloqueado_ate"]:
        if datetime.now() < info["bloqueado_ate"]:
            return "Limite de tentativas excedido. Tente novamente mais tarde.", 429
        else:
            # Libera o bloqueio se o tempo expirou e reseta o contador
            info["tentativas"] = 0
            info["bloqueado_ate"] = None

    try:
        # Verifica qual ação o usuário deseja realizar
        if acao == "criptografar":
            # Criptografa o conteúdo do arquivo
            resultado = fernet.encrypt(conteudo)
            nome_saida = arquivo.filename + ".cripto"
        elif acao == "descriptografar":
            # Descriptografa o conteúdo do arquivo
            resultado = fernet.decrypt(conteudo)
            nome_saida = arquivo.filename.replace(".cripto", "")
            info["tentativas"] = 0  # Reseta tentativas após sucesso
        else:
            return "Ação inválida.", 400

    except InvalidToken:
        # Se a senha estiver incorreta, incrementa o contador de tentativas
        info["tentativas"] += 1
        if info["tentativas"] >= 2:
            # Bloqueia o IP por 5 minutos após 2 tentativas falhas
            info["bloqueado_ate"] = datetime.now() + timedelta(minutes=5)
            return "Limite de tentativas excedido. Tente novamente em 5 minutos.", 429
        restantes = 2 - info["tentativas"]
        return f"Senha incorreta. Tentativas restantes: {restantes}", 400

    except Exception as e:
        # Caso ocorra algum erro inesperado durante o processamento
        return f"Erro ao processar o arquivo: {str(e)}", 500

    # Retorna o arquivo processado para o usuário para download
    return send_file(
        io.BytesIO(resultado),
        as_attachment=True,
        download_name=nome_saida,
        mimetype="application/octet-stream"
    )
