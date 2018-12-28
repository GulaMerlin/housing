import os
import re

from flask import Blueprint, render_template, request, jsonify, session

from app.models import User
from utils.functions import get_generateCode, is_login
from utils.settings import MEDIA_PATH
from utils.static_code import USER_REGISTER_EMAIL_FORMAT_ERROR, USER_REGISTER_PASSWORD_ERROR, USER_REGISTER_CODE_ERROR, \
    USER_REGISTER_PHONE_ERROR, USER_REGISTER_USER_NOT_REGISTER, USER_REGISTER_PASSWORD_FAILED, SUCCESS, \
    USER_REGISTER_USER_IS_REGISTER, IMG_IS_NULL, NAME_IS_EXIST, ID_CARD_ERR, ID_IS_VER, NAME_ERR, \
    ID_IS_EXIST

user_bp = Blueprint('user', __name__)


@user_bp.route('/generateCode/', methods=['POST'])
def generateCode():
    if request.method == 'POST':

        code = get_generateCode()
        session['code'] = code
        return jsonify({'code': 200, 'msg': '请求成功', 'generateCode':code})


@user_bp.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        email_re = '^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'
        phone_re = '^[0-9]{11}$'
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        generateCode = request.form.get('generateCode')
        email = request.form.get('email')
        user = User.query.filter(User.phone==int(phone)).first()
        if user:
            return jsonify(USER_REGISTER_USER_IS_REGISTER)
        if not re.match(phone_re, phone):
            return jsonify(USER_REGISTER_PHONE_ERROR)
        if not generateCode==session['code']:
            return jsonify(USER_REGISTER_CODE_ERROR)
        if not re.match(email_re, email):
            return jsonify(USER_REGISTER_EMAIL_FORMAT_ERROR)
        if not all([password, password2]):
            return jsonify(USER_REGISTER_PASSWORD_ERROR)
        user = User()
        user.phone = int(phone)
        user.password = password
        user.email = email
        user.save()
        return jsonify(SUCCESS)


@user_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        user = User.query.filter(User.phone==mobile).first()
        if not user:
            return jsonify(USER_REGISTER_USER_NOT_REGISTER)
        if not user.check_pwd(password):
            return jsonify(USER_REGISTER_PASSWORD_FAILED)
        session['user_id'] = user.id
        return jsonify(SUCCESS)


@user_bp.route('/user_info/', methods=['GET', 'POST'])
def user_info():
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        return jsonify(user.to_basic_dict())
    if request.method == 'POST':
        pass


@user_bp.route('/my/', methods=['GET', 'POST'])
@is_login
def my():
    if request.method == 'GET':
        return render_template('my.html')
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        try:
            name = user.name
        except:
            name = None
        phone = user.phone
        avatar = user.avatar
        return jsonify({'code': 200, 'msg': '请求成功', 'phone': phone, 'name': name, 'avatar': avatar})


@user_bp.route('/profile/', methods=['GET', 'POST'])
@is_login
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'POST':
        name = request.form.get('name')

        user = User.query.filter(User.name==name).first()
        if user:
            return jsonify(NAME_IS_EXIST)
        user = User.query.get(session['user_id'])
        user.name = name
        user.save()
        return jsonify({'code' :200, 'msg': '保存成功'})


@user_bp.route('/profile_image/', methods=['POST'])
@is_login
def profile_image():
    if request.method == 'POST':
        try:
            image = request.files.get('avatar')
            image.save(os.path.join(os.path.join(MEDIA_PATH, 'User'), image.filename))
            user = User.query.get(session['user_id'])
            user.avatar = image.filename
            user.save()
        except:
            return jsonify(IMG_IS_NULL)
        return jsonify({'code': 200, 'msg': '上传成功'})


@user_bp.route('/auth/', methods=['GET'])
@is_login
def auth():
    if request.method == 'GET':
        return render_template('auth.html')


@user_bp.route('/auth/', methods=['POST'])
def auth_name():
    if request.method == 'POST':
        user = User.query.get(session['user_id'])
        if user.id_name:
            return jsonify(ID_IS_VER)
        real_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        name_re = '^[\u4E00-\u9FA5\uf900-\ufa2d·s]{2,20}$'
        id_re = r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx])|([1−9]\d5\d2((0[1−9])|(10|11|12))(([0−2][1−9])|10|20|30|31)\d2[0−9Xx])'
        if not re.match(id_re, id_card):
            return jsonify(ID_CARD_ERR)
        if not re.match(name_re, real_name):
            return jsonify(NAME_ERR)
        if  User.query.filter(User.id_cart==id_card).first():
            return jsonify(ID_IS_EXIST)
        user.id_name = real_name
        user.id_cart = id_card
        user.save()
        return jsonify({'code': 200, 'msg': '保存成功'})


@user_bp.route('/auth_real_name/', methods=['GET'])
@is_login
def auth_real_name():
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        if user.id_name:
            return jsonify({'code': 7013, 'msg': '已实名认证', 'name': user.id_name, 'id_card': user.id_cart})
        return jsonify({'code': 2})


@user_bp.route('/logout/', methods=['DELETE'])
@is_login
def logout():
    if request.method == 'DELETE':
        session['user_id'] = ''
        return jsonify(SUCCESS)


@user_bp.route('/my_house/', methods=['GET'])
@is_login
def my_house():
    if request.method == 'GET':
        return render_template('myhouse.html')


@user_bp.route('/my_house_info/', methods=['GET'])
@is_login
def my_house_info():
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        houses = user.house
        nums = len(houses)
        data = []
        for house in houses:
            data.append(house.to_dict())
        return jsonify({'code': 200, 'msg': '请求成功', 'nums': nums, 'data':data})


