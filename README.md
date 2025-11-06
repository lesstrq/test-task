# Тестовое задание
## Установка
Склонируйте репозиторий на свою машину:
```
git clone https://github.com/lesstrq/test-task.git
```
Установите poetry, если он не установлен:
```
pip install poetry
```
В директории с проектом запустите установку зависимостей:
```
poetry install --no-root
```
Запустите сервер:
```
poetry run uvicorn main:app
```
Откройте браузер и перейдите в интерфейс Swagger UI: http://localhost:8000/docs

Реализовано 3 эндпоинта:
### /auth/register
Принимает:
- Имя пользователя
- Электронная почта
- Пароль
- Повтор пароля

Возвращает:
- JSON объект с информацией о созданном пользователе
- Ошибку 500, в случае ошибки при создании пользователя

Делает:
- Создает пользователя в базе данных

### /auth/login
Принимает:
- Имя пользователя или Электронная почта
- Пароль

Возвращает:
- access JWT
- Ошибку 401, в случае неверных данных пользователя

### /users/profile
Принимает:
- access JWT

Возвращает:
- JSON объект с информацией о текущем пользователе


Чтобы проверить работоспособность API можно, например, сделать следующим образом:

1. Создайте нового пользователя через /auth/register:
<img width="1782" height="750" alt="image" src="https://github.com/user-attachments/assets/a66c041b-bb2f-4d64-8b1f-13b0100145d0" />

2. Залогиньтесь, используя имя пользователя / почту и пароль:
<img width="1787" height="712" alt="image" src="https://github.com/user-attachments/assets/400a7688-e8f5-4339-bc02-28b1454d0291" />

3. Скопируйте access_token:
<img width="1748" height="620" alt="image" src="https://github.com/user-attachments/assets/4c243e6d-4fdd-49df-bfb5-752d62f5b2ea" />

4. Вернитесь на верх страницы и нажмите кнопку Authorize:
<img width="1868" height="430" alt="image" src="https://github.com/user-attachments/assets/4351408b-b73f-4de7-aeae-03e4865a880f" />

5. Вставьте скопированный токен в поле Value и нажмите Authorize:
<img width="821" height="363" alt="image" src="https://github.com/user-attachments/assets/659d5a6c-83ee-4156-9c04-413ec46230dc" />

6. Воспользуйтесь эндпоинтом /users/profile:
<img width="1807" height="1025" alt="image" src="https://github.com/user-attachments/assets/e8d44000-829e-47e0-a267-1b750d91b665" />



