<div align="center">

# Agente de IA Google para Relatório de Análise de Vendas

### Pipeline Analítico de Vendas  

Pipeline automatizado para análise de vendas utilizando Python, MySQL e agentes de IA para geração automática de relatórios analíticos.

O projeto foi desenvolvido com foco em engenharia de dados, qualidade dos dados, automação analítica e integração com modelos generativos para transformar dados 
transacionais em insights acionáveis.

<img src="https://img.shields.io/badge/Python-276DC3?style=for-the-badge&logo=r&logoColor=white" />
<img src="https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-success?style=for-the-badge" />
<img src="https://img.shields.io/badge/LICENSE-MIT-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/TESTS-pytest-orange?style=for-the-badge" />

</div>

---

## Objetivos

* Automatizar extração e preparação dos dados
* Centralizar regras de qualidade de dados
* Criar pipeline modular e reutilizável
* Gerar relatórios analíticos automáticos utilizando IA
* Aplicar boas práticas de engenharia de dados

## Principais Funcionalidades

* Integração com Banco MySQL
* conexão via SQLAlchemy
* gerenciamento de conexões
* leitura automatizada das tabelas
### Pipeline Automatizado
* carga dos dados
* padronização
* validação
* enriquecimento
* geração automática de relatórios
### Qualidade dos Dados
* detecção de valores ausentes
* validação estrutural
* identificação de duplicidades
* regras de negócio
* verificação de inconsistências
### Observabilidade
* logging estruturado
* rastreamento de erros
* monitoramento do pipeline
### Relatórios com Agente de IA
O sistema utiliza modelos generativos para:
* resumo estatístico automático
* interpretação dos indicadores
* identificação de padrões
* geração de insights
* identificação de riscos dos dados
* geração de relatórios textuais automatizados

## Arquitetura Geral
```
Banco MySQL
     ↓
Conexão SQLAlchemy
     ↓
Carga dos Dados
     ↓
Padronização
     ↓
Validação
     ↓
Métricas / Estatísticas
     ↓
Agente de IA
     ↓
Relatórios Automáticos
```

## Estrutura do Projeto
```
google_sales_analysis_agent/
|
├── config/
│   ├── db.yaml
│   ├── logging.yaml
│   └── paths.yaml
├── logs/
│     └── app.log
├── reports/
│     └── Report.pdf
├── src/
│   └── google_sales_analysis_agent/
│         ├── database/
│         │     ├── connection.py
│         │     └── load_sales.py
│         ├── services/
│         │     ├── pipeline.py
│         │     ├── standardization.py
│         │     ├── validate.py
│         │     ├── metrics.py
│         │     └── ai_reports.py
│         ├── utils/
|         |     ├── load_config/
│         │     |      └── loader_config.py
│         │     └── loggers/
|         |          └── logger.py
│         └── main.py
├── LICENSE
├── pyproject.toml
├── poetry.lock
├── README.md
└── .gitignore
```

## Estrutura dos Dados

Tabela utilizada no banco:
| Campo |	Descrição |
| ----- | --------- |
|vendas_id | identificador da venda |
|data_venda |	data da venda |
|quantidade_vendida |	quantidade comercializada |
|produto | produto vendido |
|valor_compra	| custo do produto |
|valor_venda | preço de venda |
|vendedor |	responsável pela venda |

## Mode de Utilização

1. Com a linguagem Python instalada: <a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a>
2. Instale o pipx: 
```
pip install pipx
```
3. Em seguida:
```
pipx ensurepath
```
4. E, por fim, o gerenciador Poetry:
```
pipx install poetry
```
5. Clone o repositório e acesse o diretório
```
git clone https://github.com/jcarlossc/google-sales-analytics-agent.git
cd google-sales-analytics-agent
```
6. Instalação das dependências:
```
poetry install
```
7. Para executar o projeto:
```
poetry run vendas
```

## Licença
Este projeto está licenciado sob MIT License.

## Desenvolvedor focado em:

- Data Engineering
- Analytics
- R Programming
- Python Programming
- Automação de processos
- Engenharia de Software

## Contato
* Autor: Carlos da Costa
* Recife, PE - Brasil
* Telefone: +55 81 99712 9140
* Telegram: @jcarlossc
* Blogger linguagem R: https://informaticus77-r.blogspot.com/
* Blogger linguagem Python: https://informaticus77-python.blogspot.com/
* Email: jcarlossc1977@gmail.com
* LinkedIn: https://www.linkedin.com/in/carlos-da-costa-669252149/
* GitHub: https://github.com/jcarlossc
* Kaggle: https://www.kaggle.com/jcarlossc/
* Twitter/X: https://x.com/jcarlossc1977
