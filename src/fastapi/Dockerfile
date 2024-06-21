FROM python:3.12

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml poetry.lock /opt/app/

RUN pip install --no-compile --upgrade pip \
 && pip install --no-compile poetry \
 && poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY /scripts /scripts
RUN chmod +x /scripts/entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/scripts/entrypoint.sh" ]
