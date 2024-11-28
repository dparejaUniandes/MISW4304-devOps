FROM python:3.10-slim
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

ENV NEW_RELIC_APP_NAME="devops"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=C173B6F58F7BEB512A76F13BD10B97B966B03D49F2A4D0C28907E13A0EDD70E3
ENV NEW_RELIC_LOG_LEVEL=info

EXPOSE 5000

ENTRYPOINT [ "newrelic-admin", "run-program" ]

CMD ["python", "application.py"]