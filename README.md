# sql-query-app
System that allows users to query a SQL database using natural language queries.

## Commiting code

If attempting to commit code, please use the following command standing at the root of
the repository:

`pip install pipx`
`pipx run pre-commit install`

This will install pre-commit hooks to ensure that the code is up to standards.

Additionally, you can run:

`pipx run pre-commit run --all-files`

In order to see a report of all the issues that need to be fixed.

## Running the app

You can run the command:

`docker compose up`

To build and run all the services required for the app, or you can run the following command:

`docker compose up --build`

If you want to build again the services and run the app