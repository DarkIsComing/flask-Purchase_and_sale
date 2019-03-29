#-*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05


import os
import time
from functools import wraps
from io import BytesIO
from flask_mail import Message
from werkzeug.security import generate_password_hash
from app.apps import db, mail
from app.admin import admin
from flask import render_template, make_response, session, redirect, url_for, request, flash, abort
from app.admin.forms import LoginForm, RegisterForm, addsuppliers, increasePurchaseOrders, purchsearch, \
    returnordersearch, goodssearch, addgoodsname, suppliersserach, salesorderssearch, returnsalessearch, customesserch, \
    addcustomes, warehouseserch, enteringwarehouseserach, outWarehousingsearch, \
    addsection, adddutys, powerss, addsaleorder, bumens, alertpasswd, wjpasswd, beifenser
from app.admin.uilt import get_verify_code, bars, lines, pies, on_created
from app.models import User, Purchase, goods, supplier, client, section, duty, inwarehouse, stock, sealreturngoods, \
    warehouse, returngoods, sales, power


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if 'admin' not in session:
            return redirect(url_for("admin.login",next=request.url))
        return f(*args,**kwargs)
    return decorated_function

def admin_power(f):
    @wraps(f)
    def admin_function(*args,**kwargs):
        if session['power']!='root' :
            return render_template("admin/errorroot.html")
        return f(*args,**kwargs)
    return admin_function

# 登陆模块
@admin.route("/login/",methods=["GET","POST"])
def login():
    """登陆路由"""

    form=LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = User.query.filter_by(user_count=data['account']).first()
        admins = db.session.query(User.user_power).filter_by(user_count=data['account']).first()
        if admin == None:
            flash("账号错误")
            return redirect(url_for("admin.login"))
        if not admin.check_pwd(data['pwd']):
            flash("密码错误")
            return redirect(url_for("admin.login"))
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('Wrong verify code.')
            return redirect(url_for("admin.login"))
        power_name = db.session.query(power.power_name).filter_by(power_name=admins[0]).first()
        session["admin"] = data['account']
        session['power']=power_name[0]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 验证码路由
@admin.route('/code/')
def code():
    """生成验证码图片流"""
    image, code = get_verify_code()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['image'] = code
    return response

# 注册路由
@admin.route("/register/",methods=["GET","POST"])
def register():
    """注册路由"""
    form=RegisterForm()
    if form.validate_on_submit():
        data = form.data
        names = User.query.filter_by(user_count=data['account']).count()
        if names == 1:
            flash('注册失败')
            return redirect(url_for("admin.register"))
        ses=['','男','女']
        names = User(
            user_count=data['account'],
            user_pwd=generate_password_hash((data['pwd'])),
            user_name=data['name'],
            user_sex=ses[data['sex']],
            user_phone=data['phone'],
            user_mail=data['mail']
        )

        db.session.add(names)
        db.session.commit()
        flash("注册成功")

        return redirect(url_for("admin.login"))
    return render_template("admin/register.html",form=form)

# 忘记密码路由
@admin.route("/forgetpws/")
def forgetpws():
    pass


# 首页
@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html",name=session["admin"])
@admin.route("/workPlatform/")
@admin_login_req
def workPlatform():
    purchases=len(Purchase.query.all())
    saless=len(sales.query.all())
    warehouses=len(warehouse.query.all())
    names={"purchases":purchases,"saless":saless,"warehouses":warehouses}
    return render_template("admin/workPlatform.html",name=session["admin"],names=names)

# 退出
@admin.route('/logout')
@admin_login_req
def logout():
    session.pop('admin',None)
    return redirect(url_for("admin.login"))




# 采购模块
# 供应商
@admin.route("/supplier/<int:page>",methods=["GET","POST"])
@admin_login_req
def suppliers(page=None):
    form=suppliersserach()
    if page is None:
        page = 1
    if form.data['name'] is None or form.data['name']=='':
        page_data = supplier.query.order_by(
            supplier.supplier_id.desc()
        ).paginate(page=page, per_page=4)
        return render_template("admin/supplier.html", form=form, page_data=page_data)
    if form.data['name'].strip():
        page_data = supplier.query.order_by(
            supplier.supplier_id.desc()
        ).filter(form.data['name']==supplier.supplier_name).paginate(page=page, per_page=4)

        return render_template("admin/supplier.html", form=form, page_data=page_data)

