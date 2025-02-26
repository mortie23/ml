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

COPY --from=base /build /build

WORKDIR /model

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

# Copy the training code and configuration to the Docker image
COPY train.py ./
COPY train.yaml ./

# Sets up the entry point to invoke the training code
ENTRYPOINT ["./docker-entrypoint.sh"]