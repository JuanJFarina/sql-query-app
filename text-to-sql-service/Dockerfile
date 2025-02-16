FROM python:3.10

COPY . .
RUN pip install pipenv && \
    pipenv install

EXPOSE 8501

CMD ["pipenv", "run", "serve"]
