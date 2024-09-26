import pandas as pd
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm
import os
import time
# Load environment variables
load_dotenv()

# Initialize Elasticsearch client and model



es_client = Elasticsearch(os.getenv('ELASTICSEARCH_URL', 'http://elasticsearch_app:9200')) # http://localhost:9200

# Wait for Elasticsearch to be available
for i in range(10):  # Try 10 times
    try:
        if es_client.ping():
            print("Elasticsearch is available!")
            break
    except ConnectionError:
        print("Elasticsearch is not available yet, waiting...")
        time.sleep(5)  # Wait for 5 seconds before retrying
else:
    print("Could not connect to Elasticsearch after several attempts.")
    exit(1)


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

INDEX_NAME = "faq_index"
# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_dir)
# Load the FAQ data
documents = pd.read_json('./app_data/documents-with-ids.json')
documents = documents.to_dict(orient='records')

# Check if the index exists, delete it to avoid conflicts
if es_client.indices.exists(index=INDEX_NAME):
    es_client.indices.delete(index=INDEX_NAME)

# Define the index settings with mappings for the fields and vectors
index_mapping = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "Category": {"type": "keyword"},
            "Subcategory": {"type": "keyword"},  # Added Subcategory
            "URL": {"type": "keyword"},         # Added URL
            "Question": {"type": "text"},
            "Answer": {"type": "text"},
            "id": {"type": "keyword"},
            "question_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "answer_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
            "question_answer_vector": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            }
        }
    }
}

# Create the new index
es_client.indices.create(index=INDEX_NAME, body=index_mapping)

# Prepare documents for bulk upload to Elasticsearch
bulk_data = []
for doc in tqdm(documents):
    # Access the Question and Answer from your document
    question = doc.get('Question', '')
    answer = doc.get('Answer', '')
    
    # Combine Question and Answer for concatenated vector
    question_answer = question + ' ' + answer
    
    # Generate embeddings for each field
    doc['question_vector'] = model.encode(question).tolist()
    doc['answer_vector'] = model.encode(answer).tolist()
    doc['question_answer_vector'] = model.encode(question_answer).tolist()

    # Prepare document for bulk indexing
    bulk_data.append({
        "_index": INDEX_NAME,
        "_id": doc['id'],
        "_source": {
            "Category": doc.get('Category', ''),
            "Subcategory": doc.get('Subcategory', ''),  # Add Subcategory field
            "URL": doc.get('URL', ''),                  # Add URL field
            "Question": question,
            "Answer": answer,
            "question_vector": doc['question_vector'],
            "answer_vector": doc['answer_vector'],
            "question_answer_vector": doc['question_answer_vector']
        }
    })

# Bulk indexing into Elasticsearch
helpers.bulk(es_client, bulk_data)

print(f"Successfully indexed {len(bulk_data)} documents into Elasticsearch")
