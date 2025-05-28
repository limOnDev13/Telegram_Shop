# Telegram_Shop
A telegram bot that provides the functionality of an online store. It includes a catalog with pagination, a shopping cart, a payment (test), an FAQ and an admin panel on Django. Test task from BOTTEC.

---

## Description
Online store in telegram bot. To start communication, run the /start command. The store consists of a catalog with a tree structure of categories, product browsing, and a shopping cart. A UKassa and a Django admin panel are linked to the store. The data is stored in Postgresql. Docker files are collected for the convenience of deployment.

## Setup and launch
To demonstrate how the application works, it is enough to assemble docker containers with 
the ```docker compose up --build``` command. To fill the database, you can upload a fixture fixture.json. After that, you can go to the admin panel with the data username: admin; password: admin; email: admin@admin.admin

If the application is running locally via docker (with nginx), 
then the application will work by url. http://127.0.0.1:8000/admin
___

## Technologies
- aiogram
- Django
- Postgres
- Docker
- Nginx

