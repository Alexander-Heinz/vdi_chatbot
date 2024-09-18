# Use the official Elasticsearch image from Docker Hub
FROM docker.elastic.co/elasticsearch/elasticsearch:8.4.3

# Set environment variables for Elasticsearch
ENV discovery.type=single-node
ENV xpack.security.enabled=false

# Expose necessary ports
EXPOSE 9200 9300
