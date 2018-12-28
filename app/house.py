import datetime
import os

from flask import Blueprint, request, render_template, jsonify, session

from app.models import User, House, HouseImage, Facility, Area, Order
from utils.functions import is_login
from utils.settings import MEDIA_PATH
from utils.static_code import USER_NOT_LOGIN, SUCCESS

house_bp = Blueprint('house', __name__)


@house_bp.route('/index/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':

        return render_template('index.html')
    if request.method == 'POST':
        try:
            user = User.query.get(session['user_id'])
            phone = user.phone
        except:
            user= ''
        if not user:
            return jsonify(USER_NOT_LOGIN)
        return jsonify({'code': 200,
                        'msg': '请求成功',
                        'data': {
                                    'phone': phone
                        }})


@house_bp.route('/new_house/', methods=['GET'])
@is_login
def new_house():
    if request.method == 'GET':
        return render_template('newhouse.html')


@house_bp.route('/new_house/', methods=['POST'])
def new_house_facility():
    if request.method == 'POST':
        facilitys = Facility.query.all()
        areas = Area.query.all()
        data = [facility.to_dict() for facility in facilitys]
        area_data = [area.to_dict() for area in areas]
        return jsonify({'code': 200, 'msg': '请求成功', 'data':data, 'area_data': area_data})


@house_bp.route('/create_house/', methods=['POST'])
def create_house():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        area_id = request.form.get('area_id')
        address = request.form.get('address')
        room_count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        facility = request.form.getlist('facility')
        user = User.query.get(session['user_id'])
        house = House()
        house.user_id = user.id
        house.title = title
        house.price = price
        house.area_id = area_id
        house.address = address
        house.room_count = room_count
        house.acreage = acreage
        house.unit = unit
        house.capacity = capacity
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days

        for f in facility:
            house.facilities.append(Facility.query.get(f))
        house.add_update()
        return jsonify({'code': 200, 'house_id': house.id})


@house_bp.route('/up_image/', methods=['POST'])
def up_image():
    if request.method == 'POST':
        image = request.files.get('house_image')
        house_id = request.form.get('house_id')
        image.save(os.path.join(os.path.join(MEDIA_PATH, 'pic'), image.filename))
        house = House.query.filter(House.id==house_id).first()
        house_image = HouseImage()
        house_image.house_id = house_id
        house_image.url = image.filename
        house.index_image_url = image.filename
        house.add_update()
        house_image.add_update()
        return jsonify({'code': 200})


@house_bp.route('/detail/<int:id>/', methods=['GET'])
def detail(id):
    if request.method == 'GET':
        return render_template('detail.html')


@house_bp.route('/detail/', methods=['POST'])
def detail_house():
    if request.method == 'POST':
        house_id = request.form.get('house_id')
        house = House.query.get(house_id)
        booking = 1
        try:
            if house.user_id == session['user_id']:
                booking = 0
        except:
            booking = 1
        return jsonify(SUCCESS, house.to_full_dict(), {'booking': booking})


@house_bp.route('/house_infos/', methods=['GET'])
def house_infos():
    houses = House.query.all()
    data = [house.to_dict() for house in houses]
    return jsonify({'code': 200, 'houses': data})


@house_bp.route('/booking/<int:id>/', methods=['GET'])
@is_login
def booking(id):
    if request.method == 'GET':
        return render_template('booking.html')


@house_bp.route('/booking/', methods=['POST'])
def booking_info():
    if request.method == 'POST':
        huose = House.query.get(request.form.get('house_id'))
        return jsonify(SUCCESS, huose.to_dict())


@house_bp.route('/search/', methods=['GET'])
def search():

    return render_template('search.html')


@house_bp.route('/my_search/', methods=['GET'])
def my_search():
    begin_date = request.args.get('sd')
    end_date = request.args.get('ed')
    aid = request.args.get('aid')
    begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    houses = House.query.filter(House.area_id==aid).all()
    house_list = []
    house_list2 = []
    for house in houses:
        for order in house.orders:
            if (begin_date < order.begin_date and end_date < order.begin_date) or (begin_date > order.end_date and end_date > order.end_date):
                house_list.append(house)
    orders = Order.query.all()
    order_houses_id = [order.house_id for order in orders]
    house_list1 = House.query.filter(House.id.notin_(order_houses_id)).all()
    for house2 in house_list1:
        if house2.area_id == int(aid):
            house_list2.append(house2)
    house_list = house_list+house_list2
    house_info = [house.to_dict() for house in house_list]
    return jsonify(SUCCESS, house_info)


@house_bp.route('/my_search_g/', methods=['POST'])
def my_search_g():
    if request.method == 'POST':
        begin_date = request.form.get('sd')
        end_date = request.form.get('ed')
        aid = request.form.get('aid')
        begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        houses = House.query.filter(House.area_id == aid).all()
        house_list = []
        house_list2 = []
        for house in houses:
            for order in house.orders:
                if (begin_date < order.begin_date and end_date < order.begin_date) or (
                        begin_date > order.end_date and end_date > order.end_date):
                    house_list.append(house)
        orders = Order.query.all()
        order_houses_id = [order.house_id for order in orders]
        house_list1 = House.query.filter(House.id.notin_(order_houses_id)).all()
        for house2 in house_list1:
            if house2.area_id == int(aid):
                house_list2.append(house2)
        house_list = house_list + house_list2
        house_info = [house.to_dict() for house in house_list]
        return jsonify(SUCCESS, house_info)