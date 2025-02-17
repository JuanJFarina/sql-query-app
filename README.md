# Text-to-SQL App

Microservices system that allows users to query a SQL database using natural language queries. It consists of PosgresDB, Database, Text-to-SQL, and UI services, and the tech
stack consists of:

- **Python**
- **Pre-commit** (Mypy, Pylint, Ruff)
- **Pydantic**
- **Streamlit**
- **LLMWare library with the Slim-SQL-Tool Model**
- **FastAPI**
- **SQLAlchemy**
- **Docker and Docker-Compose**

## Building and running the app

You will need to have installed Docker Desktop in your system.

Standing in the root of the repository, run the following command:

`docker compose up`

This will build the docker images and containers (if needed), and run the app.

You can then access each service independently at your localhost, and using the
appropriate port for each:

- Postgres Database: http://localhost:5432
- Database Service: http://localhost:8000
- Text-to-SQL Service: http://localhost:8001
- User Interface Service: http://localhost:8501

The UI will allow you to ask data-related questions using natural language (plain
english) using the text-to-sql service to convert the question to a SQL query, and then
using the database service to use the SQL query to retrieve the data.

An option to convert the result to natural language using an LLM is shown, but still not
implemented.

## Commiting code

In order to contribute and commit code, you'll need to have installed Python 3.10 and
Pipenv (as well as Docker Desktop).

Each service is developed as a standalone package inside its respective folder. You can
open a new window in your IDE inside a service's folder, install the dependencies, and
work isolately in one service.

When willing to commit and push code, please use the following commands standing at the
root of the repository to install pre-commit hooks:

```
pip install pipx
pipx run pre-commit install
```

After this, a pre-commit check will run every time you want to make a commit locally.
Additionally, you can run the following command to check your code ad-hoc:

`pipx run pre-commit run --all-files`

## About this development

Several decisions were made for this development:

- **Git branching**: since this was a small weekend project, no git branching strategy
was followed, and code was pushed directly to main branch. If this project would be to
grow I would create a dev branch, protect the main, add a CI/CD pipeline to run lints,
tests, and versioning on every PR to main, as well as deploying once merged in main.
- **Deployment**: for the sake of simplicity, the app has been built to be deployed
locally, using a monorepo structure. In order to scale this, different services should
be deployed independently, and a framework library should be created to facilitate
communication between services. If different teams would be to handle different
services, these should be developed by independent teams.
- **Architecture**: currently, the app is built using simple *Transaction Scripts*, but
if it were to scale, each service would require to implement more complex architectures
and patterns, like CQRS, Event-Sourcing, Repository design patterns, and more.
- **Text-to-SQL Model**: since development was made in an HP laptop with integrated
graphics, several issues were met attempting to run different models. The Slim-SQL-Tool
model was chosen due to its CPU-friendly performance.

## Next steps

- Refactor code to separete concerns and follow best practices.
- Add Pydantic models where missing.
- Add tests to cover 100% of the code.
- Add Loguru for enhanced logging.
- Migrate to Pantsbuild for better dependency management.
- Add a CI build pipeline for linting and testing.
- Refactor docker-related files to implement automatic re-starts and hot-reloads, as
well as more optimized images and build-times through caches, etc.
- Evaluate better text-to-sql models.
- Implement an LLM for natural language responses.
- Implement observability services with Grafana and Prometheus.
