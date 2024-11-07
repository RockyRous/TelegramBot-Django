Бидд контейнера
```bash
docker-compose build
```
Запуск контейнера
```bash
docker-compose up # -d
```
Терминал бд
```bash
docker exec -it postgres_db psql -U postgres -d postgres
```
Команды терминала бд:
```
Показать все заказы:
select * from store_order;

Показать только не выполненые заказы:
select * from store_order where status = 'pending';

```

Админка джанги
```
http://localhost:8000/admin/
```
Таблица с заказами:
```
http://localhost:8000/orders/
```