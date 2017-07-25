from . import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        # %r是一个万能的格式付，它会将后面给的参数原样打印出来，带有类型信息
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # 关系使用users表中的外键连接了两行。添加到User模型中的role_id列被定义为外键,
    # 就是这个外键建立起了关系。传给db.ForeignKey()的参数'roles.id'表明,这列的值是
    # roles表中行的id值。
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
