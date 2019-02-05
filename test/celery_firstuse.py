from celery import Celery
app=Celery('tasks',broker='amqp://guest:khb13719208594@localhost:5672/rabbitmqvhost')

@app.task
def add(x,y):
	return x+y