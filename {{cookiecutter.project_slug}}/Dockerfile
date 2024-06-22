FROM python:3.12-slim-bookworm
WORKDIR /app
COPY requirements/ /app/requirements/
RUN pip install \
        --disable-pip-version-check \
        --no-cache-dir \
        --requirement /app/requirements/production.txt
COPY . /app
ARG SENTRY_RELEASE
RUN echo "$SENTRY_RELEASE" > .sentry-release

WORKDIR /app
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "project.serverless.handler" ]
