"""
在单个文件中开发程序很方便,但却有个很大的缺点,因为程序在全局作用域中创建,所
以无法动态修改配置。运行脚本时,程序实例已经创建,再修改配置为时已晚。这一点对
单元测试尤其重要,因为有时为了提高测试覆盖度,必须在不同的配置环境中运行程序。

这个问题的解决方法是延迟创建程序实例,把创建过程移到可显式调用的工厂函数中。这
种方法不仅可以给脚本留出配置程序的时间,还能够创建多个程序实例,这些实例有时在
测试中非常有用。程序的工厂函数在 app 包的构造文件中定义,如 create_app() 函数
所示。

构造文件导入了大多数正在使用的 Flask 扩展。由于尚未初始化所需的程序实例,所以没
有初始化扩展,创建扩展类时没有向构造函数传入参数。 create_app() 函数就是程序的工
厂函数,接受一个参数,是程序使用的配置名。配置类在 config.py 文件中定义,其中保存
的配置可以使用 Flask app.config 配置对象提供的 from_object() 方法直接导入程序。
至于配置对象,则可以通过名字从 config 字典中选择。程序创建并配置好后,就能初始化
扩展了。在之前创建的扩展对象上调用 init_app() 可以完成初始化过程。
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 导入蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

