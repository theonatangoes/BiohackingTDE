# Sistema de Armazenamento Seguro com Criptografia de Arquivos

Este projeto é uma aplicação web desenvolvida com **Python e Flask** que permite **criptografar e descriptografar arquivos com uma senha definida pelo usuário**. O sistema utiliza a biblioteca `cryptography` com o algoritmo **Fernet**, derivando a chave a partir de uma senha usando **SHA-256** e **Base64**.

A aplicação está pronta para ser **implantada na plataforma Vercel** com integração via GitHub.

---

## 🔒 Funcionalidades

- Upload de arquivos para **criptografar** ou **descriptografar**
- Geração de chave criptográfica a partir de senha segura (SHA-256)
- Download do arquivo processado (.cripto ou restaurado)
- **Bloqueio após 5 tentativas de senha incorreta por IP**
- Interface web simples e responsiva com HTML e CSS
- Sistema não armazena arquivos nem senhas no servidor

---

## 🛡️ Medidas de Segurança

- **Criptografia Simétrica** com Fernet (AES + HMAC)
- **Derivação de chave segura** com SHA-256 + Base64
- **Limite de tentativas por IP (5 vezes)** para evitar ataques de força bruta
- **Validação de entrada e tratamento de erros**
- Arquivos e senhas **não são armazenados** no servidor

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask** – Framework web
- **cryptography** – Biblioteca de criptografia (Fernet)
- **HTML/CSS** – Interface web
- **Vercel** – Deploy automático
- **GitHub** – Controle de versão e deploy

---

## 📚 Estrutura do Projeto

BiohackingTDE-main/
├── api/
│ └── app.py  
├── public/
│ ├── index.html  
│ └── iconebiohacking.svg  
├── requirements.txt  
├── vercel.json  
└── README.md
