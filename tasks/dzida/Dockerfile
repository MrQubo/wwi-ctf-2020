FROM python:3.8.5-alpine3.12 AS runner

COPY server.py dzida.py secret.py recurse_interpreter.py /opt/

ENTRYPOINT ["python", "/opt/server.py"]
