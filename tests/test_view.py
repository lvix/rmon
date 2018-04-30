import json

from flask import url_for


class TestServerList:
    """测试 Redis 服务器列表 API
    """
    endpoint = 'api.server_list'

    def test_get_servers(self, server, client):
        """获得 Redis 服务器列表
        """
        resp = client.get(url_for(self.endpoint))

        assert resp is not None
        # RestView 视图基类会设置 HTTP 头部 Content-Type 为 json
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'

        # 访问成功后返回状态码 200 OK
        assert resp.status_code == 200

        servers = resp.json

        # 由于当前测试环境中只有一个 Redis 服务器，所以返回数量为1
        assert len(servers) == 1

        h = servers[0]

        assert h['name'] == server.name
        assert h['description'] == server.description
        assert h['host'] == server.host
        assert h['port'] == server.port
        assert 'updated_at' in h
        assert 'created_at' in h

    def test_create_server_success(self, db, client):
        """ 测试创建 Redis 服务器成功
        """
        data = {
            'name': 'redis test',
            'description': 'this is a test record',
            'host': '127.0.0.1',
            'port': '6379',
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        resp = client.post(url_for(self.endpoint), data=json.dumps(data), headers=headers)

        # RestView 视图基类会设置 HTTP 头部 Content-Type 为 json
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        # 创建成功后返回状态码 201 OK
        assert resp.status_code == 201
        # 创建成功 ok == True
        assert resp.json['ok'] is True

    def test_create_server_failed_with_invalid_host(self, db, client):
        """ 无效的服务器地址导致创建 Redis 服务器失败
        """
        data = {
            'name': 'redis test',
            'description': 'this is a test record',
            'host': '127.0.0',  # 无效的地址
            'port': '6379',
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        resp = client.post(url_for(self.endpoint), data=json.dumps(data), headers=headers)
        print(resp.json)
        # RestView 视图基类会设置 HTTP 头部 Content-Type 为 json
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        # 创建失败 400
        assert resp.status_code == 400
        # 创建失败
        assert resp.json['ok'] is False

        assert resp.json['message'] == 'String does not match expected pattern.'

    def test_create_server_failed_with_duplicate_server(self, server, client):
        """ 创建重复的服务器时将失败
        """
        data = {
            'name': 'redis test',
            'description': 'this is a test record',
            'host': '127.0.0.1',
            'port': '6379',
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        resp = client.post(url_for(self.endpoint), data=json.dumps(data), headers=headers)

        # RestView 视图基类会设置 HTTP 头部 Content-Type 为 json
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        # 创建失败 400
        assert resp.status_code == 400
        # 创建失败
        assert resp.json['ok'] is False

        assert resp.json['message'] == 'Redis server already exists'


class TestServerDetail:
    """测试 Redis 服务器详情 API
    """

    endpoint = 'api.server_detail'

    def test_get_server_success(self, server, client):
        """测试获取 Redis 服务器详情
        """
        resp = client.get(url_for(self.endpoint, object_id=1))

        assert resp.status_code == 200

        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'

        h = resp.json

        assert h['name'] == 'redis test'
        assert h['description'] == 'this is a test record'
        assert h['host'] == '127.0.0.1'
        assert h['port'] == 6379
        assert h['created_at']
        assert h['updated_at']

    def test_get_server_failed(self, db, server, client):
        """获取不存在的 Redis 服务器详情失败
        """
        resp = client.get(url_for(self.endpoint, object_id=0))

        assert resp.status_code == 404
        assert resp.json['message'] == 'object doesn\'t exist'
        assert resp.json['ok'] is False

    def test_update_server_success(self, server, client):
        """更新 Redis 服务器成功
        """
        data = {
            'name': 'renamed redis',
            'description': 'this is a renamed redis server',
            'host': '127.0.0.123',
            'port': '6888',
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        resp = client.put(url_for(self.endpoint, object_id=1), data=json.dumps(data), headers=headers)

        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        assert resp.json['ok'] is True

        resp = client.get(url_for(self.endpoint, object_id=1))

        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        h = resp.json
        assert h['name'] == 'renamed redis'
        assert h['description'] == 'this is a renamed redis server'
        assert h['host'] == '127.0.0.123'
        assert h['port'] == 6888
        assert h['created_at']
        assert h['updated_at']
        assert h['created_at'] != h['updated_at']

    def test_update_server_success_with_duplicate_server(self, server, client):
        """更新服务器名称为其他同名服务器名称时失败
        """
        data = {
            'name': 'redis test 1',
            'description': 'this is a test record',
            'host': '127.0.0.1',
            'port': '6379',
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        # 创建服务器
        resp = client.post(url_for('api.server_list'), data=json.dumps(data), headers=headers)
        # 验证
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        assert resp.status_code == 201
        assert resp.json['ok'] is True
        # 尝试修改服务器
        data = {
            'name': 'redis test',
            # 'description': 'this is a test record',
            # 'host': '127.0.0.1',
            # 'port': '6379',
        }
        resp = client.put(url_for(self.endpoint, object_id=2), data=json.dumps(data), headers=headers)
        # 修改失败

        assert resp.status_code == 400
        assert resp.json['ok'] is False
        assert resp.json['message'] == 'Redis server already exists'

    def test_delete_success(self, server, client):
        """删除 Redis 服务器成功
        """
        # 获取 object_id == 1 的服务器
        resp = client.get(url_for(self.endpoint, object_id=1))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        assert resp.json['name'] == 'redis test'

        # 尝试删除服务器
        resp = client.delete(url_for(self.endpoint, object_id=1))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        assert resp.json['ok'] is True

    def test_delete_failed_with_host_not_exist(self, db, client):
        """删除不存在的 Redis 服务器失败
        """
        # 验证 object_id == 0 的服务器不存在
        resp = client.get(url_for(self.endpoint, object_id=0))

        assert resp.status_code == 404
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        assert resp.json['ok'] is False
        assert resp.json['message'] == 'object doesn\'t exist'

        # 尝试删除之
        resp = client.delete(url_for(self.endpoint, object_id=0))
        assert resp.status_code == 404
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        assert resp.json['ok'] is False
        assert resp.json['message'] == 'object doesn\'t exist'
