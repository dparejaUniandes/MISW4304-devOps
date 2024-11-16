FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# ENV DB_URL=postgresql://postgres:postgres@host.docker.internal:5432/postgres
# ENV DB_USER=postgres
# ENV DB_PASSWORD=postgres
# ENV DB_HOST=host.docker.internal
# ENV DB_PORT=5432
# ENV DB_NAME=postgres

EXPOSE 5000

CMD ["python", "application.py"]
