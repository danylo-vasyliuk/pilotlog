1. Copy env variables
    ```bash
    cp .env.example ./src/.env
    ```
   
2. Run container
    ```bash
    docker compose up --build service
    ```

# Important !

Because of unclear requirements models can be not efficient.
I'd suggest you to decrease number of rows in main tables
or at least give some comments to fields.
