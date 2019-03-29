# -*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired
from app.models import goods, supplier, User, power, client, duty, section, warehouse


# 登陆表单
class LoginForm(FlaskForm):
    account = StringField(
        label="用户名",
        validators=[
            DataRequired()
        ],
        description="账号",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入账号！",
        }

    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired()
        ],
        description="密码",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请输入密码！",
            "lay-verify": "required",
        }
    )
    verify_code = StringField(
        label='验证码',
        validators=[
            DataRequired()
        ],
        description="验证码",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input-inline",
            "placeholder": "请输入验证码！",
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            "type": "submit",
            "lay-filter": "login",
            "style": "width:100%;",
            "onclick": "mesg()"
        }
    )


# 注册表单
class RegisterForm(FlaskForm):
    account = StringField(
        label='请输入用户名',
        validators=[
            DataRequired()
        ],
        description="输入用户名的输入框",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入登录名！",
        }
    )
    pwd = PasswordField(
        label='请输入密码',
        validators=[
            DataRequired()
        ],
        description="输入密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请输入密码！",
            "lay-verify": "required",
        }
    )
    repwd = PasswordField(
        label='请确认密码',
        validators=[
            DataRequired()
        ],
        description="确认密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请确认密码！",
            "lay-verify": "required",
        }
    )
    name = StringField(
        label='请输入真实姓名',
        validators=[
            DataRequired()
        ],
        description="请输入真实姓名输入框",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入真实姓名！",
            "lay-verify": "required",
        }
    )
    sex = SelectField(
        label="请选择性别",
        validators=[
            DataRequired()
        ],
        coerce=int,
        choices=[(0, "性别"), (1, "男"), (2, "女")],
        description="请选择性别",

        render_kw={
            "class": "contrller",
        }
    )
    phone = StringField(
        label='请输入电话号码',
        validators=[
            DataRequired()
        ],
        description="请输入电话号码",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入电话号码！",
            "lay-verify": "required",
        }
    )
    mail = StringField(
        label='请输入邮箱',
        validators=[
            DataRequired()
        ],
        description="请输入邮箱",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入邮箱！",
            "lay-verify": "required",
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 添加供应商
class addsuppliers(FlaskForm):
    name = StringField(
        label='供货商名称',
        validators=[
            DataRequired("请输入供应商名称！")
        ],
        description="供应商名称",
        render_kw={
            "type": "text",
            "placeholder": "供应商名称",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )

    addre = StringField(
        label='供应商地址',
        validators=[
            DataRequired("供应商地址！")
        ],
        description="供应商地址",
        render_kw={
            "type": "text",
            "placeholder": "供应商地址",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    credit = SelectField(
        label="供应商级别",
        validators=[
            DataRequired("请选择供应商级别！")
        ],
        coerce=int,
        choices=[(0, "供应商级别"), (1, "一星"), (2, "二星"), (3, "三星"), (4, "四星"), (5, "五星")],
        description="供应商级别",
        render_kw={
            "class": "contrller",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 供应商搜索
class suppliersserach(FlaskForm):
    name = StringField(
        label='供货商名称',
        description="供应商名称",
        render_kw={
            "type": "text",
            "placeholder": "供应商名称",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )

# 采购进货单搜索
class purchsearch(FlaskForm):
    goods_name = StringField(
        description="请输入货物名称",
        render_kw={
            "type": "text",
            "class": "layui-input",
            "placeholder": "请输入货物名称！",
            "lay-verify": "required",
        }
    )
    person_name = StringField(
        description="业务员名称查询",
        render_kw={
            "type": "text",
            "placeholder": "业务员名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 退货单搜索
class returnordersearch(FlaskForm):
    goods_name = StringField(
        description="商品名称查询",
        render_kw={
            "type": "text",
            "placeholder": "商品名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    person_name = StringField(
        description="业务员名称查询",
        render_kw={
            "type": "text",
            "placeholder": "业务员名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )
# 商品信息单搜索
class goodssearch(FlaskForm):
    goods_name = StringField(
        description="商品名称查询",
        render_kw={
            "type": "text",
            "placeholder": "商品名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )

# 添加商品名
class addgoodsname(FlaskForm):
    name = StringField(
        label='商品名',
        validators=[
            DataRequired()
        ],
        description="商品名",
        render_kw={
            "type": "text",
            "placeholder": "商品名",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    price = FloatField(
        label='商品单价',
        validators=[
            DataRequired()
        ],
        description="商品单价",
        render_kw={
            "type": "text",
            "placeholder": "商品单价",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    info = TextAreaField(
        label='商品简介',
        description="商品简介",
        render_kw={
            "type": "text",
            "placeholder": "商品简介",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 添加订单
goodsall = goods.query.all()

class increasePurchaseOrders(FlaskForm):
    goods_name = SelectField(
        label="货物名称",
        validators=[
            DataRequired("请选择供应商级别！")
        ],
        coerce=int,
        choices=[(i.goods_id, i.goods_name) for i in goodsall],
        description="供应商级别",
        render_kw={
            "class": "contrller",
            "type": "text",
            "placeholder": "商品名称",
            "autocomplete": "off",
            "lay-verify": "required",
        }
    )
    num = IntegerField(
        label='进货数量',
        validators=[
            DataRequired("请输入进货数量！")
        ],
        description="进货数量",
        render_kw={
            "type": "text",
            "placeholder": "进货数量",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    suppliers = {1: "5"}
    gys = SelectField(
        label="供应商名称",
        validators=[
            DataRequired("请选择供应商名称！")
        ],
        coerce=int,
        description="供应商名称",
        render_kw={
            "class": "form-control",
        }
    )
    users = {1: "1"}
    ywy = SelectField(
        label="业务员名称",
        validators=[
            DataRequired("请选择供业务员名称！")
        ],
        coerce=int,
        description="业务员名称",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 销售订单搜索
class salesorderssearch(FlaskForm):
    goods_name = StringField(
        description="商品名称查询",
        render_kw={
            "type": "text",
            "placeholder": "商品名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    person_name = StringField(
        description="业务员名称查询",
        render_kw={
            "type": "text",
            "placeholder": "业务员名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 添加销售订单

warehouses = {1: "1"}
class addsaleorder(FlaskForm):
    goods_name = SelectField(
        label="货物名称",
        validators=[
            DataRequired("货物名称！")
        ],
        coerce=int,
        description="供应商级别",
        render_kw={
            "class": "contrller",
            "type": "text",
            "placeholder": "商品名称",
            "autocomplete": "off",
            "lay-verify": "required",
        }
    )
    num = IntegerField(
        label='销售数量',
        validators=[
            DataRequired("请输入销售数量！")
        ],
        description="销售数量",
        render_kw={
            "type": "text",
            "placeholder": "销售数量",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    clients = {1: "k"}
    gk = SelectField(
        label="顾客名称",
        validators=[
            DataRequired("请选择顾客名称！")
        ],
        coerce=int,
        description="顾客名称",
        render_kw={
            "class": "form-control",
        }
    )
    # users = User.query.all()
    users = {"1": 5}
    ywy = SelectField(
        label="业务员名称",
        validators=[
            DataRequired("请选择供业务员名称！")
        ],
        coerce=int,
        # choices=[(i.user_id, i.user_name) for i in users],
        description="业务员名称",
        render_kw={
            "class": "form-control",
        }
    )

    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 退货订单搜索
class returnsalessearch(FlaskForm):
    goods_name = StringField(
        description="商品名称查询",
        render_kw={
            "type": "text",
            "placeholder": "商品名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    person_name = StringField(
        description="业务员名称查询",
        render_kw={
            "type": "text",
            "placeholder": "业务员名称查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )

    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 添加退货单
class addreturnorder(FlaskForm):
    goods_name = SelectField(
        label="货物名称",
        validators=[
            DataRequired("请选择供应商级别！")
        ],
        coerce=int,
        # choices=[(i.goods_id, i.goods_name) for i in goodsall],
        description="供应商级别",
        render_kw={
            "class": "contrller",
            "type": "text",
            "placeholder": "商品名称",
            "autocomplete": "off",
            "lay-verify": "required",
        }
    )
    num = IntegerField(
        label='进货数量',
        validators=[
            DataRequired("请输入进货数量！")
        ],
        description="进货数量",
        render_kw={
            "type": "text",
            "placeholder": "进货数量",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    # suppliers = supplier.query.all()
    suppliers = {1: "l"}
    gys = SelectField(
        label="供应商名称",
        validators=[
            DataRequired("请选择供应商名称！")
        ],
        coerce=int,
        # choices=[(i.supplier_id, i.supplier_name) for i in suppliers],
        description="供应商名称",
        render_kw={
            "class": "form-control",
        }
    )
    # users = User.query.all()
    users = {"1": 5}
    ywy = SelectField(
        label="业务员名称",
        validators=[
            DataRequired("请选择供业务员名称！")
        ],
        coerce=int,
        # choices=[(i.user_id, i.user_name) for i in users],
        description="业务员名称",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 客户管理查询
class customesserch(FlaskForm):
    name = StringField(
        description="客户名查询",
        render_kw={
            "type": "text",
            "placeholder": "客户名查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    phone = StringField(
        description="手机号查询",
        render_kw={
            "type": "text",
            "placeholder": "手机号查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 添加客户
class addcustomes(FlaskForm):
    name = StringField(
        label='客户名',
        validators=[
            DataRequired()
        ],
        description="客户名",
        render_kw={
            "type": "text",
            "placeholder": "客户名",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    addr = StringField(
        label='客户地址',
        validators=[
            DataRequired()
        ],
        description="客户地址",
        render_kw={
            "type": "text",
            "placeholder": "客户地址",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    phone = StringField(
        label='客户手机',
        description="客户手机",
        render_kw={
            "type": "text",
            "placeholder": "客户手机",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    credit = SelectField(
        label="客户级别",
        coerce=int,
        # choices=[(0, "客户级别"), (1, "一星"), (2, "二星"), (3, "三星"), (4, "四星"), (5, "五星")],
        description="客户级别",
        render_kw={
            "class": "contrller",
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 库存查询
class warehouseserch(FlaskForm):
    name = StringField(
        description="商品名查询",
        render_kw={
            "type": "text",
            "placeholder": "商品名查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    gys = StringField(
        description="供应商查询",
        render_kw={
            "type": "text",
            "placeholder": "供应商查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 入库搜索
class enteringwarehouseserach(FlaskForm):
    name = StringField(
        description="商品名查询",
        render_kw={
            "type": "text",
            "placeholder": "商品名查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    ywy = StringField(
        description="业务员查询",
        render_kw={
            "type": "text",
            "placeholder": "业务员查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 出库搜索
class outWarehousingsearch(FlaskForm):
    name = StringField(
        description="商品名查询",
        render_kw={
            "type": "text",
            "placeholder": "商品名查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    ywy = StringField(
        description="业务员查询",
        render_kw={
            "type": "text",
            "placeholder": "业务员查询",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "搜索",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )

# 添加部门
class addsection(FlaskForm):
    name = StringField(
        label='部门名',
        validators=[
            DataRequired()
        ],
        description="部门名",
        render_kw={
            "type": "text",
            "placeholder": "部门名",
            "autocomplete": "off",
            "lay-verify": "required",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )

# 添加职务
class adddutys(FlaskForm):
    name = StringField(
        label='职务名',
        validators=[
            DataRequired()
        ],
        description="职务名",
        render_kw={
            "type": "text",
            "placeholder": "职务名",
            "autocomplete": "off",
            "class": "layui-input"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )

# 修改权限
powers = {"1": 6}
users = {"5": 6}


class powerss(FlaskForm):
    account = SelectField(
        label="请选择用户名",
        validators=[
            DataRequired()
        ],
        coerce=int,
        # choices=[(i.user_id, i.user_name) for i in users],
        description="请选择权限",
        render_kw={
            "class": "contrller",
        }
    )

    powerss = SelectField(
        label="请选择权限",
        validators=[
            DataRequired()
        ],
        coerce=int,
        # choices=[(i.power_id, i.power_name) for i in powers],
        description="请选择权限",
        render_kw={
            "class": "contrller",
        }
    )

    submit = SubmitField(
        "修改",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )


# 修改部门和职务

dutys = {1: 5}
sections = {"p": 5}

class bumens(FlaskForm):
    account = SelectField(
        label="请选择用户名",
        validators=[
            DataRequired()
        ],
        coerce=int,
        # choices=[(i.user_id, i.user_name) for i in users],
        description="用户名",
        render_kw={
            "class": "contrller",
        }
    )

    dutyser = SelectField(
        label="请选择职务",
        validators=[
            DataRequired()
        ],
        coerce=int,
        # choices=[(i.duty_id, i.duty_name) for i in dutys],
        description="请选择职务",
        render_kw={
            "class": "contrller",
        }
    )
    sectionsr = SelectField(
        label="请选择部门",
        validators=[
            DataRequired()
        ],
        coerce=int,
        # choices=[(i.section_id, i.section_name) for i in sections],
        description="请选择部门",
        render_kw={
            "class": "contrller",
        }
    )
    submit = SubmitField(
        "修改",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
            "onclick": "mesg()"
        }
    )

# 修改密码
class alertpasswd(FlaskForm):
    account = StringField(
        label='请输入旧密码',
        validators=[
            DataRequired()
        ],
        description="请输入旧密码",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入旧密码！",
            'autocomplete': 'off'
        }
    )
    pwd = PasswordField(
        label='请输入新密码',
        validators=[
            DataRequired()
        ],
        description="输入密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请输入新密码！",
            "lay-verify": "required",
            'autocomplete': 'off'
        }
    )
    repwd = PasswordField(
        label='请确认密码',
        validators=[
            DataRequired()
        ],
        description="确认密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请确认密码！",
            "lay-verify": "required",
            'autocomplete': 'off'
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )


# 忘记密码
class wjpasswd(FlaskForm):
    countname = StringField(
        label='请输入登录名',
        validators=[
            DataRequired()
        ],
        description="请输入登录名",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入登录名！",
            'autocomplete': 'off'
        }
    )
    account = StringField(
        label='请输入邮箱',
        validators=[
            DataRequired()
        ],
        description="请输入邮箱",
        render_kw={
            "type": "text",
            "lay-verify": "required",
            "class": "layui-input",
            "placeholder": "请输入邮箱！",
            'autocomplete': 'off'
        }
    )
    pwd = PasswordField(
        label='请输入新密码',
        validators=[
            DataRequired()
        ],
        description="输入密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请输入新密码！",
            "lay-verify": "required",
            'autocomplete': 'off'
        }
    )
    repwd = PasswordField(
        label='请确认密码',
        validators=[
            DataRequired()
        ],
        description="确认密码的输入框",
        render_kw={
            "type": "password",
            "class": "layui-input",
            "placeholder": "请确认密码！",
            "lay-verify": "required",
            'autocomplete': 'off'
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "subm",
        }
    )

# 备份
class beifenser(FlaskForm):
    submit = SubmitField(
        "立即备份数据",
        render_kw={
            "class": "layui-btn",
            "lay-filter": "formDemo",
        }
    )

