## Pré-requisitos

- Python 3.12 ou superior
- Poetry (gerenciador de dependências)

## Instalação

1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/stract.git
cd stract
```

2. Instale as dependências usando Poetry
```bash
poetry install
```

3. Ative o ambiente virtual
```bash
poetry shell
```

4. Execute o servidor
```bash
poetry run python -m flask run
```

O servidor estará disponível em `http://localhost:5000`

## Endpoints Disponíveis

### GET /
Retorna informações pessoais do desenvolvedor
```json
{
    "nome": "Renan Nunes Bittencourt",
    "email": "programmerrnb@gmail.com",
    "LinkedIn": "https://www.linkedin.com/in/renan-nunes-bittencourt-26baa6203/"
}
```

### GET /{plataforma}
Retorna todos os anúncios da plataforma especificada em formato CSV
- Inclui todos os campos disponíveis para a plataforma
- Adiciona nome da conta que está veiculando o anúncio
- Formato: CSV com cabeçalhos apropriados

Exemplo:
```csv
Platform,Ad Name,Clicks,Account Name,...
Facebook,Some Ad,10,Account1,...
Facebook,Other Ad,20,Account2,...
```

### GET /{plataforma}/resumo
Retorna um resumo agregado por conta da plataforma
- Agrega dados numéricos por conta
- Mantém identificação da conta
- Campos de texto podem ficar vazios (exceto nome da conta)

Exemplo:
```csv
Platform,Ad Name,Clicks,Account Name,...
Facebook,,30,Account1,...
Facebook,,25,Account2,...
```

### GET /geral
Retorna todos os anúncios de todas as plataformas
- Inclui identificação da plataforma
- Nome da conta que veicula o anúncio
- Todos os campos disponíveis na API
- Calcula Cost per Click para Google Analytics

### GET /geral/resumo
Retorna um resumo agregado por plataforma
- Agrega dados numéricos por plataforma
- Campos de texto podem ficar vazios (exceto nome da plataforma)
- Métricas calculadas incluídas

## Funcionalidades Implementadas

- ✅ Consumo da API externa com autenticação
- ✅ Processamento de respostas paginadas
- ✅ Geração de relatórios em CSV
- ✅ Cálculo de Cost per Click para Google Analytics
- ✅ Agregação de dados por conta e plataforma
- ✅ Tratamento de erros
- ✅ Uso eficiente de campos específicos por plataforma

## Tecnologias Utilizadas

- Python 3.12
- Flask 3.1.0
- Requests 2.32.3
- Poetry para gerenciamento de dependências

## Dependências

As dependências são gerenciadas pelo Poetry e estão definidas no `pyproject.toml`:
- Flask: Framework web
- Requests: Cliente HTTP para consumo da API externa

## Autor

Renan Nunes Bittencourt
- Email: programmerrnb@gmail.com
- LinkedIn: https://www.linkedin.com/in/renan-nunes-bittencourt-26baa6203/

## Notas Adicionais

- A API utiliza autenticação via token Bearer
- Todos os endpoints são acessíveis via GET
- Os relatórios são gerados em tempo real
- Os dados são processados de forma eficiente para grandes volumes
- Implementação segue as melhores práticas de Python e Flask
