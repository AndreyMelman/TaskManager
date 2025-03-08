FROM python:3.12-slim

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY ./app /code/app

WORKDIR /code/app

EXPOSE 8000

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
