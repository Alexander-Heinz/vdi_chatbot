# Use a specific version of Python
FROM python:3.10-slim AS base

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the app files
COPY . .

# Command to run the application
CMD ["bash", "-c", "python index_docs.py && streamlit run app.py --server.port=8501 --server.enableCORS=false"]
