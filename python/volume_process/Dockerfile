FROM python:3.9

ENV TZ Asia/Taipei

# upgrade pip
RUN pip install --upgrade pip
RUN pip install pipenv

# 可以輸出LOG
ENV PYTHONUNBUFFERED 1

# set display port to avoid crash
ENV DISPLAY=:99

# facebook crawler need
WORKDIR /app
COPY . .

# install from Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile

# run crawler bot every 2 hours
CMD ["python", "volume_process", "--schedule_arg"] 