# 删除供应商
@admin.route("/dellsupplier/",methods=["GET"])
@admin_login_req
def dellsupplier():
    ids=request.args.get('id')
    names = supplier.query.filter_by(supplier_id=ids).first()
    try:
        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"


# 添加供应商
@admin.route("/addSupplier/",methods=["GET","POST"])
@admin_login_req
def addSupplier():
    form=addsuppliers()
    if form.validate_on_submit():
        data = form.data
        names = supplier.query.filter_by(supplier_name=data['name']).count()
        if names == 1:
            flash("添加失败，已有此供应商")
            return redirect(url_for("admin.addTradeName"))
        names = supplier(
            supplier_name=data['name'],
            supplier_addre=data['addre'],
            supplier_credit=data['credit'],
        )
        db.session.add(names)
        db.session.commit()
        time.sleep(2)
    return render_template("admin/addSupplier.html",form=form)


# 采购订单
@admin.route("/purchaseOrder/<int:page>",methods=["GET","POST"])
@admin_login_req
def purchaseOrder(page=None):
    form=purchsearch()
    if page is None:
        page = 1
    if (form.data['goods_name'] is None or form.data['goods_name']=='') and(form.data['person_name'] is None or form.data['person_name'] ==''):
        page_data = db.session.query(Purchase.purchase_id,Purchase.purchase_num,Purchase.purchase_count,Purchase.purchase_price,
                                     Purchase.purchase_supplier,Purchase.purchase_user_name,Purchase.purchase_goods,Purchase.purchase_addtime,
                                     goods.goods_price).order_by(
            Purchase.purchase_id.desc()
        ).filter_by(purchase_goods=goods.goods_name).paginate(page=page, per_page=4)

        return render_template("admin/purchaseOrder.html", form=form, page_data=page_data)

    if (form.data['goods_name'].strip()) and (form.data['person_name'] is None or form.data['person_name'] ==''):
        page_data = Purchase.query.order_by(
            Purchase.purchase_id.desc()
        ).filter(form.data['goods_name']==Purchase.purchase_goods).paginate(page=page, per_page=4)

        return render_template("admin/purchaseOrder.html", form=form, page_data=page_data)

    if (form.data['goods_name'] is None or form.data['goods_name'] == '') and (
            form.data['person_name'].strip()):
        page_data = Purchase.query.order_by(
            Purchase.purchase_id.desc()
        ).filter(form.data['person_name']==Purchase.purchase_user_name).paginate(page=page, per_page=4)
        return render_template("admin/purchaseOrder.html", form=form, page_data=page_data)

# 添加订单
@admin.route("/increasePurchaseOrder/",methods=["GET","POST"])
@admin_login_req
def increasePurchaseOrder():
    form=increasePurchaseOrders()
    if form.validate_on_submit():
        data = form.data
        good_names=goods.query.filter_by(goods_id=data['goods_name']).first()
        ywy=User.query.filter_by(user_id=data['ywy']).first()
        gys=supplier.query.filter_by(supplier_id=data['gys']).first()
        names = Purchase(
            purchase_goods=good_names.goods_name,
            purchase_count=data['num'],
            purchase_supplier=gys.supplier_name,
            purchase_user_name=ywy.user_name,
            purchase_price=float(data['num'])*float(good_names.goods_price),
            purchase_num=on_created()
        )
        db.session.add(names)
        db.session.commit()
        time.sleep(2)

    return render_template("admin/increasePurchaseOrder.html",form=form)

# 删除订单
@admin.route("/dell/",methods=['GET'])
@admin_login_req
def dell():
    ids=request.args.get('id')
    names = Purchase.query.filter_by(purchase_id=ids).first()
    try:
        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"

# 入库订单
@admin.route("/inwarehouses/",methods=['GET'])
@admin_login_req
def inwarehouses():
    ids=request.args.get('id')
    ids = Purchase.query.filter_by(purchase_id=ids).first()
    sql = 'insert into inwarehouse(inwarehouse_num,inwarehouse_count,inwarehouse_price,inwarehouse_goods,inwarehouse_supplier,inwarehouse_user_name) select purchase_num,purchase_count,purchase_price,purchase_goods,purchase_supplier,purchase_user_name from purchase where purchase_id={0}'.format(ids)
    sql_warehouse='insert into warehouse(warehouse_goods_num,warehouse_goods_name,warehouse_supplier_name) select purchase.purchase_count,goods.goods_name,purchase.purchase_supplier from purchase,goods where purchase.purchase_goods=goods.goods_name and purchase_id={0}'.format(ids)

    try:
        db.session.execute(sql)
        db.session.execute(sql_warehouse)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()

    return "success"





