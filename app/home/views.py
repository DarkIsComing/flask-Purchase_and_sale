#-*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05

from app.home import home
from flask import render_template


@home.route("/")
def index():
    return render_template("home/index.html")
