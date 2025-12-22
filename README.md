# ❯❯❯❯ AI Chatbot with Custom Knowlegebase

[![Python](https://img.shields.io/badge/Python-3.10.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
<!-- [![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white)](https://www.docker.com/) -->
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/docs/transformers)


## 1 Project Overview
A highly practical use case for LLMs is interacting with your own documents using natural language. If your team keeps years worth of meeting notes, it is no longer a tedious half-day ordeal to go searching for the project requirements someone put together years ago. Ask the right question and an AI can pull that information out of messy documents in mere seconds. Need to vet a company's terms of service, but they only provide a 75 page document of legal-speak? An LLM can easily identify the relevant pieces of information you are looking for as well as point you to the right section of the source material if you need further clarification. 

There exists a multitude of use cases for AI systems that can draw from a custom knowledge base. In this project I set up a retrieval augmented generation (RAG) pipeline that can connect any LLM to your specific knowledge base. It takes care of processing documents and provides a clean interface to chat with the model.

Though many of us are used to using large models like ChatGPT, this project leverages smaller, locally run LLMs by default. These models can run on consumer grade hardware, removing API costs and preserving your privacy. Any documents you choose to upload stay on your local machine. No one but you has access to it.


## 2 Getting Started
This project requires that you have PostgreSQL installed on your machine. To create the PostgreSQL database:

```bash
sudo -u postgres psql postgres
psql
CREATE TABLE text_embeddings;
\c text_embeddings;
CREATE EXTENSION vector;
```
Once the database is set up, make sure to create a .env file and add your database url to it. Use the `test_db_conn.py` script to ensure you can connect to the database you created.

This projct uses a hyprid local environment with both Conda and Pip. Conda is better suited for dealing with heavier machine learning packages that use languages other than Python under the hood. For the packages that are not available in Conda's channels, pip works well. To set up the environment:

```bash
# if you don't have conda installed
sudo apt-get update && sudo apt-get upgrade
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
conda -V # check install worked

# once conda is intalled
conda env create -f environment.yaml
```


## 3 The RAG Pipeline
This project uses a PostgreSQL database with the `pgvector` extention to store embeddings. A locally stored corpus is processed and added to the database using the `populate_db.py`. This script chunks up each source into sentences before embedding each. The table strucure includes a primary key `id` for each sentence, its plain text representation, its embedding values, and the name of the source it came from. 

This approach has the advantange of keeping ideas isolated from one another, making it easier to find relevant information. Since we will intially match with only single senteces, the code grabs a few of the surrounding sentences as well to provide the model with more relevant context. By using a PostgreSQL database over a pure vector database, we can grab sequential sentences.

Finally, the retrieved context is appended to the user prompt which is then sent to an LLM to respond. This pipeline allows for relevant context to be found efficiently and with high accuracy. For specific metrics see section 5 below.

<!-- ```mermaid
graph LR
    %% Styles
    classDef storage fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef db fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef text fill:#ffffff,stroke:#333,stroke-dasharray: 5 5;

    %% Main Database Node (Shared Resource)
    Postgres[(PostgreSQL DB<br/>w/ pgvector)]:::db

    %% Subgraph: Data Ingestion
    subgraph Ingestion [Data Ingestion Pipeline]
        Raw[Raw Data / Docs]:::storage --> Chunk[Chunk into<br/>Sentences]:::process
        Chunk -->|Store ID, Content,<br/>Embedding, Source| Postgres
    end

    %% Subgraph: Query & Retrieval
    subgraph Retrieval [RAG Inference Pipeline]
        User(User Query):::storage --> Embed[Embed Query]:::process
        Embed -->|Vector: 0.2, ...| Search[Compare w/ DB]:::process
        
        %% Connection to DB
        Search <--> Postgres
        
        Search -->|Get Top K Matches| TopK[IDs: 3, 1, etc.]:::process
        TopK --> Expand[Get 'h' Surrounding<br/>Sentences]:::process
        
        %% Logic Note
        Logic(Range: i-h to i+h<br/>*No Duplicates!*):::text
        Logic -.- Expand

        Expand --> Context[Context + Query]:::storage
        Context --> LLM[LLM]:::process
        LLM --> Answer[Final Answer]:::storage
    end
``` -->

## 4 LLM Model Breakdowns
To create your own models in Ollama:
```ollama create <custom_name> -f ModelFile```
```ollama show --modelfile <model_name>```

## 5 Results