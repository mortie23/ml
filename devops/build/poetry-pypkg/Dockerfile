FROM python:3.12-alpine
RUN pip install poetry==1.8.5
RUN poetry self add "keyrings.google-artifactregistry-auth"
RUN poetry self add poetry-plugin-export==1.8
ENTRYPOINT ["poetry"]