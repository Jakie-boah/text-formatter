from celery import Celery

app = Celery(
    "celery",
    broker="redis://redis:6379",
    backend="redis://redis:6379",
)

app.conf.broker_url = "redis://redis:6379"
app.conf.result_backend = "redis://redis:6379"

app.autodiscover_tasks()
