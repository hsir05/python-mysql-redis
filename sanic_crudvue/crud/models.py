import datetime

from peewee import CharField, IntegerField, DateTimeField, SqliteDatabase, TextField, Model, MySQLDatabase
from playhouse.shortcuts import dict_to_model, model_to_dict

from sanic_session import Session
session = Session()

# db = SqliteDatabase('info.db')
db = MySQLDatabase('todoStu', host='localhost', port=3306, user='root', password='root')


class BaseModel(Model):
    class Meta:
        database = db
        indexes = (
            # create a no-unique on username and email
            (('sex', 'email'), False),
        )

    @classmethod
    def filters(cls, sex=None, email=None, page_number=1, items_per_page=20):
        """this filter code for example demo"""
        if not sex and not email:
            qs = cls.select()
        elif sex and email:
            qs = cls.select().where(cls.sex == sex, cls.email.contains(email))
        elif sex:
            qs = cls.select().where(cls.sex == sex)
        elif email:
            qs = cls.select().where(cls.email.contains(email))
        cls.result = qs.order_by(cls.id).paginate(page_number, items_per_page)
        return cls

    @classmethod
    def list_data(cls, page=1, page_size=10, sort='created_at'):
        qs = cls.select()
        cls.result = qs.order_by(sort).paginate(page, page_size)
        return cls

    @classmethod
    def counts(cls):
        return cls.result.count()

    @classmethod
    def get_id(cls, id):
        return cls.get().where(cls.id == id)

    @classmethod
    def get_user_info(cls, username, password):
        try:
            qs = User.get(User.username == username)
        except Exception:
            return None

        if qs.password == password:
            print('********连接查询********')
            result = cls.select(cls.id, cls.role_name, cls.role_code).join(User, on=(cls.id == User.role_id)).where(cls.id == qs.role_id)
            qs = model_to_dict(qs)
            del qs['role_id']
            del qs['password']
            qs['roleId'] = result[0].id
            qs['roleName'] = result[0].role_name
            qs['roleCode'] = result[0].role_code
            return qs

    @classmethod
    def values_list(cls, *args, **kwargs):
        result = []
        for arg in args:
            qs_expression = "{0}.select({0}.{1}).iterator()".format(cls.__name__, arg)
            for row in eval(qs_expression):
                result.append(eval('row.{0}'.format(arg)))
        return result


class ShanghaiPersonInfo(BaseModel):
    created_at = DateTimeField(default=datetime.datetime.utcnow(), null=True)
    username = CharField()
    email = CharField()
    phone = CharField()
    sex = CharField()
    zone = TextField()


class User(BaseModel):
    created_at = DateTimeField(default=datetime.datetime.utcnow(), null=True)
    username = CharField()
    password = CharField()
    role_id = IntegerField()
    email = CharField()
    phone = CharField()
    sex = CharField()
    status = IntegerField()

    # 用户名不可重复
    def login(self, username):
        print('++++&&&&&&&&*********')
        try:
            qs = User.get(User.username == username)
        except Exception:
            return None
        return qs


class Banner(BaseModel):
    class Meta:
        db_table = 'banner'

    created_at = DateTimeField(default=datetime.datetime.utcnow(), null=True)
    title = CharField()
    img = CharField()
    path = CharField()
    status = IntegerField()
    desc = CharField()


# 角色表
class Roles(BaseModel):
    class Meta:
        db_table = 'roles'

    created_at = DateTimeField(default=datetime.datetime.utcnow(), null=True)
    role_name = CharField()
    role_code = CharField()
    menu_id = IntegerField()


# 权限菜单表
class Menu(BaseModel):
    class Meta:
        db_table = 'menu'

    menu_name = CharField()
    path = CharField()
    icon = CharField()
    parent_id = IntegerField()
    child_id = IntegerField()
    role_id = IntegerField()
