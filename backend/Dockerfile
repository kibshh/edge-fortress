FROM python:3.11-slim

# 1) Set working directory inside the image
WORKDIR /app

# 2) Copy dependency list first (better caching)
COPY requirements.txt .

# 3) Install deps in the image
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy app source last (so code changes don't bust earlier cache layers)
COPY app ./app

# 5) Document the port the app listens on (informational)
EXPOSE 8000

# 6) Start the server when the container runs
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]