# 采购退货单的存储
@admin.route("/returngoods/")
@admin_login_req
def returngood():
    ids = request.args.get('id')
    ids = Purchase.query.filter_by(purchase_id=ids).first()
    sql = 'insert into returngoods(returngoods_num,returngoods_count,returngoods_price,returngoods_goods,returngoods_supplier,returngoods_user_name) select purchase_num,purchase_count,purchase_price,purchase_goods,purchase_supplier,purchase_user_name from Purchase where purchase_id={0}'.format(
        ids)
    try:
        db.session.execute(sql)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()

    return "success"

# 采购退货单
@admin.route("/returnOrder/<int:page>",methods=['GET',"POST"])
@admin_login_req
def returnOrder(page=None):
    form = returnordersearch()
    if page is None:
        page = 1
    if (form.data['goods_name'] is None or form.data['goods_name']=='') and(form.data['person_name'] is None or form.data['person_name'] ==''):
        page_data = returngoods.query.order_by(
            returngoods.returngoods_id.desc()
        ).paginate(page=page, per_page=4)
        return render_template("admin/returnOrder.html", form=form, page_data=page_data)
    if (form.data['goods_name'].strip()) and (form.data['person_name'] is None or form.data['person_name'] ==''):
        page_data = returngoods.query.order_by(
            returngoods.returngoods_id.desc()
        ).filter(form.data['goods_name']==returngoods.returngoods_goods).paginate(page=page, per_page=4)
        return render_template("admin/returnOrder.html", form=form, page_data=page_data)
    if (form.data['goods_name'] is None or form.data['goods_name'] == '') and (
            form.data['person_name'].strip()):
        page_data = returngoods.query.order_by(
            returngoods.returngoods_id.desc()
        ).filter(form.data['person_name']==returngoods.returngoods_user_name).paginate(page=page, per_page=4)
        return render_template("admin/returnOrder.html", form=form, page_data=page_data)





# 商品类型模块
@admin.route("/categoryOfGoods/<int:page>",methods=["GET","POST"])
@admin_login_req
def categoryOfGoods(page=None):
    form = goodssearch()
    if page is None:
        page = 1
    if form.data['goods_name'] is None or form.data['goods_name'] == '':
        page_data = goods.query.order_by(
            goods.goods_id.desc()
        ).paginate(page=page, per_page=4)
        return render_template("admin/categoryOfGoods.html", form=form, page_data=page_data)
    if form.data['goods_name'].strip():
        page_data = goods.query.order_by(
            goods.goods_id.desc()
        ).filter(form.data['goods_name'] == goods.goods_name).paginate(page=page, per_page=4)
        return render_template("admin/categoryOfGoods.html", form=form, page_data=page_data)



# 删除商品种类
@admin.route("/dellgoods/",methods=['GET'])
@admin_login_req
def dellgoods():
    ids=request.args.get('id')
    names = goods.query.filter_by(goods_id=ids).first()
    try:
        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"


# 添加商品
@admin.route("/addTradeName/",methods=["GET","POST"])
@admin_login_req
def addTradeName():
    form=addgoodsname()
    if form.validate_on_submit():
        data = form.data
        names = goods.query.filter_by(goods_name=data['name']).count()
        if names == 1:
            flash("添加失败，已经有此商品")
            return redirect(url_for("admin.addTradeName"))
        names = goods(
            goods_name=data['name'],
            goods_price=data['price'],
            goods_intro=data['info'],
        )
        db.session.add(names)
        db.session.commit()
        flash("添加商品成功")
        time.sleep(2)
    return render_template("admin/addTradeName.html",form=form)






