FROM python:3.9

ENV TZ Asia/Taipei

# 可以輸出LOG
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

WORKDIR /app
COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "ptt", "--schedule_arg"]