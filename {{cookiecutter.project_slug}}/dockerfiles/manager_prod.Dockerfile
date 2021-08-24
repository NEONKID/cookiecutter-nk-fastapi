# FROM python:3.8.5-slim
# MAINTAINER Saint

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /usr/src/app
COPY ./pyproject.toml .
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./manager ./manager
COPY ./shared ./shared

CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "manager.src.app:create_app()", "--access-logfile", "-"]