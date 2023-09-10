FROM python:3.11-slim AS requirements

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.5.1

COPY pyproject.toml poetry.lock /app/
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

FROM python:3.11-slim

WORKDIR /app

COPY --from=requirements /app/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN pip install .

ENTRYPOINT [ "python", "dyndns/cli.py" ]
