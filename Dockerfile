FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Java (required for Spark)
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME automatically
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create logs and outputs folders
RUN mkdir -p logs outputs

# Run pipeline
CMD ["python", "run_pipeline.py"]