from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
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


app = Flask(__name__)
# SECRET_KEY is used by Flask-WTF
app.config['SECRET_KEY'] = 'a secret string hard to guess'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
