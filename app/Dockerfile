FROM python:3.10-slim

WORKDIR /app

COPY . /app

COPY .env /app/.env

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["bash", "-c", "python index_docs.py && streamlit run app.py --server.port=8501 --server.enableCORS=false"]

# CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.enableCORS=false"]
