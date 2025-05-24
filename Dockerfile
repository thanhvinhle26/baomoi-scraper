FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless libc6 libc6-dev libc-dev && \
    rm -rf /var/lib/apt/lists/*

# 2. Find and set JVM path (critical fix)
RUN JVM_PATH=$(find /usr/lib/jvm -name 'libjvm.so' | head -1) && \
    echo "Found JVM at: $JVM_PATH" && \
    echo "export JVM_PATH=$JVM_PATH" >> /etc/profile.d/java.sh && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >> /etc/profile.d/java.sh

COPY requirements.txt .
COPY VnCoreNLP-1.2.jar /app/vncorenlp/VnCoreNLP-1.2.jar
COPY models /app/vncorenlp/models/
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV JVM_PATH=/usr/lib/jvm/java-17-openjdk-amd64/lib/server/libjvm.so

RUN mkdir -p /app/output

ENTRYPOINT ["bash", "-c", "source /etc/profile.d/java.sh && python run_scraper.py"]