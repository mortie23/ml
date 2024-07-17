FROM python:3.11-slim

# Define build argument.
ARG SA_KEY_BASE64

# Create a temp key file with the service account key.
RUN echo $SA_KEY_BASE64 | base64 -d> /tmp/sa-artifact-registry.json

# Set the environment variable for the service account key.
ENV GOOGLE_APPLICATION_CREDENTIALS=/tmp/sa-artifact-registry.json

RUN mkdir -p /opt/hellofruit/templates

COPY app.py requirements.txt requirements-internal.txt /opt/hellofruit
COPY templates /opt/hellofruit/templates/
WORKDIR /opt/hellofruit

# System deps:
RUN pip install --no-cache-dir -U pip && \
  pip install --no-cache-dir -U keyrings.google-artifactregistry-auth
RUN pip install --no-cache-dir -U -r requirements.txt
RUN pip install --no-cache-dir -U -r requirements-internal.txt

# Remove the service acccount key file.
RUN rm /tmp/sa-artifact-registry.json

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "2",  "--threads", "100", "--timeout", "600", "app:app", "--reload"]