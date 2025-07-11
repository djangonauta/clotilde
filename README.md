# Projeto de Automação via Selenium do Tribunal de Justiça do Pará

## Instalação

Requisitos:

- Python 3.13
- Poetry 2.1

### Após clonar o projeto mude para o diretório de instalação e instale suas dependências via Poetry

```bash
poetry install --with dev # windows
poetry install --with dev,unix # linux
```

## Comandos de execução

Os seguintes comandos são executados no ambiente de desenvolvimento para tarefas especificas.

### Criar migrations para alterações feitas nos modelos

```bash
poetry run python ./dj.py makemigrations
```

### Aplicar as migrations para o banco de dados local Sqlite

```bash
poetry run python ./dj.py migrate
```

### Iniciar o servidor de desenvolvimento

```bash
poetry run python ./dj.py runserver
```

### Iniciar a aplicação via Pywebview

```bash
poetry run python ./main.py
```

### Construir o projeto para distribuição na plataforma Windows

```bash
poetry run pyinstaller .\app.spec --noconfirm
```
