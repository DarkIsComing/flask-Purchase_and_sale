#-*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05

from flask import Blueprint


home=Blueprint('home',__name__)

import app.home.views