# 销售模块
# 销售订单
@admin.route("/salesOrder/<int:page>",methods=["GET","POST"])
@admin_login_req
def salesOrder(page=None):
    form = salesorderssearch()
    if page is None:
        page = 1
    if (form.data['goods_name'] is None or form.data['goods_name'] == '') and (
            form.data['person_name'] is None or form.data['person_name'] == ''):
        page_data = db.session.query(sales.sales_goods_name, sales.sales_num, sales.sales_count,
                                     sales.sales_price,
                                     sales.sales_user_name,
                                     sales.sales_addtime,
                                     sales.sales_id,
                                     client.client_name).order_by(
            sales.sales_id.desc()
        ).filter_by(sales_client_id=client.client_id).paginate(page=page, per_page=4)
        return render_template("admin/salesOrder.html", form=form, page_data=page_data)

    if (form.data['goods_name'].strip()) and (form.data['person_name'] is None or form.data['person_name'] == ''):
        page_data = db.session.query(sales.sales_id, sales.sales_num, sales.sales_count,
                                     sales.sales_price,
                                     sales.sales_user_name, sales.sales_goods_name,
                                     sales.sales_addtime,
                                     client.client_name).order_by(
            sales.sales_id.desc()
        ).filter_by(form.data['goods_name'] == sales.sales_goods_name,sales_client_id=client.client_id).paginate(page=page, per_page=4)
        return render_template("admin/salesOrder.html", form=form, page_data=page_data)

    if (form.data['goods_name'] is None or form.data['goods_name'] == '') and (
            form.data['person_name'].strip()):
        page_data = db.session.query(sales.sales_id, sales.sales_num, sales.sales_count,
                                     sales.sales_price,
                                     sales.sales_user_name, sales.sales_goods_name,
                                     sales.sales_addtime,
                                     client.client_name).order_by(
            sales.sales_id.desc()
        ).filter_by(form.data['goods_name'] == sales.sales_user_name,sales_client_id=client.client_id).paginate(page=page, per_page=4)
        return render_template("admin/salesOrder.html", form=form, page_data=page_data)


# 删除销售订单
@admin.route("/dellsaleses/",methods=["GET"])
@admin_login_req
def dellsaleses():
    ids=request.args.get('id')
    names = sales.query.filter_by(sales_id=ids).first()
    try:
        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"


# 增加销售订单
@admin.route("/addsalesOrder/",methods=["GET","POST"])
@admin_login_req
def addsalesOrder():
    form=addsaleorder()
    if form.validate_on_submit():
        data = form.data
        warehouse_names = db.session.query(warehouse.warehouse_goods_name).filter_by(warehouse_id=data['goods_name'])
        goods_names=goods.query.filter_by(goods_name=warehouse_names).first()

        ywy = User.query.filter_by(user_id=data['ywy']).first()
        gk = client.query.filter_by(client_id=data['gk']).first()

        names = sales(
            sales_goods_name=warehouse_names.first().warehouse_goods_name,
            sales_count=data['num'],
            sales_client_id=gk.client_id,
            sales_user_name=ywy.user_name,
            sales_price=float(data['num']) * float(goods_names.goods_price),
            sales_num=on_created()

        )

        db.session.add(names)
        db.session.commit()
        time.sleep(2)
    return render_template("admin/addsalesOrder.html",form=form)


# 销售出库
@admin.route("/outwarehouses/",methods=['GET'])
@admin_login_req
def outwarehouses():

    ids=request.args.get('id')
    sales_goods_name=db.session.query(sales.sales_goods_name,sales.sales_count).filter_by(sales_id=ids).first()
    warehouse_goods=db.session.query(warehouse.warehouse_goods_num).filter_by(warehouse_goods_name=sales_goods_name.sales_goods_name).first()
    sql = 'insert into stock(stock_num,stock_count,stock_price,stock_goods,stock_supplier,stock_user_name) select sales_num,sales_count,sales_price,sales_goods_name,sales_client_id,sales_user_name from sales where sales_id={0}'.format(ids)

    try:
        db.session.execute(sql)

        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"



# 销售退货
@admin.route("/returnsalegoods/")
@admin_login_req
def returnsalegoods():
    ids = request.args.get('id')
    ids = sales.query.filter_by(sales_id=ids).first()
    sql = 'insert into sealreturngoods(sealreturngoods_num,sealreturngoods_count,sealreturngoods_price,sealreturngoods_goods,sealreturngoods_supplier,sealreturngoods_user_name) select sales_num,sales_count,sales_price,sales_goods_name,sales_client_id,sales_user_name from sales where sales_id={0}'.format(ids)
    try:
        db.session.execute(sql)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()

    return "success"


