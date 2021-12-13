FROM python:3.9

COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install --system

EXPOSE 5000

CMD [ "python", "run.py"]