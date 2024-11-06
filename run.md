Запуск контейнера
```bash
docker-compose build; docker-compose up # -d
```
Терминал бд
```bash
docker exec -it postgres_db psql -U postgres -d postgres
```