# 销售退货单
@admin.route("/returnSales/<int:page>",methods=["GET","POST"])
@admin_login_req
def returnSales(page=None):
    form=returnsalessearch()
    if page is None:
        page = 1

    if (form.data['goods_name'] is None or form.data['goods_name'] == '') and (
            form.data['person_name'] is None or form.data['person_name'] == ''):
        page_data = db.session.query(sealreturngoods.sealreturngoods_user_name, sealreturngoods.sealreturngoods_num,
                                     sealreturngoods.sealreturngoods_count,
                                     sealreturngoods.sealreturngoods_price,
                                     sealreturngoods.sealreturngoods_goods,
                                     sealreturngoods.sealreturngoods_addtime,
                                     client.client_name).order_by(
            sealreturngoods.sealreturngoods_id.desc()
        ).filter_by(sealreturngoods_supplier=client.client_id).paginate(page=page, per_page=4)
        return render_template("admin/returnSales.html", form=form, page_data=page_data)
    if (form.data['goods_name'].strip()) and (form.data['person_name'] is None or form.data['person_name'] == ''):
        page_data = db.session.query(sealreturngoods.sealreturngoods_user_name, sealreturngoods.sealreturngoods_num,
                                     sealreturngoods.sealreturngoods_count,
                                     sealreturngoods.sealreturngoods_price,
                                     sealreturngoods.sealreturngoods_goods,
                                     sealreturngoods.sealreturngoods_addtime,
                                     client.client_name).order_by(
            sealreturngoods.sealreturngoods_id.desc()
        ).filter_by(form.data['goods_name'] == sealreturngoods.sealreturngoods_goods, sealreturngoods_supplier=client.client_id).paginate(
            page=page, per_page=4)
        return render_template("admin/returnSales.html", form=form, page_data=page_data)
    if (form.data['goods_name'] is None or form.data['goods_name'] == '') and (
            form.data['person_name'].strip()):
        page_data = db.session.query(sealreturngoods.sealreturngoods_user_name, sealreturngoods.sealreturngoods_num,
                                     sealreturngoods.sealreturngoods_count,
                                     sealreturngoods.sealreturngoods_price,
                                     sealreturngoods.sealreturngoods_goods,
                                     sealreturngoods.sealreturngoods_addtime,
                                     client.client_name).order_by(
            sealreturngoods.sealreturngoods_id.desc()
        ).filter_by(form.data['goods_name'] == sealreturngoods.sealreturngoods_user_name, sealreturngoods_supplier=client.client_id).paginate(
            page=page, per_page=4)
        return render_template("admin/salesOrder.html", form=form, page_data=page_data)




# 删除销售退货订单
@admin.route("/dellreturnsaleses/",methods=["GET"])
@admin_login_req
def dellreturnsaleses():
    ids=request.args.get('id')
    names = sealreturngoods.query.filter_by(sealreturngoods_id=ids).first()
    try:

        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"

# 客户管理
@admin.route("/customerz/<int:page>",methods=["GET","POST"])
@admin_login_req
def customerz(page=None):
    form=customesserch()
    if page is None:
        page = 1

    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['phone'] is None or form.data['phone'] == ''):
        page_data = client.query.order_by(
            client.client_id.desc()
        ).paginate(page=page, per_page=4)
        return render_template("admin/customerz.html", form=form, page_data=page_data)

    if (form.data['name'].strip()) and (form.data['phone'] is None or form.data['phone'] == ''):
        page_data = client.query.order_by(
            client.client_id.desc()
        ).filter(form.data['name'] == client.client_name).paginate(page=page, per_page=4)

        return render_template("admin/customerz.html", form=form, page_data=page_data)

    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['phone'].strip()):
        page_data = client.query.order_by(
            client.client_id.desc()
        ).filter(form.data['phone'] == client.client_phone).paginate(page=page, per_page=4)
        return render_template("admin/customerz.html", form=form, page_data=page_data)



# 增加客户
@admin.route("/addCustomerz/",methods=["GET","POST"])
@admin_login_req
def addCustomerz():
    form=addcustomes()
    if form.validate_on_submit():
        data = form.data
        names = client.query.filter_by(client_name=data['name']).count()
        if names == 1:
            flash("添加失败，已有此用户")
            return redirect(url_for("admin.addTradeName"))
        names = client(
            client_name=data['name'],
            client_addre=data['addr'],
            client_phone=data['phone'],
            client_credit=data['credit']
        )
        db.session.add(names)
        db.session.commit()
        time.sleep(2)
    return render_template("admin/addCustomerz.html",form=form)


# 删除客户
@admin.route("/dellcustomer/",methods=['GET'])
@admin_login_req
def dellcustomer():
    ids=request.args.get('id')
    names = client.query.filter_by(client_id=ids).first()
    try:

        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"



# 财务模块
# 员工工资
@admin.route("/employeeWages/")
@admin_login_req
def employeeWages():
    return render_template("admin/employeeWages.html")

