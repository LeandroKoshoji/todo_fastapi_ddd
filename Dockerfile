# Use a imagem oficial do Python
FROM python:3.11-slim

# Instale as dependências necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo pyproject.toml e poetry.lock para o diretório de trabalho
COPY pyproject.toml poetry.lock* /app/

# Instale o Poetry
RUN pip install poetry

# Instale as dependências do projeto
RUN poetry install

# Copie todo o conteúdo do projeto para o diretório de trabalho
COPY . /app

# Exponha a porta que a aplicação irá rodar
EXPOSE 8000

# Defina o comando para rodar a aplicação
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
