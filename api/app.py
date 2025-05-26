from flask import Flask, request, send_file
from cryptography.fernet import Fernet, InvalidToken
import io
import base64
import hashlib
from collections import defaultdict

app = Flask(__name__)

# Armazena a contagem de tentativas por IP
tentativas_por_ip = defaultdict(int)

def gerar_chave(senha):
    """
    Gera uma chave Fernet baseada na senha usando SHA-256 e Base64.
    """
    hash_senha = hashlib.sha256(senha.encode()).digest()
    return base64.urlsafe_b64encode(hash_senha)

@app.route("/processar", methods=["POST"])
def processar():
    # Recebe dados do formulário
    arquivo = request.files.get("arquivo")
    senha = request.form.get("senha")
    acao = request.form.get("acao")
    ip = request.remote_addr  # IP do usuário

    # Verifica se todos os campos foram preenchidos
    if not arquivo or not senha or not acao:
        return "Dados ausentes no formulário.", 400

    # Lê o conteúdo do arquivo enviado
    conteudo = arquivo.read()

    # Gera a chave criptográfica com base na senha
    chave = gerar_chave(senha)
    fernet = Fernet(chave)

    try:
        if acao == "criptografar":
            # Criptografa o conteúdo
            resultado = fernet.encrypt(conteudo)
            nome_saida = arquivo.filename + ".cripto"

        elif acao == "descriptografar":
            # Verifica se o IP excedeu 5 tentativas
            if tentativas_por_ip[ip] >= 5:
                return "Limite de tentativas excedido. Tente novamente mais tarde.", 429

            # Tenta descriptografar
            resultado = fernet.decrypt(conteudo)
            nome_saida = arquivo.filename.replace(".cripto", "")
            tentativas_por_ip[ip] = 0  # Zera tentativas após sucesso

        else:
            return "Ação inválida.", 400

    except InvalidToken:
        # Incrementa tentativa após erro de senha
        tentativas_por_ip[ip] += 1
        restantes = 5 - tentativas_por_ip[ip]
        return f"Senha incorreta. Tentativas restantes: {restantes}", 400

    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}", 500

    # Envia o arquivo processado como download
    return send_file(
        io.BytesIO(resultado),
        as_attachment=True,
        download_name=nome_saida,
        mimetype="application/octet-stream"
    )

# Roda o servidor localmente (desativado na Vercel)
if __name__ == "__main__":
    app.run(debug=True)
