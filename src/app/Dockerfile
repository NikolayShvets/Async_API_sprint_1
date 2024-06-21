FROM python:3.12

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update && pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /scripts /scripts
RUN chmod +x /scripts/entrypoint.sh

COPY . .

EXPOSE 8000

ENTRYPOINT [ "/scripts/entrypoint.sh" ]
