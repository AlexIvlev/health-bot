# Health bot
Telegram-bot для слежения за здоровьем.

## Развертывание проекта
```
cp env-example .env
```
- Прописать в .env необходимые токены
- Выполнить команду
```
docker-compose up -d
```

## Дополнительная функциональность
- Реализована визуализация достижения целей по воде и калориям в виде столбиковых диаграмм
- Реализована выдача рекомендаций на основании активности и целей по воде и калориям
- К определению калорийности через сервис OpenFoodFacts была добавлена возможность задания калорийности вручную, если продукт не найден в базе сервиса

## Демонстрация работы бота
### Начало работы
![start.png](screenshots/start.png)

### Работа с профилем

![set_profile.png](screenshots/set_profile.png)

![profile.png](screenshots/profile.png)

![edit_profile.png](screenshots/edit_profile.png)

### Логирование воды, еды и тренировок

![log_water.png](screenshots/log_water.png)

![log_food.png](screenshots/log_food.png)

![log_workout.png](screenshots/log_workout.png)

### Прогресс по воде и калориям
![check_progress.png](screenshots/check_progress.png)

### Визуализация достижения целей
![visualize_goals.png](screenshots/visualize_goals.png)

### Получение рекомендаций
![get_recommendations.png](screenshots/get_recommendations.png)

## Демонстрация деплоя на онлайн-сервер
