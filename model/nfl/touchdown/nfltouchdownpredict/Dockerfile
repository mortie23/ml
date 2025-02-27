FROM australia-southeast1-docker.pkg.dev/prj-xyz-shr-rep-0/rpo-bld-dkr-0/poetry-dkr AS base

WORKDIR /build
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
COPY ./ ./

RUN poetry install

FROM base AS model

# Enables passing of environment at build time with --build-arg
ARG env=nil
ENV env=$env
ARG project_id=nil
ENV project_id=$project_id
ENV NLTK_DATA=/usr/share/nltk_data

COPY --from=base /build /build

# These will be set by Vertex at time to include correct environment
#ENV AIP_STORAGE_URI=gs://bkt-herdml-dev-edap-herd-gnl-vertex-0/aiplatform-custom-training-yyyy-mm-dd-hh:mm:ss.ms/model
#ENV AIP_HEALTH_ROUTE=
#ENV AIP_PREDICT_ROUTE=
#ENV AIP_HTTP_PORT=

WORKDIR /model

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

# Copy the training code and configuration to the Docker image
COPY predict.py ./
COPY predict.yaml ./

# Sets up the entry point to invoke the predict end point
ENTRYPOINT ["./docker-entrypoint.sh"]