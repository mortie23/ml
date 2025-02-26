FROM python:3.10-bullseye
RUN pip install poetry==2.0.0
RUN poetry self add "keyrings.google-artifactregistry-auth"
RUN poetry self add poetry-plugin-export
ENTRYPOINT ["poetry"]