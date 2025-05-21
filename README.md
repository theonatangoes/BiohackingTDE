# BiohackingTDE

# 🔐 Sistema de Armazenamento Seguro com Criptografia de Arquivos

Projeto desenvolvido para o **TDE 02 da disciplina de Biohacking**, com foco na implementação de um sistema de criptografia de arquivos utilizando Python.

## 🎯 Objetivo

Desenvolver uma aplicação prática que permita o **upload e armazenamento seguro de arquivos**, protegidos por criptografia. O sistema garante que apenas usuários autorizados possam descriptografar e acessar os dados, contribuindo para a segurança digital e integridade da informação.

## 🛠 Tecnologias e Bibliotecas

- Python 3.x
- `cryptography` (biblioteca para criptografia simétrica)
- Interface em terminal (CLI)
- Sistema de arquivos local para simular o armazenamento

## 🔄 Funcionalidades

- 🔐 Criptografar arquivos com senha do usuário
- 🔓 Descriptografar arquivos com a mesma senha
- 📁 Armazenar os arquivos criptografados em um diretório seguro
- ❌ Impedir acesso a arquivos sem senha válida

## 🚨 Segurança Implementada

- Criptografia **simétrica (Fernet/AES)**
- Proteção por senha com geração de chave segura
- Análise de possíveis vulnerabilidades e recomendações

## 🧪 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/theonatangoes/BiohackingTDE.git
   cd BiohackingTDE
   ```
