FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements/ /app/requirements/
RUN pip install \
        --disable-pip-version-check \
        --no-cache-dir \
        --requirement /app/requirements/production.txt
COPY . /app

WORKDIR /app
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "project.serverless.handler" ]
