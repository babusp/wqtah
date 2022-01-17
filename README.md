## Wqtah-Backend

# Prerequisite:

    * Python 3.8+
    * PostgreSQL 12.2+
    
1. Project setup, database setup and env set up

     * Pull from git repository 
     * Create virtual environment and apply to project
     * Run command for project dependency:
        ```
        $ pip install -r requirements.txt
        ```
     * Run command for project dependency:
        ```
            rename file .env.sample to .env and put the values
        ```
     * DB migrations:
        ```
        $ python manage.py migrate
        ```
     * Initial data save in DB:
        ```
        $ python manage.py loaddata fixtures/*.json
        ```
          
2. Run server:
    ```
     $ python manage.py runserver
    ```
3. Run Celery for send notification using rabbitmq queue
     ```
     $ celery -A wqtah worker --loglevel=info
    ```
