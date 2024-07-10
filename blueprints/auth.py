from flask import Blueprint, render_template, request, jsonify, redirect, url_for,session
from exts import mail, db
from flask_mail import Message
from models import EMailCaptchaModel, UserModel
import random
import string
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return render_template(url_for('auth.login'))
            if check_password_hash(user.password, password):
                # cookie:不适合存储太多数据，适合存储登录授权的东西
                session['user_id'] = user.id
                return redirect('/')
            else:
                return render_template(url_for('auth.login'))
        else:
            return render_template(url_for('auth.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# get请求，从服务器获取数据
# post请求，发送数据给服务器
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 获取前端数据
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


@bp.route('/captcha/email')
def get_email_captcha():
    email = request.args.get('email')
    source = string.digits * 4
    captcha = random.sample(source, 4)
    captcha = ''.join(captcha)
    message = Message(subject='验证码', recipients=[email], body=f'您的验证码是{captcha}')
    mail.send(message)
    # 用数据库存储
    email_captcha = EMailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # {code: 200/400/500,message:"",data:{}}
    return jsonify({"code": 200, "message": "", "data": None})


# @bp.route('/mail/test')
# def mail_test():
#     message = Message(subject='邮箱测试', recipients=['1463155531@qq.com'], body='验证码')
#     mail.send(message)
#     return '邮件发送成功'
