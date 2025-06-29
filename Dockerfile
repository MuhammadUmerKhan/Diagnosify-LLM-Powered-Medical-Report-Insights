# Use compatible Python version
FROM python:3.10-slim

WORKDIR /app
COPY . /app/

# Install dependencies
RUN apt-get update && apt-get install -y build-essential cmake && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "Home.py"]