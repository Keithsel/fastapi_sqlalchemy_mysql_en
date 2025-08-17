# FastAPI SQLAlchemy MySQL

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Keithsel/fastapi_sqlalchemy_mysql_en)

## Local Development

* Python 3.10+
* MySQL 8.0+
* Redis (latest stable version recommended)

1. Install dependencies

   ```shell
   pip install -r requirements.txt
   ```

2. Create a database named `fsm` with `utf8mb4` encoding
3. Install and start Redis
4. Enter the backend directory

   ```shell
   cd backend
   ```

5. Create a `.env` file

   ```shell
   touch .env
   cp .env.example .env
   ```

6. Modify the configuration files `core/conf.py` and `.env` as needed
7. Database migration with [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

    ```shell
    # Generate migration file
    alembic revision --autogenerate
    
    # Apply migration
    alembic upgrade head
    ```

8. Start the FastAPI service

   ```shell
   # Help
   fastapi --help
   
   # Development mode
   fastapi dev main.py
   ```

9. Visit in browser: http://127.0.0.1:8000/docs

---

### Docker

1. Go to the directory containing the `docker-compose.yml` file and create the environment variable file `.env`

   ```shell
   cd deploy/docker-compose/
   
   cp .env.server ../../backend/.env
   ```

2. Run the one-click startup command

   ```shell
   # Use sudo if necessary
   docker-compose up -d --build
   ```

3. Wait for the command to complete automatically
4. Visit in browser: http://127.0.0.1:8000/docs

## Sponsor

If this project helps you, you can sponsor the author with some coffee beans as encouragement: [:coffee: Sponsor :coffee:](https://wu-clan.github.io/sponsor/)

## License

This project is licensed under the terms of the MIT License.
