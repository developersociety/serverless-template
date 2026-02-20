FROM python:3.14-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/usr/local
COPY pyproject.toml uv.lock /app/
RUN uv sync \
    --frozen \
    --no-cache \
    --compile-bytecode \
    --group production \
    --no-dev
COPY . /app
ARG SENTRY_RELEASE
RUN echo "$SENTRY_RELEASE" > .sentry-release

WORKDIR /app
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "project.serverless.handler" ]
