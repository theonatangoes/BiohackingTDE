from flask import Flask, request, send_file   
from cryptography.fernet import Fernet, InvalidToken  
import io  
import base64 
import hashlib 

app = Flask(__name__)

def gerar_chave(senha):
    """
    Gera uma chave criptográfica a partir da senha usando SHA-256.
    A chave precisa estar no formato compatível com o algoritmo Fernet.
    """
    hash_senha = hashlib.sha256(senha.encode()).digest()  # Cria um hash SHA-256 da senha
    chave = base64.urlsafe_b64encode(hash_senha)  # Codifica o hash em base64 (formato exigido pelo Fernet)
    return chave  # Retorna a chave pronta para uso na criptografia

@app.route("/processar", methods=["POST"])
def processar():
    """
    Rota principal da API. Processa um arquivo enviado por formulário e realiza
    a criptografia ou descriptografia dependendo da ação escolhida pelo usuário.
    """

    # Obtém os dados enviados pelo formulário
    arquivo = request.files.get("arquivo")  # Arquivo enviado pelo usuário
    senha = request.form.get("senha")       # Senha fornecida
    acao = request.form.get("acao")         # Ação escolhida: criptografar ou descriptografar

    # Verifica se todos os dados foram preenchidos
    if not arquivo or not senha or not acao:
        return "Dados ausentes no formulário.", 400  # Erro HTTP 400: requisição inválida

    # Lê o conteúdo do arquivo
    conteudo = arquivo.read()

    # Gera a chave de criptografia com base na senha
    chave = gerar_chave(senha)

    # Cria o objeto Fernet com a chave gerada
    fernet = Fernet(chave)

    try:
        # Realiza a criptografia
        if acao == "criptografar":
            resultado = fernet.encrypt(conteudo)  # Criptografa o conteúdo do arquivo
            nome_saida = arquivo.filename + ".cripto"  # Adiciona a extensão .cripto ao nome do arquivo

        # Realiza a descriptografia
        elif acao == "descriptografar":
            resultado = fernet.decrypt(conteudo)  # Descriptografa o conteúdo
            nome_saida = arquivo.filename.replace(".cripto", "")  # Remove a extensão .cripto do nome

        # Caso a ação seja inválida
        else:
            return "Ação inválida.", 400

    # Se a senha estiver errada ou o conteúdo não for compatível
    except InvalidToken:
        return "Senha incorreta ou arquivo inválido.", 400

    # Captura qualquer outro erro que possa ocorrer
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}", 500

    # Envia o arquivo processado de volta ao usuário como download
    return send_file(
        io.BytesIO(resultado),  # Cria um arquivo temporário em memória com o conteúdo criptografado ou descriptografado
        as_attachment=True,  # Garante que o arquivo seja baixado e não exibido no navegador
        download_name=nome_saida,  # Nome do arquivo que será baixado
        mimetype="application/octet-stream"  # Tipo de arquivo genérico
    )

# Bloco para rodar o app Flask localmente (não afeta o funcionamento no Vercel)
if __name__ == "__main__":
    app.run(debug=True)
