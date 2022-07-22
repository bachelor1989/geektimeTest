import pytest
from api.mall import Mall


class TestMall:
    def setup_class(self):
        print("suite 数据初始化 setup_class()")
        self.mall = Mall()

        print("获取token")
        r = self.mall.login('admin123', 'admin123', '')
        token = r.json()['data']['token']
        self.mall.set_token(token)

    def setup(self):
        print("case级别初始化 setup()")

    def test_login(self):
        r = self.mall.login("admin123", 'admin123', '')
        assert r.status_code == 200
        assert r.json()['errmsg'] == '成功'
        assert r.json()['data']['adminInfo']['nickName'] == 'admin123'

    def test_login_fail(self):
        r = self.mall.login('admin123', 'wrong', '')
        assert r.status_code == 200
        assert r.json()['errmsg'] == '用户帐号或密码不正确'

    @pytest.mark.parametrize('username,mobile,user_id',
                             [('user123', '', ''),
                              ('', '13811100999', ''),
                              ('', '', ''),
                              (None, None, ''),
                              ('user', '', ''),
                              ('', '', '1')])
    def test_user_list_match(self, username, mobile, user_id):
        r = self.mall.list_users(username=username, mobile=mobile, user_id=user_id)
        assert r.status_code == 200
        assert r.json()['errmsg'] == '成功'
        list_data = r.json()['data']['list']
        assert len(list_data) > 0
        if username:
            assert username in list_data[0]['nickname']
        if mobile:
            assert mobile == list_data[0]['mobile']
        if user_id:
            assert user_id == str(list_data[0]['id'])

    @pytest.mark.parametrize('username,mobile,user_id',
                             [('admin', '', ''),
                              ('', '138', ''),
                              ('', '', '666')])
    def test_user_list_dismatch(self, username, mobile, user_id):
        r = self.mall.list_users(username=username, mobile=mobile, user_id=user_id)
        assert r.status_code == 200
        assert r.json()['errmsg'] == '成功'
        assert r.json()['data']['total'] == 0

    @pytest.mark.parametrize('nickname,consignee,order_sn,start,end,order_status_array',
                             [('', '', '', '', '', None),
                              ('user', '', '', '', '', None),
                              ('', '牛', '', '', '', None),
                              ('', '', '20220721252146', '', '', None),
                              ('', '', '', '2022-07-13 00:00:00', '2022-07-19 00:00:00', None),
                              ('', '', '', '', '', ['101', '102', '103'])])
    def test_order_list_match(self, nickname, consignee, order_sn, start, end, order_status_array):
        r = self.mall.list_orders(nickname=nickname, consignee=consignee,
                                  order_sn=order_sn, start=start, end=end, order_status_array=order_status_array)
        assert r.status_code == 200
        assert r.json()['errmsg'] == '成功'
        assert r.json()['data']['total'] > 0
        list_data = r.json()['data']['list']
        if nickname:
            for d in list_data:
                assert nickname in d['userName']
        if consignee:
            for d in list_data:
                assert consignee in d['consignee']
        if order_sn:
            for d in list_data:
                assert order_sn == d['orderSn']
        if start:
            for d in list_data:
                assert start <= d['addTime']
        if end:
            for d in list_data:
                assert end >= d['addTime']
        if order_status_array:
            for d in list_data:
                assert str(d['orderStatus']) in order_status_array

    @pytest.mark.parametrize('nickname,consignee,order_sn,start,end,order_status_array',
                             [('admin', '', '', '', '', None),
                              ('', '哈天', '', '', '', None),
                              ('', '', '202207198', '', '', None),
                              ('', '', '', '2022-07-13 00:00:00', '2022-07-14 00:00:00', None),
                              ('', '', '', '', '', ['101', '102'])])
    def test_order_list_dismatch(self, nickname, consignee, order_sn, start, end, order_status_array):
        r = self.mall.list_orders(nickname=nickname, consignee=consignee,
                                  order_sn=order_sn, start=start, end=end, order_status_array=order_status_array)
        assert r.status_code == 200
        assert r.json()['errmsg'] == '成功'
        assert r.json()['data']['total'] == 0

    @pytest.mark.parametrize('page,limit',
                             [('1', '2'),
                              ('2', '2')])
    def test_order_list_page(self, page, limit):
        r = self.mall.list_orders(page=page, limit=limit)
        assert r.status_code == 200
        assert r.json()['errmsg'] == '成功'
        assert str(r.json()['data']['page']) == page
        assert str(r.json()['data']['limit']) == limit
        assert str(len(r.json()['data']['list'])) == limit

    @pytest.mark.last
    def test_logout(self):
        r = self.mall.logout()
        assert r.json()['errmsg'] == '成功'

    def teardown(self):
        print("case teardown()")

    def teardown_class(self):
        print("suite 数据清理 teardown_class()")
