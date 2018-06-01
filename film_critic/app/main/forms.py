from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError


class EditProfileForm(FlaskForm):
    """
    用户信息编辑表单
    """
    username = StringField('用户名', validators=[Length(0, 64)])
    password = PasswordField('输入密码', validators=[
        DataRequired(), Length(6, 16, message='密码长度至少6位'), EqualTo('password2', message='密码不匹配')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('确认')


class WriteComment(FlaskForm):
    """
    影评输入表单
    """
    content = TextAreaField("评论",
        validators=[
            DataRequired("请输入内容！"),
        ],
        description="内容",
        render_kw={
            "id": "input_content"
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub"
        }
    )
