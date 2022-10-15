from datetime import datetime, timedelta
import jwt
from django.db import connection
from django.http import JsonResponse

JWT_SECRET_KEY = "123"
FAIL_DATA = {'flag': 'no', 'msg': 'fail'}
NOT_ALLOWED_DATA = {'flag': 'no', 'msg': 'not allowed'}
user_account = ['CodeName', 'Password', 'Permission', 'Class', 'Region', 'Race', 'Avatar', 'Mail']
account_approve_queue = ['CodeName', 'Password', 'Permission', 'Class', 'Region', 'Race', 'Description']


def success(msg, result=None):
    print(4)
    if result is None:
        return JsonResponse({'request': {'flag': 'yes', 'msg': msg}})
    else:
        return JsonResponse({'request': {'flag': 'yes', 'msg': msg}, 'result': result})


def fail(msg):
    return JsonResponse({'request': {'flag': 'no', 'msg': msg}})


def get_jwt(username, role_data='default'):
    # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 生payload部分的方法
    # payload = jwt_payload_handler(user)  # 生成payload, 得到字典
    #
    # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 生成jwt的方法
    # print(jwt.decode(token,JWT_SECRET_KEY))
    payload = {
        'exp': datetime.utcnow() + timedelta(seconds=3600),  # 单位秒
        'iat': datetime.utcnow(),
        'data': {'username': username, 'role_data': role_data}
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return str(token)


def judge(token, std):
    test = str.encode(token)
    try:
        result = jwt.decode(test, JWT_SECRET_KEY, algorithms='HS256', options={"verify_signature": False})
        name = result.get('data').get('username')
        print(name)
        with connection.cursor() as cursor:
            sql = 'select * from user_account where CodeName = \'' + name + "\'"
            cursor.execute(sql)
            one = cursor.fetchone()
            return one[2] <= std
    except:
        return False


def token2name(token):
    test = str.encode(token)
    result = jwt.decode(test, JWT_SECRET_KEY, algorithms='HS256', options={"verify_signature": False})
    return result.get('data').get('username')


def check_user(CodeName, password):
    with connection.cursor() as cursor:
        sql = 'select * from user_account where CodeName = \'' + CodeName + "\'"
        try:
            cursor.execute(sql)
            one = cursor.fetchone()
            if one is None:
                return fail('用户名不存在')
            if one[1] == password:
                token = get_jwt(CodeName)
                result = {'CodeName': CodeName, 'token': token}
                return success('登录成功', result)
            else:
                return fail('密码错误')
        except:
            return fail('未知错误')


def all_users():
    sql = 'select * from user_account'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        dict_list = []
        for item in cursor:
            dict_list.append({'CodeName': item[0], 'Permission': item[2]})
    return dict_list


def modify_user(name, permission):
    try:
        sql = "update user_account Set Permission = " + permission + "where CodeName = \''" + name + "\'"
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return success('成功修改')
    except:
        return fail('修改失败')


def delete_user(name):
    try:
        sql = "delete from user_account where CodeName = \''" + name + "\'"
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return success('成功删除')
    except:
        return JsonResponse({'request': FAIL_DATA})


def add_person(username, password, permission):
    with connection.cursor() as cursor:
        sql = "insert into user_account values('{}','{}','{}')".format(username, password, permission)
        print(sql)
        try:
            cursor.execute(sql)
            print("success!")
            return True
        except:
            print('False')
            return False


def reject(name):
    try:
        with connection.cursor() as cursor:
            sql = "delete from account_approve_queue where CodeName = '{}' ".format(name)
            cursor.execute(sql)
            return success('拒绝该用户的注册申请')
    except:
        return JsonResponse({'request': FAIL_DATA})


def consent(CodeName, Permission):
    print(CodeName)
    try:
        with connection.cursor() as cursor:
            sql1 = "select * from account_approve_queue where CodeName = '{}' ".format(CodeName)
            print(sql1)

            cursor.execute(sql1)
            one = cursor.fetchone()
            print(one)
            CodeName = one[0]
            Class = one[1]
            region = one[2]
            Race = one[3]
            Description = one[4]
            Password = one[5]

            sql2 = "insert into user_account values('{}','{}',{},'{}','{}','{}','{}','{}')".format(CodeName, Password,
                                                                                                   Permission,
                                                                                                   "", region, Race, "",
                                                                                                   "", "")
            print(sql2)
            cursor.execute(sql2)
            sql3 = "delete from account_approve_queue where CodeName = '{}' ".format(CodeName)
            print(sql3)
            cursor.execute(sql3)
            return success('同意该用户的申请')
    except:
        return JsonResponse({'request': FAIL_DATA})


def one_user(token):
    try:
        name = token2name(token)
        with connection.cursor() as cursor:
            sql = 'select * from user_account where CodeName = \'' + name + "\'"
            cursor.execute(sql)
            one = cursor.fetchone()
            data = {}
            for i in enumerate(user_account):
                data[i[1]] = one[i[0]]
            return success('获取用户信息成功', data)
    except:
        return fail('获取用户信息失败')


def add_into_queue(CodeName, Class, Region, Race, Description, Password):
    try:
        with connection.cursor() as cursor:
            sql = "insert into account_approve_queue values('{}','{}',{},'{}','{}','{}','{}')".format(CodeName,
                                                                                                      Password, 2,
                                                                                                      Class,
                                                                                                      Region, Race,
                                                                                                      Description,
                                                                                                      )
            print(sql)
            cursor.execute(sql)
        return success('注册成功，请等待审核')
    except:
        return fail('注册失败QWQ')


def all_applications():
    sql = 'select * from account_approve_queue'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        dict_list = []
        for item in cursor:
            data = {}
            for i in enumerate(account_approve_queue):
                if i != 'Password':
                    data[i[1]] = item[i[0]]
            dict_list.append(data)
        return dict_list


def modify_application(CodeName, Permission, Class, Region, Race, Description):
    try:
        sql = "update account_approve_queue Set Permission = {},Class = '{}',Region = '{}',Race = '{}',Description = " \
              "'{}' where CodeName = '{}'".format(Permission, Class, Region, Race, Description, CodeName)
        print(sql)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return success('申请用户信息修改成功~')
    except:
        return fail('修改失败了')
