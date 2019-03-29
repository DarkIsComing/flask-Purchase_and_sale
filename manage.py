#-*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05

from app.apps import app

if __name__ == '__main__':
    app.run(host='127.0.0.1',debug=True,port=5050)