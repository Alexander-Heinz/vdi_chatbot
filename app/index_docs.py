import pandas as pd
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm
load_dotenv()

# Initialize sentence transformer model
# model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

INDEX_NAME = "faq_index"

# Load the FAQ data
df = pd.read_csv('../data/faqs.csv')
df = df.drop_duplicates(subset=['Question', 'Answer', 'Category'], keep='first')

questions = df['Question'].tolist()
answers = df['Answer'].tolist()
categories = df['Category'].tolist()

# Generate embeddings for questions with progress bar
def generate_embeddings(questions):
    embeddings = []
    for question in tqdm(questions, desc="Generating embeddings"):
        embedding = model.encode(question)
        embeddings.append(embedding)
    return embeddings


embeddings = generate_embeddings(questions)

# Elasticsearch Setup
# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# delete index if available
es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)

# Define the index mapping to support dense vectors
index_mapping = {
    "mappings": {
        "properties": {
            "question": {"type": "text"},
            "answer": {"type": "text"},
            "category": {"type": "keyword"},
            "question_embedding": {
                "type": "dense_vector",
                "dims": 384  # Adjust this according to your model output size
            }
        }
    }
}

# Create an index
es.indices.create(
    index=INDEX_NAME,
    mappings=index_mapping["mappings"],  # Use individual parameters
    ignore=400
)

# Prepare data for Elasticsearch indexing
def generate_documents(questions, answers, categories, embeddings):
    for question, answer, category, embedding in zip(questions, answers, categories, embeddings):
        yield {
            "_index": "faq_index",
            "_source": {
                "category": category,
                "question": question,
                "answer": answer,
                "question_embedding": embedding.tolist()  # Convert to list for JSON storage
            }
        }

# Index data in Elasticsearch
helpers.bulk(es, generate_documents(questions, answers, categories, embeddings))

print("Data added to Elasticsearch successfully.")

