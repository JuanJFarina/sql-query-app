FROM python:3.10

COPY . .
RUN pip install pipenv && \
    pipenv install

EXPOSE 8000

CMD ["pipenv", "run", "serve"]
