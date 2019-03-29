#-*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05


import datetime
import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from pyecharts import Bar, Line, Pie
from pyecharts_javascripthon.api import TRANSLATOR
from sqlalchemy import extract, func
from app.apps import db
from app.models import Purchase, sales,warehouse,goods


def rndColor():
    '''随机颜色'''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def gene_text():
    '''生成4位验证码'''
    return ''.join(random.sample(string.ascii_letters+string.digits, 4))

def draw_lines(draw, num, width, height):
    '''划线'''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

def get_verify_code():
    '''生成验证码图形'''
    code = gene_text()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB',(width, height),'white')
    # 字体
    font = ImageFont.truetype('app/static/arial.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5+random.randint(-3,3)+23*item, 5+random.randint(-3,3)),
                  text=code[item], fill=rndColor(),font=font )
    # 划线
    draw_lines(draw, 2, width, height)
    # 高斯模糊
    im = im.filter(ImageFilter.GaussianBlur(radius=1.5))
    return im, code


# 进货表格
# 进货量
def bars():
    bar=bar_chart()
    javascript_snippet = TRANSLATOR.translate(bar.options)
    return bar,javascript_snippet

def bar_chart():
    d = db.session.query(func.count(extract('Day', Purchase.purchase_addtime)),
                         extract('Day', Purchase.purchase_addtime)).group_by(
        extract('Day', Purchase.purchase_addtime)
    ).all()

    attr = ["{}号".format(j) for _,j in d]
    v1 = [i for i,_ in d]
    bar = Bar("日采购量")
    bar.add(
        "",
        attr,
        v1,
        is_datazoom_show=True,
        datazoom_type="both",
        datazoom_range=[10, 25],
    )
    return bar


# 销售表格
# 销售量
def lines():
    line = line_chart()
    javascript_snippet = TRANSLATOR.translate(line.options)
    return line,javascript_snippet
def line_chart():
    sale = db.session.query(func.count(extract('Day', sales.sales_addtime)),
                         extract('Day', sales.sales_addtime)).group_by(
        extract('Day', sales.sales_addtime)
    ).all()
    attr = [i for _,i in sale]
    v1 = [j for j,_ in sale]
    print(attr)
    print(v1)
    line = Line("日销售量")

    line.add("", attr, v1, is_stack=True, is_smooth=True,is_fill=True)
    return line


def pies():
    pie = pie_chart()
    javascript_snippet = TRANSLATOR.translate(pie.options)
    return pie,javascript_snippet
def pie_chart():
    warehouses = db.session.query(func.count(warehouse.warehouse_goods_num),
                                  goods.goods_name).filter(warehouse.warehouse_goods_name == goods.goods_name).group_by(
        warehouse.warehouse_supplier_name
    ).all()
    print(warehouses)
    attr = [i for _, i in warehouses]
    v1 = [j for j, _ in warehouses]
    print(attr)
    print(v1)
    pie = Pie("")

    pie.add("", attr, v1, is_stack=True, is_smooth=True, is_fill=True, rosetype="area", is_label_show=True)
    return pie



# 生成编号
def on_created():
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    return uniqueNum