# 进购利润
@admin.route("/procurementfunds/")
@admin_login_req
def procurementfunds():
    return render_template("admin/ProcurementFunds.html")

# 销售利润
@admin.route("/salesfunds/")
@admin_login_req
def salesfunds():
    return render_template("admin/SalesFunds.html")

# 总利润
@admin.route("/totalprofit/")
@admin_login_req
def totalprofit():
    return render_template("admin/TotalProfit.html")



# 仓库模块

# 库存信息
@admin.route("/seeWarehouse/<int:page>",methods=["GET","POST"])
@admin_login_req
def seeWarehouse(page=None):
    form = warehouseserch()
    if page is None:
        page = 1

    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['gys'] is None or form.data['gys'] == ''):
        page_data=db.session.query(warehouse.warehouse_goods_name,warehouse.warehouse_goods_num,warehouse.warehouse_supplier_name,goods.goods_price).order_by(
            warehouse.warehouse_id.desc()
        ).filter_by(warehouse_goods_name=goods.goods_name).paginate(page=page, per_page=4)
        return render_template("admin/seeWarehouse.html", form=form, page_data=page_data)

    if (form.data['name'].strip()) and (form.data['gys'] is None or form.data['gys'] == ''):
        page_data = db.session.query(warehouse.warehouse_id, warehouse.warehouse_goods_num,
                                     warehouse.warehouse_supplier_name, goods.goods_price).order_by(
            warehouse.warehouse_id.desc()
        ).filter_by(form.data['name'] == warehouse.warehouse_goods_name,warehouse_goods_name=goods.goods_name).paginate(page=page, per_page=4)

        return render_template("admin/seeWarehouse.html", form=form, page_data=page_data)

    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['gys'].strip()):
        page_data = db.session.query(warehouse.warehouse_id, warehouse.warehouse_goods_num,
                                     warehouse.warehouse_supplier_name, goods.goods_price).order_by(
            warehouse.warehouse_id.desc()
        ).filter_by(form.data['gys'] == warehouse.warehouse_supplier_name,
                    warehouse_goods_name=goods.goods_name).paginate(page=page, per_page=4)

        return render_template("admin/seeWarehouse.html", form=form, page_data=page_data)




# 仓库信息删除
@admin.route("/dellwarehouse/",methods=["GET"])
@admin_login_req
def dellwarehouse():
    ids=request.args.get('id')
    names = warehouse.query.filter_by(warehouse_id=ids).first()
    try:
        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"

# 采购入库单
@admin.route("/enteringWarehouse/<int:page>",methods=["GET","POST"])
@admin_login_req
def enteringWarehouse(page=None):
    form = enteringwarehouseserach()
    if page is None:
        page = 1
    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['ywy'] is None or form.data['ywy'] == ''):
        page_data = inwarehouse.query.order_by(
            inwarehouse.inwarehouse_id.desc()
        ).paginate(page=page, per_page=4)
        return render_template("admin/enteringWarehouse.html", form=form, page_data=page_data)

    if (form.data['name'].strip()) and (form.data['ywy'] is None or form.data['ywy'] == ''):
        page_data = inwarehouse.query.order_by(
            inwarehouse.inwarehouse_id.desc()
        ).filter(form.data['name'] == inwarehouse.inwarehouse_goods).paginate(page=page, per_page=4)

        return render_template("admin/enteringWarehouse.html", form=form, page_data=page_data)

    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['ywy'].strip()):
        page_data = inwarehouse.query.order_by(
            inwarehouse.inwarehouse_id.desc()
        ).filter(form.data['gys'] == inwarehouse.inwarehouse_user_name).paginate(page=page, per_page=4)
        return render_template("admin/enteringWarehouse.html", form=form, page_data=page_data)


# 删除采购入库
@admin.route("/dellcgrk/",methods=["GET"])
@admin_login_req
def dellcgrk():
    ids=request.args.get('id')
    names = inwarehouse.query.filter_by(inwarehouse_id=ids).first()
    try:

        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"

