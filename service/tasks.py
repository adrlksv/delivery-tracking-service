from celery import Celery
from configs.config import BROKER_URL
from ..db.models import Order, Session


app = Celery('tasks', broker=BROKER_URL)


@app.task
def update_order_status(order_id, status, location):
    session = Session()
    order = session.query(Order).filter_by(order_id=order_id).first()
    if order():
        order.status = status
        order.location = location
        session.commit()
    session.close()