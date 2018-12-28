import datetime

from flask import Blueprint, request, render_template, session, jsonify

from app.models import House, User, Order
from utils.static_code import SUCCESS, COMMENT_IS_NULL

order_bp = Blueprint('order', __name__)


@order_bp.route('/create/', methods=['POST'])
def order_create():
    if request.method == 'POST':
        user_id = session['user_id']
        user = User.query.get(user_id)
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        house_id = request.form.get('house_id')
        house = House.query.filter(House.id==house_id).first()
        house_price = house.price
        begin_date = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        days = end_date - begin_date
        amount = days.days * house_price
        orders = Order()
        orders.house_price = house_price
        orders.user_id = user_id
        orders.house_id = house_id
        orders.begin_date = begin_date
        orders.end_date = end_date
        orders.days = days.days
        orders.amount = amount
        orders.status = 'WAIT_ACCEPT'
        user.orders.append(orders)
        user.add_update()
        return jsonify(SUCCESS)


@order_bp.route('/my_orders/', methods=['GET'])
def my_orders():
    if request.method == 'GET':
        return render_template('orders.html')


@order_bp.route('/my_orders/', methods=['POST'])
def orders_info():
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        orders = user.orders
        orders_info = [order.to_dict() for order in orders]
        return jsonify(SUCCESS, orders_info)


@order_bp.route('/lorders/', methods=['GET'])
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')


@order_bp.route('/lorders/', methods=['POST'])
def lorders_info():
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        houses = user.house
        lorder = []
        for house in houses:
            if house.orders:
                for order in house.orders:
                    lorder.append(order)
        lorders_info = [lorder_info.to_dict() for lorder_info in lorder]
        return jsonify(SUCCESS, lorders_info)


@order_bp.route('/up_order/', methods=['POST'])
def up_order():
    if request.method == 'POST':
        code = request.form.get('code')
        if code == '1':
            order_id = request.form.get('lorder_id')
            order = Order.query.get(order_id)
            order.status = 'WAIT_PAYMENT'
            order.add_update()
            return jsonify(SUCCESS)
        if code == '2':
            order_id = request.form.get('lorder_id')
            try:
                comment = request.form.get('comment')
            except:
                return jsonify(COMMENT_IS_NULL)
            if not comment:
                return jsonify(COMMENT_IS_NULL)
            order = Order.query.get(order_id)
            order.status = 'REJECTED'
            order.comment = comment
            order.add_update()
            return jsonify(SUCCESS)
        return jsonify({'code': 201, 'msg': '修改状态失败！'})


@order_bp.route('/order_status/', methods=['GET'])
def order_status():
    user = User.query.get(session['user_id'])
    houses = user.house
    lorder = []
    for house in houses:
        if house.orders:
            for order in house.orders:
                lorder.append(order)
    lorders_info = [lorder_info.to_dict() for lorder_info in lorder]

    return jsonify(SUCCESS, lorders_info)
