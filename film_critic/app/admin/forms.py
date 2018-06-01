from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField,DateField,FloatField,TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError,NumberRange

from app.models import User,Movie


class LoginForm(FlaskForm):
    """
    登录表单
    """
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')

class MovieInfo(FlaskForm):
    """
    添加电影表单
    """
    name = StringField('电影名', validators=[DataRequired()])
    actor = StringField('主演', validators=[DataRequired()])
    director = StringField('导演', validators=[DataRequired()])
    tag = StringField('类型', validators=[DataRequired()])
    language = StringField('语言', validators=[DataRequired()])
    release_year = DateField('年份', validators=[DataRequired()])
    evaluate = FloatField('评价', validators=[DataRequired(), NumberRange(min=0, max=10, message='数值只能在0-10内')])
    evaluate_count = StringField('评价人数', validators=[DataRequired()])
    country = StringField('国家', validators=[DataRequired()])
    picture = StringField('插图', validators=[DataRequired()])
    description = TextAreaField('简介', validators=[DataRequired()])
    submit = SubmitField('添加')


    def validate_name(self, field):
        if Movie.query.filter_by(name=field.data).first():
            raise ValidationError('电影已存在')

class ModifyInfo(FlaskForm):
    """
    电影信息修改表单
    查找按钮
    """
    find_name = StringField('请输入要查找的电影名', validators=[DataRequired()])
    submit = SubmitField('确定')

    def validate_find_name(self, field):
        if Movie.query.filter_by(name=field.data).first() is None:
            raise ValidationError('电影不存在')

class ModifyInfo2(FlaskForm):
    """
    电影信息修改表
    输入表单
    修改按钮
    """
    name = StringField('电影名', validators=[DataRequired()])
    actor = StringField('主演', validators=[DataRequired()])
    director = StringField('导演', validators=[DataRequired()])
    tag = StringField('类型', validators=[DataRequired()])
    language = StringField('语言', validators=[DataRequired()])
    release_year = DateField('年份', validators=[DataRequired()])
    evaluate = FloatField('评价', validators=[DataRequired(), NumberRange(min=0, max=10, message='数值只能在0-10内')])
    evaluate_count = StringField('评价人数', validators=[DataRequired()])
    country = StringField('国家', validators=[DataRequired()])
    picture = StringField('插图', validators=[DataRequired()])
    description = TextAreaField('简介', validators=[DataRequired()])
    submit = SubmitField('修改')

class DeleteInfo(FlaskForm):
    """
    电影信息表单删除
    查找按钮
    """
    find_name = StringField('请输入要查找的电影名', validators=[DataRequired()])
    submit = SubmitField('确定')

    def validate_find_name(self, field):
        if Movie.query.filter_by(name=field.data).first() is None:
            raise ValidationError('电影不存在')

class DeleteInfo2(FlaskForm):
    """
    电影信息表删除
    输入表单
    删除按钮
    """
    name = StringField('电影名')
    actor = StringField('主演')
    director = StringField('导演')
    tag = StringField('类型')
    language = StringField('语言')
    release_year = DateField('年份')
    evaluate = FloatField('评价', validators=[NumberRange(min=0, max=10, message='数值只能在0-10内')])
    evaluate_count = StringField('评价人数')
    country = StringField('国家')
    picture = StringField('插图')
    description = TextAreaField('简介')
    submit = SubmitField('删除')

class UserInfo(FlaskForm):
    """
            用户信息表单
            查找按钮
            """
    find_name = StringField('请输入要查找的用户名')
    submit = SubmitField('确定')

    def validate_find_name(self, field):
        if field.data == '':
            raise ValidationError('请输入用户名')
        elif User.query.filter_by(username=field.data).first() is None:
            raise ValidationError('用户不存在')

class DeleteUser(FlaskForm):
    """
    用户信息删除按钮
    """
    delete_name = StringField('请输入要删除的用户名')
    delete_submit = SubmitField('删除')
    def validate_delete_name(self, field):
        if field.data == '':
            raise ValidationError('请输入用户名')
        elif User.query.filter_by(username=field.data).first() is None:
            raise ValidationError('用户不存在')
