FROM python:3.8-buster

ARG YOUR_ENV

ENV YOUR_ENV=DEV \
  POETRY_VERSION=1.3.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /
COPY poetry.lock pyproject.toml app.py /

COPY /templates /templates

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev

CMD ["poetry", "run", "app.py"]