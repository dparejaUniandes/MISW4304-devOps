FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install newrelic
# ENV DB_URL=postgresql://postgres:postgres@host.docker.internal:5432/postgres
# ENV DB_USER=postgres
# ENV DB_PASSWORD=postgres
# ENV DB_HOST=host.docker.internal
# ENV DB_PORT=5432
# ENV DB_NAME=postgres

ENV NEW_RELIC_APP_NAME="devops-entrega-4"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=897b309cef4e49725994e707de6e6274FFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info

EXPOSE 5000

ENTRYPOINT [ "newrelic-admin", "run-program" ]

CMD ["python", "application.py"]