# 出库单
@admin.route("/outWarehousing/<int:page>",methods=['GET',"POST"])
@admin_login_req
def outWarehousing(page=None):
    form=outWarehousingsearch()
    if page is None:
        page = 1
    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['ywy'] is None or form.data['ywy'] == ''):
        page_data = db.session.query(stock.stock_num,
                                     stock.stock_count,
                                     stock.stock_price,
                                     stock.stock_user_name,
                                     stock.stock_goods,
                                     stock.stock_addtime,
                                     client.client_name).order_by(
            stock.stock_id.desc()
        ).filter_by(stock_supplier=client.client_id).paginate(page=page, per_page=4)
        return render_template("admin/outWarehousing.html", form=form, page_data=page_data)

    if (form.data['name'].strip()) and (form.data['ywy'] is None or form.data['ywy'] == ''):
        page_data = db.session.query(stock.stock_num,
                                     stock.stock_count,
                                     stock.stock_price,
                                     stock.stock_user_name,
                                     stock.stock_goods,
                                     stock.stock_addtime,
                                     client.client_name).order_by(
            stock.stock_id.desc()
        ).filter_by(form.data['name'] == stock.stock_goods,stock_supplier=client.client_id).paginate(page=page, per_page=4)
        return render_template("admin/enteringWarehouse.html", form=form, page_data=page_data)

    if (form.data['name'] is None or form.data['name'] == '') and (
            form.data['ywy'].strip()):
        page_data = db.session.query(stock.stock_num,
                                     stock.stock_count,
                                     stock.stock_price,
                                     stock.stock_user_name,
                                     stock.stock_goods,
                                     stock.stock_addtime,
                                     client.client_name).order_by(
            stock.stock_id.desc()
        ).filter_by(form.data['gys'] == stock.stock_user_name,stock_supplier=client.client_id).paginate(page=page, per_page=4)
        return render_template("admin/enteringWarehouse.html", form=form, page_data=page_data)


# 删除出库订单
@admin.route("/dellckdd/",methods=["GET"])
@admin_login_req
def dellckdd():
    ids=request.args.get('id')
    names = stock.query.filter_by(stock_id=ids).first()
    try:
        db.session.delete(names)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"







# 统计模块
# 库存统计
@admin.route("/inventoryStatistics/")
@admin_login_req
def inventoryStatistics():
    _bar,javascript_snippet = pies()
    return render_template(
        "admin/inventoryStatistics.html",
        chart_id=_bar.chart_id,
        host=url_for('static', filename='assets/js'),
        renderer=_bar.renderer,
        my_width="50%",
        my_height=500,
        custom_function=javascript_snippet.function_snippet,
        options=javascript_snippet.option_snippet,
        script_list=_bar.get_js_dependencies(),
    )


# 订单统计
@admin.route("/purchasingStatistics/")
@admin_login_req
def purchasingStatistics():
    _bar, javascript_snippet = bars()
    return render_template(
        "admin/purchasingStatistics.html",
        chart_id=_bar.chart_id,
        host=url_for('static',filename='assets/js'),
        renderer=_bar.renderer,
        my_width="50%",
        my_height=500,
        custom_function=javascript_snippet.function_snippet,
        options=javascript_snippet.option_snippet,
        script_list=_bar.get_js_dependencies(),
    )


# 销售统计
@admin.route("/salesStatistics/")
@admin_login_req
def salesStatistics():
    line, javascript_snippet = lines()
    return render_template(
        "admin/salesStatistics.html",
        chart_id=line.chart_id,
        host=url_for('static', filename='assets/js'),
        renderer=line.renderer,
        my_width="50%",
        my_height=500,
        custom_function=javascript_snippet.function_snippet,
        options=javascript_snippet.option_snippet,
        script_list=line.get_js_dependencies(),
    )


# 基本模块
@admin.route("/persionDetail/",methods=['GET','POST'])
@admin_login_req
def persionDetail():
    form=alertpasswd()
    usermessage=User.query.filter(User.user_count==session["admin"]).first()
    admin = User.query.filter_by(user_count=usermessage.user_count).first()
    if form.validate_on_submit():
        if not admin.check_pwd(form.data['account']):
            flash('旧密码错误，请联系管理员修改')
            return render_template("admin/persionDetail.html", form=form, usermessage=usermessage)
        admin.user_pwd = generate_password_hash((form.data['pwd']))
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        session.pop('admin', None)
        return 'Success'

    return render_template("admin/persionDetail.html",form=form,usermessage=usermessage)

