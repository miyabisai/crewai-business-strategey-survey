FROM python:3.11.8-slim

EXPOSE 8501

RUN apt-get update 
RUN apt-get install -y build-essential software-properties-common git 
RUN pip install --upgrade pip
RUN rm -rf /var/lib/apt/lists/
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["streamlit", "run", "main.py"]

