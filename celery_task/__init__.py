from celery import Celery

# include:导入指定的任务模块
# 这一次创建 app，并没有直接指定 broker(消息中间件来接收和发送任务消息) 和 backend(存储结果)。而是在配置文件中。
app = Celery(
    'demo',
    include=[
        'celery_task.image_task',
    ]
)
# 通过Celery 实例加载配置模块
app.config_from_object(
    'celery_task.celeryconfig',
)
