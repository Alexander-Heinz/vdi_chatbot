# vdi_chatbot
a chatbot for VDI


NEXT STEPS:
- Retrieval evaluation (ok) DOCUMENT!!!
- RAG evaluation (ok) DOCUMENT!!!
- Create streamlit UI
- Monitoring 
- Ingestion
- Containerizing (Docker)
    - make app run on local browser using only docker-compose


TODO: 2 points: Multiple retrieval approaches are evaluated, and the best one is used



### Problem description

VDI/VDE-IT is a German institute that supports innovation in technology, engineering, and digital transformation, particularly focusing on research, policy, and technology transfer.
The company has a FAQ-Page with frequently asked questions regarding project funding, and a rather static chatbot which can already answer questions based on keywords and multiple-choice options.

This project implements a chatbot powered by LLM (Large Language Model) AI technology designed to assist users by answering questions related to VDI/VDE-IT's focus areas in technology, engineering, and digital innovation. The chatbot uses a custom-built knowledge base, created by scraping the FAQ pages of the VDI/VDE-IT website, ensuring that the answers provided are accurate and relevant.

While a simple FAQ page offers static responses, this chatbot dynamically interprets and responds to user queries, handling more complex and nuanced questions. It enhances the user experience by delivering fast, personalized answers, making it easier to access information about VDI/VDE-IT's projects and services.


### Features:
Dynamic Q&A: Leverages the power of LLM to deliver more flexible and context-aware responses.
Knowledge Base: Built from VDI/VDE-IT's FAQs via web scraping.
Efficient Information Retrieval: Enables users to access relevant information quickly, without needing to search through static pages.

### Technologies Used:
- Python (for web scraping and LLM integration)
- Large Language Models (for intelligent question answering)
- Docker (for containerizing the application, TODO)
- Vector Database (TODO)

### How to Use:
Clone this repository and follow the setup instructions to deploy the chatbot locally or integrate it into a web application. The chatbot can be customized to suit different use cases or expanded with additional data sources.





![alt text](image.png)

Steps:

- Scrape relevant documents: FAQ with section names

- Index documents
    - simple indexing using ElasticSearch
    - advanced indexing using Vector Embeddings (sentence embeddings)

- Store embeddings in Vector Database (TODO)

- Create a search function for searching relevant documents based on queries: Relevant _FAQ Questions_ in relevant _Categories_ based on _user queries_ (Questions asked by users)
    - use ElasticSearch / Vector Search for sentence similiarity


- Retrieval evaluation
    - for each record (Answer) in the FAQ, generate 5 questions which possibly address this answer. 
    - Next, we input the questions into our search function to see if the desired answer would actually be among our top results
    - Use scoring algorithms to get an objective measure of retrieval quality
    - Problem: We did not verify that the questions are actually valid, since we created the "ground truth" using an LLM.

- Offline evaluation: LLM as a judge 

