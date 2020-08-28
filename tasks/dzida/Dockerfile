FROM python:3.8.5-alpine3.12 AS runner

COPY server.py dzida.py secret.py recurse_interpreter.py /opt/

CMD ["python", "/opt/server.py"]
