# Meu Projeto de Busca Inteligente

Este repositório contém o código fonte de um software inovador que permite aos usuários fazer o upload de arquivos e realizar buscas indexadas utilizando a biblioteca Langchain e modelos de linguagem (LLM). O projeto está estruturado em microserviços e faz uso das tecnologias AWS, Elastic Search Cloud e AWS Cloud para garantir alta escalabilidade e performance.

## Visão Geral

Nosso projeto oferece as seguintes funcionalidades:

- **Upload de Arquivos**: Permite que os usuários façam o upload de arquivos diversos.
- **Busca Indexada**: Utiliza Elastic Search para indexar os arquivos e permitir buscas rápidas e precisas.
- **Integração com LLM**: Usa a biblioteca Langchain para realizar buscas avançadas e fornecer respostas inteligentes.
- **Microserviços**: Estruturado em microserviços, garantindo escalabilidade e facilidade de manutenção.
- **AWS Cloud**: Aproveita a infraestrutura da AWS para garantir disponibilidade e segurança.

## Diagrama da Arquitetura

![Diagrama da Arquitetura](caminho/para/imagem.png)

## Como Rodar Localmente

Siga os passos abaixo para configurar e rodar o projeto localmente em seu ambiente de desenvolvimento:

### 1. Criar o Ambiente Virtual

Crie um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **Linux/MacOS**:
  ```bash
  source venv/bin/activate
  ```

### 2. Instalar Dependências

Instale as dependências necessárias utilizando o `pip`:

```bash
pip install -r requirements.txt
```

### 3. Criar o Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente de acordo com o arquivo `.env.example`:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e edite os valores conforme necessário.

### 4. Rodar o Docker Compose

Inicie os serviços necessários utilizando o Docker Compose:

```bash
docker-compose up -d
```

### 5. Rodar o FastAPI

Execute o arquivo `main.py` para iniciar o servidor FastAPI:

```bash
python main.py
```

### 6. Acessar a Documentação

Acesse a documentação interativa da API através do navegador em:

```
http://localhost:8000/docs
```

## Contribuição

Se você deseja contribuir com este projeto, sinta-se à vontade para abrir issues ou pull requests. Toda ajuda é bem-vinda!

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE). 