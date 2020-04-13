FROM python:buster

RUN pip install pipenv

WORKDIR /app
COPY . .
RUN pipenv install --system --deploy --ignore-pipfile
CMD ["python", "ptt", "--schedule_arg"]