# 忘记密码
@admin.route("/wjmm/",methods=['GET','POST'])
def wjmm():
    form = wjpasswd()
    if form.validate_on_submit():
        usermessage = User.query.filter(User.user_count == form.data["countname"]).first()
        if usermessage is None:
            flash("账号错误！")
            return render_template("admin/wjmm.html", form=form)
        admin = User.query.filter_by(user_count=usermessage.user_count).first()

        if admin.user_mail != form.data['account']:
            flash('请输入正确的邮箱地址，或联系管理员修改')
            return render_template("admin/wjmm.html", form=form)

        admin.user_pwd = generate_password_hash((form.data['pwd']))
        mails=[]
        mails.append(form.data['account'])
        try:
            msg = Message('修改密码通知', sender='gchase@163.com', recipients=mails)
            msg.html = '<span>尊敬的</span>'+usermessage.user_name+'，您好：<br>您在we商贸中申请找回密码<br><b style="background-color: #FF0000">重设密码已完成,若非本人操作</b><br>请及时联系管理员修改<b>ganiner@163.com</b>'
            mail.send(msg)
            flash("修改成功")
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        return redirect(url_for('admin.login'))
    return render_template("admin/wjmm.html", form=form)



# 管理模块
# 员工管理
@admin.route("/admin_list/<int:page>",methods=["GET","POST"])
@admin_login_req
@admin_power
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.user_id.desc()
    ).paginate(page=page, per_page=4)


    return render_template("admin/admin_list.html",page_data=page_data)

# 员工状态
@admin.route("/admin/admin_pass/",methods=["GET"])
@admin_login_req
@admin_power
def admin_pass():
    ids=request.args.get('id')
    ids = User.query.filter_by(user_id=ids).first()
    User.user_ispass=True
    try:
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return "success"

# 部门管理
@admin.route("/section/<int:page>",methods=["GET","POST"])
@admin_login_req
@admin_power
def sections(page=None):
    if page is None:
        page = 1
    page_data = section.query.order_by(
        section.section_id.desc()
    ).paginate(page=page, per_page=4)
    return render_template("admin/section.html",page_data=page_data)

# 添加部门
@admin.route("/addSection/",methods=["GET","POST"])
@admin_login_req
@admin_power
def addSection():
    form=addsection()
    if form.validate_on_submit():
        data = form.data
        names = section.query.filter_by(section_name=data['name']).count()
        if names == 1:
            flash("添加失败，已经有这个部门")
            return redirect(url_for("admin.register"))
        names = section(
            section_name=data['name']
        )
        db.session.add(names)
        db.session.commit()
        time.sleep(2)
    return render_template("admin/addSection.html",form=form)



# 职务管理
@admin.route("/dutylist/<int:page>",methods=["GET","POST"])
@admin_login_req
@admin_power
def dutylist(page=None):
    if page is None:
        page = 1
    page_data = duty.query.order_by(
        duty.duty_id.desc()
    ).paginate(page=page, per_page=4)
    return render_template("admin/dutylist.html",page_data=page_data)

# 添加职务
@admin.route("/addduty/",methods=['GET',"POST"])
@admin_login_req
@admin_power
def addduty():
    form=adddutys()
    if form.validate_on_submit():
        data = form.data
        names = duty.query.filter_by(duty_name=data['name']).count()
        if names == 1:
            flash("添加失败，已经有这个职务")
            return redirect(url_for("admin.register"))
        names = duty(
            duty_name=data['name'],
        )
        db.session.add(names)
        db.session.commit()
        time.sleep(2)
    return render_template("admin/addduty.html",form=form)



# 修改权限
@admin.route('/comminrole/',methods=['GET',"POST"])
@admin_login_req
@admin_power
def comminrole():
    form=powerss()
    if form.validate_on_submit():
        users=User.query.filter_by(user_name=form.data['account'])
    return render_template("admin/comminrole.html",form=form)

# 修改职务和部门
@admin.route('/bumen/',methods=['GET',"POST"])
@admin_login_req
@admin_power
def bumen():
    form=bumens()
    if form.validate_on_submit():
        users=User.query.filter_by(user_id=form.data['account']).first()
        users.user_duty = form.data['dutyser']
        users.user_section = form.data['sectionsr']
        db.session.commit()
        time.sleep(2)
    return render_template("admin/bumen.html",form=form)


# 备份
@admin.route("/beifen/",methods=['GET','POST'])
@admin_login_req
@admin_power
def beifen():
    key = "传入数据库密码"
    name = on_created()
    path = "app/backup/"+name
    form = beifenser()

    if form.validate_on_submit():
        os.system("mysqldump -uroot -p{0} sm2.0 > {1}.dump" .format(key,path))
        os.system("mysqldump  -uroot -p{0} --host=localhost --all-databases> {1}.txt" .format (key,path))
        flash("备份完成")
    return render_template("admin/beifen.html",form=form)