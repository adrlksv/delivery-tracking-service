from flask import Flask, jsonify, request
from ..db.models import Order, Session
from tasks import update_order_status


app = Flask(__name__)


@app.route('/orders/<int:order_id>/status', methods=['GET'])
def get_order_status(order_id):
    session = Session()
    order = session.query(Order).filter_by(order_id=order_id).first()
    session.close()
    if order():
        return jsonify(order.to_dict())
    else:
        return jsonify({'message': 'Заказ не найден'}), 404
    

@app.route('/orders/<int:order_id>/update', methods=['POST'])
def update_order(order_id):
    session = Session()
    order = session.query(Order).filter_by(order_id=order_id).first()
    if order():
        data = request.get_json()
        if 'status' in data:
            order.status = data['status']
        if 'location' in data:
            order.location = data['location']
        session.commit()
        session.close()
        update_order_status.delay(order_id, order.status, order.location)
        return jsonify({'message': 'Статус заказа обновлен'})
    else:
        return jsonify({'message': 'Заказ не найден'}), 404
    

if __name__ == '__main__':
    app.run(debug=True)
