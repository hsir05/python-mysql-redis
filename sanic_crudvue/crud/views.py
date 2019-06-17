from sanic.response import json
from sanic import Blueprint
from sanic.views import HTTPMethodView
from playhouse.shortcuts import model_to_dict

from .models import ShanghaiPersonInfo, User, Banner, Roles
from .helper import list_remove_repeat
from .util import generate_token, certify_token
from .redisUtils import get_value, set_value

crud_bp = Blueprint(
    'crud',
    url_prefix='/api'
)

key = "JD98Dskw=23njQndW9D"


# 登陆
class LoginView(HTTPMethodView):

    async def post(self, request):
        if request.method == 'POST':
            username, password = request.json.get('username'), request.json.get('password')
            print('^^^^^^^^^&&^^^^^^^^^^')

            result = Roles.get_user_info(username, password)
            token = generate_token(key, 3600)
            # r = await redis.get_redis_pool()
            # await r.set('token', token)
            # t = await r.get('token')
            await set_value('token', token)

            t = await get_value('token')
            return json({'data': result, 'token': token, 't': t, 'message': 'success', 'code': 20000})

            # try:
            #     result = User.login(self, username)
            # except Exception:
            #     return json({'data': None, 'message': '用户不存在', 'code': 20008})
            #
            # if result.password == password:
            #
            #     token = generate_token(key, 3600)
            #     result.token = token
            #     print(result)
            #     return json({'data': result, 'message': 'success', 'code': 20000})
            # else:
            #     return json({'data': None, 'message': '密码错误', 'code': 20007})


# 退出
class LogoutView(HTTPMethodView):

    async def post(self, request):

        print(request.method)
        return json({'message': 'success', 'code': '200'})


class UserInfoListView(HTTPMethodView):

    async def get(self, request):
        max_per_page = request.app.config['MAX_PER_PAGE']
        page = int(request.args.get('page', 1))
        username, password = request.args.get('username'), request.args.get('password')
        print(username)
        print(password)
        qs = User.list_data(username=username, password=password, page_number=page, items_per_page=max_per_page)
        result = [model_to_dict(row) for row in qs.result.iterator()]

        return json(
            {
                'results': result,
                'count': max_per_page,
                'page': page,
                'total': User.list_data(username=username, password=password).counts()
            }
        )


class BannerInfoListView(HTTPMethodView):

    async def get(self, request):
        max_per_page = request.app.config['MAX_PER_PAGE']

        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('pageSize', max_per_page))
        sort = request.args.get('sort', '-created_at')

        qs = Banner.list_data(page=page, page_size=page_size, sort=sort)
        result = [model_to_dict(row) for row in qs.result.iterator()]

        return json(
            {
                'data': result,
                'page': page,
                'total': Banner.list_data().counts(),
                'code': 20000
            }
        )

    async def post(self, request):
        title = request.json.get('title')
        img = request.json.get('img')
        path = request.json.get('path')
        desc = request.json.get('desc')

        Banner.create(title=title, img=img, path=path, desc=desc)
        return json({'message': 'success', 'data': {}, 'code': 20000})

    async def put(self, request):
        id = request.json.get('id')
        title = request.json.get('title')
        img = request.json.get('img')
        path = request.json.get('path')
        desc = request.json.get('desc')

        Banner.update(title=title, img=img, path=path, desc=desc).where(Banner.id == id).execute()
        return json({'message': 'success', 'data': {}, 'code': 20000})

    async def delete(self, request):
        id = request.args.get('id')
        print(id)
        Banner.delete().where(Banner.id == id).execute()
        return json({'message': 'success', 'data': {}, 'code': 20000})


class InfoListView(HTTPMethodView):
    async def get(self, request):
        result = {'roles': ['admin'], 'introduction': 'I am a super administrator', 'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', 'name': 'Super Admin'}
        return json({'data': result, 'message': 'success', 'code': 20000})


class PersonsInfoListView(HTTPMethodView):

    """
    @api {GET} /api/persons   Get all or a part of person info
    @apiName GetAllInfoList
    @apiGroup Info Manage
    @apiVersion 1.0.0

    @apiExample {httpie} Example usage: (support combinatorial search)

    All person：
    http /api/persons

    You can according to 'sex | email' or 'sex & email'
    http /api/persons?sex=xxx&email=xx
    http /api/persons?sex=xxx
    http /api/persons?email=xx

    @apiParam {String} sex
    @apiParam {String} email

    @apiSuccess {String} create_datetime
    @apiSuccess {String} email
    @apiSuccess {String} id
    @apiSuccess {String} phone
    @apiSuccess {String} sex
    @apiSuccess {String} username
    @apiSuccess {String} zone

    """
    async def get(self, request):
        max_per_page = request.app.config['MAX_PER_PAGE']
        page = int(request.args.get('page', 1))
        sex, email = request.args.get('sex'), request.args.get('email')
        qs = ShanghaiPersonInfo.filters(sex=sex, email=email, page_number=page,
                                        items_per_page=max_per_page)
        result = [model_to_dict(row) for row in qs.result.iterator()]

        return json(
            {
                'results': result,
                'count': max_per_page,
                'page': page,
                'total': ShanghaiPersonInfo.filters(sex=sex, email=email).counts()
            }
        )


class PersonsInfoDetailView(HTTPMethodView):

    """
    @api {GET} /api/persons/detail/:id  details info
    @apiName GetPersonDetails
    @apiGroup Info Manage
    @apiVersion 1.0.0

    @apiExample {httpie} Example usage:

    http /api/persons/detail/1

    @apiSuccess {String} create_datetime
    @apiSuccess {String} email
    @apiSuccess {String} id
    @apiSuccess {String} phone
    @apiSuccess {String} sex
    @apiSuccess {String} username
    @apiSuccess {String} zone


    """

    async def get(self, request, item_id):
        data = ShanghaiPersonInfo.get(id=item_id)
        return json(model_to_dict(data))

    async def put(self, request, item_id):
        update_data = eval(request.body.decode())
        qs = ShanghaiPersonInfo.update(**update_data).where(ShanghaiPersonInfo.id == item_id)
        qs.execute()
        new_data = ShanghaiPersonInfo.get(id=item_id)
        return json(model_to_dict(new_data))


class SexListView(HTTPMethodView):

    """
    @api {GET} /api/persons/sex Get all sexList
    @apiName GetAllSexList
    @apiGroup Info Manage
    @apiVersion 1.0.0

    @apiExample {httpie} Example usage:

    http /api/persons/sex

    @apiSuccess {String} label
    @apiSuccess {String} value

    """
    async def get(self, request):
        unique_list = list_remove_repeat(ShanghaiPersonInfo.values_list('sex'))
        result = [dict(label=i, value=i) for i in unique_list]
        return json(result)


class RecListView(HTTPMethodView):
    async def get(self, request):
        unique_list = list_remove_repeat(ShanghaiPersonInfo.values_list('sex'))
        result = [dict(label=i, value=i) for i in unique_list]
        return json(result)


crud_bp.add_route(PersonsInfoDetailView.as_view(), '/detail/<item_id>')
crud_bp.add_route(PersonsInfoListView.as_view(), '/persons')
crud_bp.add_route(SexListView.as_view(), '/persons/sex')
crud_bp.add_route(RecListView.as_view(), '/rec')

crud_bp.add_route(LoginView.as_view(), '/login')
crud_bp.add_route(UserInfoListView.as_view(), '/user')
crud_bp.add_route(BannerInfoListView.as_view(), '/banner')
crud_bp.add_route(LogoutView.as_view(), '/logout')
crud_bp.add_route(InfoListView.as_view(), '/info')
