# Chatbot for hotel reservations

this agent chatbot use tools and modern mcp technology in order to interact with database and this also use an RAG(Retrieval Augmented Generation) method to improve its context and give the right answer to the final user.

# installation

if you want to run this project using your custom and local env you must follow this commands for the custom local installation, I am using poetry to handle all the packages and tools for python that we need here.

```bash
install poetry
cd rag-hotel
poetry init # --> this will create the pyprect.toml
poetry env use python3.11 # this will create venv
poetry install # --> this install all in env.
potery run python app/main.py
```

# run the local Qdrant vectorDB.

every time that we need to run the agent the vector DB, must need to
be run in the docker container as we are going to run this locally for now.

# three knowledge sources:

1️⃣ RAG
PDFs → policies, services, FAQ

2️⃣ PostgreSQL
rooms
reservations
guests
availability

3️⃣ Tools
create_reservation()
check_availability()
check_reservation()
register_checkin()

# example workflow with langGraph

START
 ↓
intent_classifier
 ↓
router
 ├─ rag_node
 ├─ availability_tool
 ├─ reservation_tool
 ↓
response_generator
 ↓
END

```bash
docker run -p 6333:6333 qdrant/qdrant

```

# requiriments.

poetry add \
 langchain \
 langchain-openai \
 langchain-community \
 sqlalchemy \
 psycopg2-binary \
 python-dotenv \
 pydantic \
 mcp

```

## Depeencies:

```

python
poetry

````

# Architecture of this project is

```bash
rag-hotel/
│
├── agent/
│   ├── router.py
│   ├── tools.py
│   └── workflow.py
│
├── database/
│   ├── connection.py
│   ├── queries.py
│   └── models.py
│
├── app/
│   ├── config.py
│   ├── llm.py
│   │
│   ├── rag/
│   │   ├── loader.py
│   │   ├── splitter.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   ├── retriever.py
│   │   └── pipeline.py
│   │
│   ├── main.py
│
├── data/
│   ├── pdf/
│   │   ├── fag_hotel.pdf
│   │   ├── information_hotel.pdf
│   │   ├── politicas.pdf
│   │   └── servicios.pdf
│   │
│   ├── html/        (más adelante)
│   └── markdown/    (más adelante)
│
├── .env
├── pyproject.toml
└── poetry.lock
````


## Final architecture(ideal)

```bash

                User
                 │
                 ▼
            Agent Router
        ┌────────┼─────────┐
        │        │         │
        ▼        ▼         ▼
      RAG     SQL DB     Actions
   (PDFs)   (Postgres)   (Tools)
        │        │         │
        └────────┴─────────┘
                 │
                 ▼
                LLM
                 │
                 ▼
               Answer

```
