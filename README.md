# Sistema de Armazenamento Seguro com Criptografia de Arquivos

Este projeto é uma aplicação web feita em **Flask** que permite criptografar e descriptografar arquivos usando uma senha. O backend utiliza a biblioteca `cryptography` para segurança com Fernet e derivação de chave PBKDF2HMAC.

A aplicação está preparada para ser implantada na plataforma **Vercel** utilizando integração com **GitHub**.

---

## Funcionalidades

- Upload de arquivo para criptografia/descriptografia
- Entrada de senha para geração de chave de criptografia segura
- Download do arquivo processado (criptografado ou descriptografado)
- Interface web simples e responsiva com HTML e CSS

---

## Tecnologias

- Python 3.x
- Flask
- cryptography
- Vercel (para deploy)
- GitHub (para controle de versão e deploy)

---

## Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

/
├── app.py # Código principal Flask
├── requirements.txt # Dependências Python
├── vercel.json # Configuração para deploy Vercel
├── templates/
│ └── index.html # Página HTML do sistema
└── static/ # (opcional) CSS e imagens, se houver
