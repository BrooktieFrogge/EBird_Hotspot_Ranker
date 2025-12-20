# playwright base image for headless browser installing
FROM mcr.microsoft.com/playwright/python:v1.56.0-jammy
# set work dir
WORKDIR /app

# download dependencies
COPY requirements.txt server/
RUN pip install --no-cache-dir -r server/requirements.txt
# copy server files to /app/server
COPY . server/

EXPOSE 8000
# set python path
ENV PYTHONPATH=/app/server
# run server
# run server with configurable workers
CMD ["/bin/sh", "-c", "fastapi run server/main.py --port 8000 --workers ${WEB_CONCURRENCY:-1}"]
