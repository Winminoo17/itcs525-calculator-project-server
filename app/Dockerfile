FROM python:3.13.5-bookworm

WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "5000"]