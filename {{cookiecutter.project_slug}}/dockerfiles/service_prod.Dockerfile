FROM python:{{cookiecutter.project_python_version}}-slim
MAINTAINER {{cookiecutter.project_author_name}}

RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /usr/src/app
COPY ./pyproject.toml .
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./service ./service
COPY ./shared ./shared

CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "1", "-k", "worker.uvicorn.AppWorker", "service.src.app:create_app()", "--access-logfile", "-"]