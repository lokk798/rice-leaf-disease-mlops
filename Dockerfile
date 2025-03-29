FROM python:3.11.5

RUN apt-get update -y && \
    apt-get install awscli -y && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Copy project files into the container
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]