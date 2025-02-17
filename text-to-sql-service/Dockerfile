FROM python:3.10

COPY . .
RUN pip install pipenv && \
    pipenv install

EXPOSE 8001

CMD ["pipenv", "run", "serve"]
