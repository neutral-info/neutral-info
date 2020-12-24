FROM python:3.7

# upgrade pip
RUN pip install --upgrade pip
RUN pip install pipenv

# set display port to avoid crash
ENV DISPLAY=:99

# facebook crawler need
WORKDIR /app
COPY . .
RUN pipenv install --system --deploy --ignore-pipfile

# run crawler bot every 2 hours
CMD ["python", "ptt", "--schedule_arg"] 