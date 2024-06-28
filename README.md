# DocumentSearchAI

This repository contains the source code for an innovative software created by Felipe Carillo that allows users to upload files and perform indexed searches using the Langchain library and language models (LLM). The project is structured in microservices and utilizes AWS, Elastic Search Cloud, and AWS Cloud technologies to ensure high scalability and performance.

## Overview

Our project offers the following features:

- **File Upload**: Allows users to upload various files.
- **Indexed Search**: Utilizes Elastic Search to index files and enable fast and precise searches.
- **LLM Integration**: Uses the Langchain library for advanced searches and intelligent responses.
- **Microservices**: Structured in microservices, ensuring scalability and ease of maintenance.
- **AWS Cloud**: Leverages AWS infrastructure to ensure availability and security.
- **Document Scanning**: Supports scanning documents and indexing them for search.
- **Vector Search**: Uses ChatGPT-4 and vector search for enhanced document retrieval.

## Architecture Diagram

<div style="display: flex; justify-content: space-between;">
  <div style="text-align: center;">
    <img src="https://github.com/FelipeCarillo/DocumentSearchAI/assets/63021830/3a8c95d0-5e15-4dbc-a5aa-62eb0e68f97c" alt="Production Diagram" width="400"/>
    <p><em>Image 1: Production Diagram</em></p>
  </div>
  <div style="text-align: center;">
    <img src="https://github.com/FelipeCarillo/DocumentSearchAI/assets/63021830/74a24c81-cd18-42d9-8171-a42e79e1c23e" alt="Local Diagram" width="400"/>
    <p><em>Image 2: Local Diagram</em></p>
  </div>
</div>

## How to Run Locally

Follow the steps below to set up and run the project locally in your development environment:

### Prerequisites

- Python
- React
- Docker

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/FelipeCarillo/DocumentSearchAI.git
cd DocumentSearchAI
```

### 2. Create the Virtual Environment

Create a virtual environment to isolate the project dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **Linux/MacOS**:
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the necessary dependencies using `pip`:

```bash
pip install -r requirements-dev.txt
```

### 4. Create the `.env` File

Create a `.env` file in the root directory of the project and configure the environment variables according to the `.env.example` file:

```bash
cp .env.example .env
```

Open the `.env` file and edit the values as needed.

### 5. Set Up the Frontend

Navigate to the `./frontend` directory and install the frontend dependencies:

```bash
cd frontend
npm install
```

Create a `.env` file in the `./frontend` directory and configure the environment variables according to the `.env.example` file:

```bash
cp .env.example .env
```

Edit the `.env` file as needed.

### 6. Start Docker Services

Navigate back to the root directory and start the required services using Docker Compose:

```bash
cd ..
docker-compose up -d
```

### 7. Run FastAPI

Start the FastAPI server:

```bash
python main.py
```

You can access the interactive API documentation in your browser at:

```
http://localhost:8000/docs
```

### 8. Start the Frontend

Navigate to the `./frontend` directory and start the React application:

```bash
cd frontend
npm start
```

## Technologies Used

The DocumentSearchAI project utilizes a variety of modern technologies to achieve its functionality and performance:

- **Langchain**: For advanced search and language model integration.
- **AWS (Amazon Web Services)**: To leverage cloud infrastructure for scalability and availability.
- **AWS CDK (Cloud Development Kit)**: For deploying infrastructure as code on AWS.
- **Continuous Deployment (CD)**: To automate the deployment process.
- **Python**: The primary programming language for backend development.
- **JavaScript**: Used for frontend development.
- **React**: For building the user interface of the application.
- **Docker**: To containerize the application for consistent environments across development, testing, and production.
- **GitHub**: For version control and collaborative development.
- **OpenAI**: To integrate with ChatGPT-4 for intelligent document search.
- **Elastic Search**: For indexing and searching documents efficiently.
- **MinIO**: To simulate AWS S3 for local development and testing.

These technologies collectively contribute to the robustness, scalability, and intelligence of the DocumentSearchAI project.

## Contribution

If you want to contribute to this project, feel free to open issues or pull requests. All help is welcome!

## License

This project is licensed under the [MIT License](LICENSE).
