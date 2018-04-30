from rmon.models import Server 
from rmon.common.rest import RestException


class TestServer:
    """
    test Server functionality 
    """
    
    def test_save(self, db):
        """
        test Server.save()
        """

        assert Server.query.count() == 0 

        server = Server(name='test', host='127.0.0.1')

        server.save()

        assert Server.query.count() == 1

        assert Server.query.first() == server 


    def test_delete(self, db, server):

        assert Server.query.count() == 1
        server.delete()
        assert Server.query.count() == 0

    def test_ping_success(self, db, server):
        """when Server.ping method succeeds
            make sure Redis service is monitoring 127.0.0.1:6379
            """
        assert server.ping() is True 

    def test_ping_failure(self, db):
        """
            when Server.ping fails 
            it raises RestException 
            """
        server = Server(name='test', host='127.0.0.1', port=6399)

        try:
            server.ping()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'cannot connect to redis server {}'.format(server.host)

    def test_get_metrics_success(self, server):
        assert server.get_metrics()['arch_bits'] == 64

    def test_get_metrics_failure(self, db):
        server = Server(name='test', host='127.0.0.1', port=6399)
        try:
            server.get_metrics()
        except RestException as e:
            assert e.code == 400
            assert e.message == 'cannot connect to redis server {}'.format(server.host)
        
        