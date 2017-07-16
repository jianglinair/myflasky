# "flask_wtf.Form" has been renamed to "FlaskForm" and will be removed in 1.0.
# from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# Required si going away in WTForms 3.0, use DataRequired
# from wtforms.validators import Required
from wtforms.validators import DataRequired


# 这个表单中的字段都定义为类变量,类变量的值是相应字段类型的对象。在这个示例中,
# NameForm 表单中有一个名为 name 的文本字段和一个名为 submit 的提交按钮。 StringField
# 类表示属性为 type="text" 的 <input> 元素。 SubmitField 类表示属性为 type="submit" 的
# <input> 元素。字段构造函数的第一个参数是把表单渲染成 HTML 时使用的标号。
#
# StringField 构造函数中的可选参数 validators 指定一个由验证函数组成的列表,在接受
# 用户提交的数据之前验证数据。验证函数 Required() 确保提交的字段不为空。
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
