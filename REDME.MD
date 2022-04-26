Тестовый проект основной целью которого выпольнить задачу:
Спроектировать и разработать сервис, который по заданным правилам запускает рассылку по списку клиентов.
Для запуска проекта вам необходимо сделать следующее:

Копируем проект
git clone git@github.com:myxahev/Fabric_test_task.git

Установка зависимостей
pip install -r requirements.txt

Создать контейнер с Redis для выполнения задач Celery
docker run -it -p 6379:6379 redis

Запуск Celery worker и beat
celery -A Fabric_test_task worker -l info
celery -A Fabric_test_task beat -l info

