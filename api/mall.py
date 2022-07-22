from requests import Response
import requests


class Mall:
    def __init__(self):
        self.host = 'litemall.hogwarts.ceshiren.com'
        self.token = None

    def set_token(self, token):
        self.token = token

    def login(self, username, password, code) -> Response:
        r = requests.post(
            'https://' + self.host + '/admin/auth/login',
            headers={'Origin': 'https://litemall.hogwarts.ceshiren.com'},
            cookies={'cookie1': 'cookie1 value'},
            json={
                'username': username,
                'password': password,
                'code': code
            },
        )
        return r

    def list_users(self, username=None, mobile=None, user_id=None,
                   sort='add_time', order='desc', page='1', limit='20') -> Response:
        params = {}
        if user_id is not None:
            params['id'] = user_id
        if username is not None:
            params['username'] = username
        if mobile is not None:
            params['mobile'] = mobile
        if sort is not None:
            params['sort'] = sort
        if order is not None:
            params['order'] = order
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit

        r = requests.get(
            url='https://' + self.host + '/admin/user/list',
            headers={
                'Cookie': 'JSESSIONID=13352cf4-64fe-4f51-b819-08228e842c8a; X-Litemall-Admin-Token='+self.token,
                'Host': self.host,
                'X-Litemall-Admin-Token': self.token
            },
            params=params
        )
        return r

    def list_orders(self, nickname=None, consignee=None, order_sn=None, order_status_array: list = None,
                    start=None, end=None, sort='add_time', order='desc', page='1', limit='20'):
        param = "?"
        if nickname is not None:
            param += "nickname=" + nickname + "&"
        if consignee is not None:
            param += "consignee=" + consignee + "&"
        if order_sn is not None:
            param += "orderSn=" + order_sn + "&"
        if order_status_array is not None:
            for order_status in order_status_array:
                param += "orderStatusArray=" + order_status + "&"
        if start is not None:
            param += "start=" + start + "&"
            param += "timeArray=" + start + "&"
        if end is not None:
            param += "end=" + end + "&"
            param += "timeArray=" + end + "&"
        if sort is not None:
            param += "sort=" + sort + "&"
        if order is not None:
            param += "order=" + order + "&"
        if page is not None:
            param += "page=" + page + "&"
        if page is not None:
            param += "limit=" + limit + "&"
        r = requests.get(
            url='https://' + self.host + '/admin/order/list' + param[:-1],
            headers={
                'Cookie': 'JSESSIONID=13352cf4-64fe-4f51-b819-08228e842c8a; X-Litemall-Admin-Token='+self.token,
                'Host': self.host,
                'X-Litemall-Admin-Token': self.token
            }
        )
        return r

    def logout(self):
        r = requests.post(
            'https://' + self.host + '/admin/auth/logout',
            headers={
                'Cookie': 'JSESSIONID=13352cf4-64fe-4f51-b819-08228e842c8a; X-Litemall-Admin-Token='+self.token,
                'Host': self.host,
                'X-Litemall-Admin-Token': self.token
            }
        )
        return r
