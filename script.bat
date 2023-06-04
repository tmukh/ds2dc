REM Build the Docker image
docker build -t postgrestest --file Dockerfile1.dockerfile .

REM Run the Docker container
docker run --name tabular_container -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=csvs -d postgrestest

REM Wait for the PostgreSQL server to initialize
:waitloop
timeout /t 2 >nul
docker exec tabular_container psql -h localhost -U postgres -c "\l" >nul 2>&1
if %errorlevel% neq 0 (
  echo Waiting for the PostgreSQL server to initialize...
  goto waitloop
)

REM Execute the script once the PostgreSQL server is ready
docker exec tabular_container sh -c "./populate_csvs.sh"
    