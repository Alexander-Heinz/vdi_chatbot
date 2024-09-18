# vdi_chatbot
a chatbot for VDI


![alt text](image.png)

Steps:

- Scrape relevant documents: FAQ with section names

- Index documents
    - simple indexing using ElasticSearch
    - advanced indexing using Vector Embeddings (sentence embeddings)

- Store embeddings in Vector Database

- Create a search function for searching relevant documents based on queries: Relevant _FAQ Questions_ in relevant _Categories_ based on _user queries_ (Questions asked by users)
    - use ElasticSearch and Vector Search