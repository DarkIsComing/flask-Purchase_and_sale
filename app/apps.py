#-*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app=Flask(__name__)


# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://uesr:password@127.0.0.1:3306/dbname?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
# 密钥配置，在生产环境中使用系统自动生成
app.config['SECRET_KEY']='d890fbe7e26c4c3eb557b6009e3f4d3d'

# 调试开关，生产环境是关闭的
app.debug=True

# 注册数据模型
db=SQLAlchemy(app)



# 邮件配置
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

mail = Mail(app)

# 注册蓝图
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint
app.register_blueprint(admin_blueprint,url_prefix='/admin/')
app.register_blueprint(home_blueprint,url_prefix='/')

@app.errorhandler(404)
def page_not_found(error):
    return render_template("admin/404.html"),404






