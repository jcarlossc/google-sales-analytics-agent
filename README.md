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

### Pipeline Automatizado
✅ Carrega configurações</br>
✅ Configura logging</br>
✅ Cria conexão com Banco de Dados</br>
✅ Extrai dados</br>
✅ Padronização dados</br>
✅ Calcula métricas</br>
✅ Calcula estatísticas</br>
✅ Valida dados</br>
✅ Geração automática de relatórios</br>

### Qualidade dos Dados
✅ Detecção de valores ausentes</br>
✅ Validação estrutural</br>
✅ Identificação de duplicidades</br>
✅ Regras de negócio</br>
✅ Verificação de inconsistências</br>
✅ Verificação de valores negativos</br>
✅ Verificação de datas</br>

### Observabilidade
✅ Logging estruturado</br>
✅ Rastreamento de erros</br>
✅ Monitoramento do pipeline</br>

### Relatórios com Agente de IA
O sistema utiliza modelos generativos para:</br>
✅ Resumo estatístico automático</br>
✅ Interpretação dos indicadores</br>
✅ Geração de insights</br>
✅ Geração de relatórios textuais automatizados</br>

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
Relatórios textual Automáticos
```

## Estrutura do Projeto
```
google_sales_analysis_agent/
|
├── config/
│   ├── api_google.yaml
│   ├── db.yaml
│   ├── logging.yaml
│   └── paths.yaml
├── logs/
│     └── app.log
├── reports/
│     ├── indicadores.png
│     ├── top_products.png
│     ├── top_seller.png
│     └── Report.pdf
├── src/
│   └── google_sales_analysis_agent/
│         ├── agent_ia_google/
│         │     └── agent_ia_report.py
│         ├── database/
│         │     ├── connection.py
│         │     └── load_sales.py
│         ├── services/
│         │     ├── pipeline.py
│         │     ├── standardization.py
│         │     ├── validate.py
│         │     ├── metrics.py
│         │     ├── statistic.py
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

## Observabilidade
O projeto possui logging estruturado com rastreamento completo da execução.
Exemplo de log:
```
2026-06-06 15:39:05,873 - INFO - root - Logger configurado com sucesso.
2026-06-06 15:39:05,875 - INFO - google_sales_analytics_agent.services.pipeline - ### Iniciando pipeline de vendas. ###
2026-06-06 15:39:05,877 - INFO - google_sales_analytics_agent.services.pipeline - Criando conexão com banco.
2026-06-06 15:39:05,879 - INFO - google_sales_analytics_agent.database.connection - Iniciando criação da engine.
2026-06-06 15:39:06,467 - INFO - google_sales_analytics_agent.database.connection - Engine criada com sucesso.
2026-06-06 15:39:06,467 - INFO - google_sales_analytics_agent.services.pipeline - Carregando dados.
2026-06-06 15:39:06,468 - INFO - google_sales_analytics_agent.database.load_sales - Iniciando carregamento dos dados de vendas.
2026-06-06 15:39:07,182 - INFO - google_sales_analytics_agent.database.load_sales - 600 registros carregados.
2026-06-06 15:39:07,184 - INFO - google_sales_analytics_agent.services.pipeline - Padronizando dados.
2026-06-06 15:39:07,186 - INFO - google_sales_analytics_agent.services.standardization - Iniciando padronização dos dados.
2026-06-06 15:39:07,482 - INFO - google_sales_analytics_agent.services.standardization - 0 duplicatas removidas.
2026-06-06 15:39:07,484 - INFO - google_sales_analytics_agent.services.standardization - Padronização concluída.
2026-06-06 15:39:07,485 - INFO - google_sales_analytics_agent.services.pipeline - Validando dados.
2026-06-06 15:39:07,486 - INFO - google_sales_analytics_agent.services.validate - Iniciando validação de qualidade.
```

## Mode de Utilização
⚠️Observação: aplicações em Python, ou em outras linguagens, que utilizam banco de dados e APIs, nunca é recomendado deixar senhas diretamente no código (hardcoded password). Neste projeto, por motivos didáticos (para facilitar a reprodução), o arquivo de senha do Banco de Dados e a chave da api Google estão no arquivo YAML, mas essa abordagem é extremamente desaprovada em produção. 



1. Execute o XAMPP
* Caso não o tenha, baixe-o: <a href="https://www.apachefriends.org/pt_br/download.html">https://www.apachefriends.org/pt_br/download.html</a>
* Instale-o normalmente
* Execute o Painel de Controle
* Acione o Apache e o MySQL/MariaDB
* Ao lado do botão start/stop do MySQL/MariaDB, clique em Admin. Isso irá abrir a interface do MySQL/MariaDB no navegador
* Clique na aba importar e em escolher arquivo: o script está na raiz do projeto: ```script_database/loja_informatica.sql```, após isso, clique em importar no final da página
* O banco de Dados está com usuário ```root``` e senha vazia. O arquivo de configuração está em: ```config/db.yaml```

2. Com a linguagem Python instalada: <a href="https://www.python.org/downloads/" target="_blank">https://www.python.org/downloads/</a>
3. Instale o pipx: 
```
pip install pipx
```
4. Em seguida:
```
pipx ensurepath
```
5. E, por fim, o gerenciador Poetry:
```
pipx install poetry
```
6. Clone o repositório e acesse o diretório
```
git clone https://github.com/jcarlossc/google-sales-analytics-agent.git
cd google-sales-analytics-agent
```
7. Instalação das dependências:
```
poetry install
```
8. Para executar o projeto:
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
