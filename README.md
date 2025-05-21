# 🔐 Sistema de Armazenamento Seguro com Criptografia de Arquivos

Projeto desenvolvido para o **TDE 02 da disciplina de Biohacking**, com foco na implementação de um sistema de criptografia de arquivos utilizando Python e uma interface web simples em Flask.

## 🎯 Objetivo

Desenvolver uma aplicação prática que permita o **upload, criptografia e armazenamento seguro de arquivos**, além da descriptografia, garantindo que apenas usuários autorizados possam acessar os dados. O sistema contribui para a segurança digital e integridade da informação.

## 🛠 Tecnologias e Bibliotecas

- Python 3.x
- Flask (para interface web)
- `cryptography` (biblioteca para criptografia simétrica - Fernet/AES)
- Sistema de arquivos local para armazenamento seguro

## 🔄 Funcionalidades

- 🔐 Upload e criptografia de arquivos com senha do usuário
- 🔓 Descriptografia de arquivos protegidos pela mesma senha
- 📁 Armazenamento dos arquivos criptografados em diretório seguro (`arquivos/`)
- 🌐 Interface web simples para facilitar o uso
- ❌ Controle de acesso via senha para evitar acesso não autorizado

## 🚨 Segurança Implementada

- Criptografia **simétrica (Fernet/AES)**
- Geração de chave segura a partir da senha
- Medidas para prevenir acesso indevido aos arquivos
- Análise básica de riscos e recomendações

## 🧪 Como Usar

1. Clone o repositório:

   ```bash
   git clone https://github.com/theonatangoes/BiohackingTDE.git
   cd BiohackingTDE

   BiohackingTDE/
   ├── README.md
   ├── main.py                  # Servidor Flask principal
   ├── criptografia/
   │   ├── __init__.py
   │   ├── criptografar.py      # Funções de criptografia
   │   └── descriptografar.py   # Funções de descriptografia
   ├── arquivos/                # Armazenamento dos arquivos criptografados/descriptografados
   ├── templates/
   │   └── index.html           # Front-end HTML e CSS para interface web
   ```
