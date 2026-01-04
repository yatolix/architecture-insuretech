# app/main.py
from ariadne import QueryType, make_executable_schema, graphql_sync
from ariadne.asgi import GraphQL
import json
import os
from typing import Dict, List, Optional

# Load test data from JSON files
def load_data():
    with open('clients.json', 'r') as f:
        clients_data = json.load(f)
    with open('documents.json', 'r') as f:
        documents_data = json.load(f)
    with open('relatives.json', 'r') as f:
        relatives_data = json.load(f)
    
    return clients_data, documents_data, relatives_data

# Load data
clients, documents, relatives = load_data()

# Create lookup dictionaries
documents_by_client: Dict[str, List] = {}
for doc in documents:
    client_id = doc.pop('clientId')
    if client_id not in documents_by_client:
        documents_by_client[client_id] = []
    documents_by_client[client_id].append(doc)

relatives_by_client: Dict[str, List] = {}
for rel in relatives:
    client_id = rel.pop('clientId')
    if client_id not in relatives_by_client:
        relatives_by_client[client_id] = []
    relatives_by_client[client_id].append(rel)

# Define resolvers
query = QueryType()

@query.field("client")
def resolve_client(_, info, id):
    for client in clients:
        if client["id"] == id:
            client_data = client.copy()
            client_data["documents"] = documents_by_client.get(id, [])
            client_data["relatives"] = relatives_by_client.get(id, [])
            return client_data
    return None

@query.field("clientDocuments")
def resolve_client_documents(_, info, id):
    return documents_by_client.get(id, [])

@query.field("clientRelatives")
def resolve_client_relatives(_, info, id):
    return relatives_by_client.get(id, [])

# Load schema from parent directory
schema_file = os.path.join(os.path.dirname(__file__), '..', 'schema.graphql')
with open(schema_file, 'r') as f:
    type_defs = f.read()

# Create executable schema
schema = make_executable_schema(type_defs, query)

# Create ASGI app
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)