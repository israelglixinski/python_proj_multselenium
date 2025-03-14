# Python Proj MultiSelenium

## Sobre o Projeto
O **Python Proj MultiSelenium** é um sistema de automação que utiliza Selenium para executar tarefas em múltiplos computadores simultaneamente. O projeto é dividido em dois módulos principais:

- **API**: Responsável por fornecer as informações necessárias para a execução das automações.
- **Cliente**: Consome os dados da API e executa a automação Selenium nas máquinas configuradas.

O projeto permite configurar diferentes tipos de rotinas e lotes para acelerar atividades, além de agendar execuções conforme necessidade.

## Funcionalidades
✅ Suporte a múltiplos computadores para execução simultânea das rotinas.  
✅ Estrutura modular dividida entre API e cliente.  
✅ Configuração flexível para diferentes tipos de rotinas.  
✅ Execução agendada para horários específicos.  
✅ Possibilidade de compilação do cliente para `.exe` ou execução direta via Python.  

## Estrutura do Projeto
```
python_proj_multselenium/
│── main.py                # Gerenciador principal
│
├── api/                   # Módulo da API
│   ├── app.py             # Ponto de entrada da API
│   ├── banco.py           # Gerenciamento do banco de dados
│   ├── banco.db           # Arquivo do banco de dados SQLite
│   ├── alimentador.py     # Alimentação de dados para a API
│   ├── creates.sql        # Estrutura do banco de dados
│   ├── __init__.py        # Modularização
│   ├── __main__.py        # Entrada do módulo API
│
├── client/                # Módulo do Cliente
│   ├── exec.py            # Script de execução da automação
│   ├── centro_acoes.py    # Gerenciador de ações Selenium
│   ├── configs.json       # Arquivo de configurações
│   ├── x__init__.py       # Modularização
│   ├── x__main__.py       # Entrada do módulo Cliente
```

## Requisitos
- Python 3.8+
- Selenium
- Flask (para a API)
- SQLite (banco de dados integrado)

## Instalação
### 1. Clonar o Repositório
```sh
git clone https://github.com/seu-usuario/python_proj_multselenium.git
cd python_proj_multselenium
```

### 2. Instalar Dependências
```sh
pip install -r requirements.txt
```

### 3. Iniciar a API
```sh
cd api
python app.py
```

### 4. Iniciar o Cliente
```sh
cd client
python exec.py
```

## Configuração
O arquivo `configs.json` dentro do diretório `client/` armazena as configurações necessárias para a execução das rotinas. Certifique-se de ajustá-lo conforme necessário.

## Compilação para Executável
Para transformar o cliente em `.exe`:
```sh
pip install pyinstaller
pyinstaller --onefile exec.py
```
O executável estará disponível na pasta `dist/`.

## Contribuição
Contribuições são bem-vindas! Para sugerir melhorias ou corrigir bugs, abra uma issue ou envie um pull request.

## Licença
Este projeto está licenciado sob a licença MIT.
