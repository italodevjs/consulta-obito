# 🔍 Consulta de Óbito — Ferramenta CLI

Ferramenta de linha de comando para verificar se uma pessoa está registrada em óbito nas principais bases de dados públicas brasileiras. Desenvolvida para uso em investigações com Kali Linux e sistemas Debian/Ubuntu.

---

## ⚙️ Instalação no Kali Linux

Abra o terminal e execute os comandos abaixo:

```bash
# 1. Clone o repositório
git clone https://github.com/caetanoitalo59-boop/consulta-obito.git

# 2. Entre na pasta
cd consulta-obito

# 3. Instale as dependências
sudo pip3 install requests beautifulsoup4

# 4. Torne o script executável
chmod +x consulta_obito.py
```

---

## 🚀 Como Usar

### Busca simples por nome
```bash
python3 consulta_obito.py -n "Nome da Pessoa"
```

### Busca com CPF
```bash
python3 consulta_obito.py -n "João Silva" -c "12345678901"
```

### Busca com data de nascimento
```bash
python3 consulta_obito.py -n "Maria Santos" -d "15/03/1950"
```

### Busca completa (nome + CPF + data)
```bash
python3 consulta_obito.py -n "Pedro Costa" -c "98765432100" -d "20/12/1955"
```

### Ver ajuda
```bash
python3 consulta_obito.py --help
```

---

## 📋 Opções Disponíveis

| Opção | Descrição |
|-------|-----------|
| `-n, --nome` | Nome da pessoa (**obrigatório**) |
| `-c, --cpf` | CPF da pessoa (opcional) |
| `-d, --data` | Data de nascimento no formato `DD/MM/YYYY` (opcional) |
| `-h, --help` | Exibe a ajuda |
| `-v, --version` | Exibe a versão |

---

## 🗄️ Fontes de Dados Consultadas

| Fonte | Descrição | Registros |
|-------|-----------|-----------|
| **CNF Brasil** | Cadastro Nacional de Falecidos | 50+ milhões |
| **Portal Registro Civil** | Base oficial de certidões de óbito | Nacional |
| **SIM DATASUS** | Sistema de Informação sobre Mortalidade (Ministério da Saúde) | Nacional |

---

## 📊 Interpretação dos Resultados

**✅ Encontrado:**
```
✅ PESSOA POSSIVELMENTE EM ÓBITO - Registros encontrados em bases de dados
   Recomendação: Verificar detalhes nos portais oficiais
```
A pessoa foi localizada em ao menos uma base de dados de óbitos. Recomenda-se confirmar nos portais oficiais.

**❌ Não encontrado:**
```
❌ NÃO ENCONTRADO - Nenhum registro de óbito nas bases consultadas
   Nota: Ausência de registro não garante que a pessoa esteja viva
```
Nenhum registro encontrado. Pode haver atraso na atualização das bases.

---

## 🛠️ Requisitos

- Python 3.7 ou superior
- Conexão com internet
- Bibliotecas: `requests`, `beautifulsoup4`

---

## 🔗 Portais Oficiais

- [Portal Registro Civil](https://www.registrocivil.org.br/)
- [CNF Brasil](https://www.falecidosnobrasil.org.br/)
- [SIM DATASUS](http://sim.saude.gov.br/)

---

## ⚠️ Aviso Legal

Esta ferramenta consulta exclusivamente bases de dados **públicas** brasileiras. O uso deve estar em conformidade com a **LGPD (Lei Geral de Proteção de Dados Pessoais)** e demais legislações vigentes. Utilize apenas para fins legítimos e autorizados.

---

## 🐛 Problemas Comuns

**Erro: `ModuleNotFoundError: No module named 'requests'`**
```bash
sudo pip3 install requests beautifulsoup4
```

**Nenhum resultado encontrado:**
- Verifique a grafia do nome (sem abreviações)
- Tente adicionar CPF ou data de nascimento para refinar a busca
- Consulte diretamente os portais oficiais listados acima

---

*Desenvolvido para uso em investigações com Kali Linux.*
