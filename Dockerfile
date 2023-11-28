FROM python:3.10-slim AS builder

COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry==1.6.1 \
    && poetry export --with lint --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . ./

RUN mkdir /model_dills

CMD ["gunicorn", "main:app", "-c", "gunicorn.config.py"]
