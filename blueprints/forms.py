import wtforms
from wtforms.validators import Email, Length, EqualTo,InputRequired
from models import UserModel, EMailCaptchaModel


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='验证码格式错误')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    # 自定义验证
    # 1.邮箱验证
    # 2.验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='已被注册')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EMailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='验证码错误')


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='密码格式错误')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=20, message='标题格式错误')])
    content = wtforms.StringField(validators=[Length(min=3,  message='内容格式错误')])


class AnswerForm(wtforms.Form):
    question_id = wtforms.StringField(validators=[InputRequired(message='必须传入ID')])
    content = wtforms.StringField(validators=[Length(min=3,  message='内容格式错误')])
