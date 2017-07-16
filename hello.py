import os
# from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_script import Shell
from flask_bootstrap import Bootstrap
# from flask_moment import Moment
# "flask_wtf.Form" has been renamed to "FlaskForm" and will be removed in 1.0.
# from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# Required si going away in WTForms 3.0, use DataRequired
# from wtforms.validators import Required
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret string hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)


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


# 模型这个术语表示程序使用的持久化实体。在 ORM 中,模型一般是一个 Python 类,类中
# 的属性对应数据库表中的列。
#
# Flask-SQLAlchemy 创建的数据库实例为模型提供了一个基类以及一系列辅助类和辅助函数,
# 可用于定义模型的结构。roles 表和 users 表可定义为模型 Role 和 User
class Role(db.Model):
    # 类变量定义在类中且在<函数体>之外。类变量通常不作为实例变量使用。类变量在整个实例化的对象中是公用的。
    # 类变量 __tablename__ 定义在数据库中使用的表名。
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 添加到 Role 模型中的 users 属性代表这个关系的面向对象视角。
    # 对于一个 Role 类的实例,其 users 属性将返回与角色相关联的用户组成的列表。
    # db.relationship() 的第一个参数表 明这个关系的另一端是哪个模型。如果模型类尚未定义, 可使用字符串形式指定。
    #
    # db.relationship() 中的 backref 参数向 User 模型中添加一个 role 属性, 从而定义反向关系。
    # 这一属性可替代 role_id 访问 Role 模型, 此时获取的是模型对象, 而不是外键的值。
    users = db.relationship("User", backref='role', lazy='dynamic')

    def __repr__(self):
        # %r是一个万能的格式付，它会将后面给的参数原样打印出来，带有类型信息
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 关系使用users表中的外键连接了两行。添加到User模型中的role_id列被定义为外键,
    # 就是这个外键建立起了关系。传给db.ForeignKey()的参数'roles.id'表明,这列的值是
    # roles表中行的id值。
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    # app.run(debug=True)
