"""rmon.views.urls 
defined urls for APIs
"""

from flask import Blueprint 
from rmon.views.index import IndexView
from rmon.views.server import ServerList, ServerDetail


# 'api' is the Blueprint name 
api = Blueprint('api', __name__)

# IndexView will be used as 'index', 
# for example, url_for('api.index')
api.add_url_rule('/', view_func=IndexView.as_view('index'))
api.add_url_rule('/servers', view_func=ServerList.as_view('server_list'))
api.add_url_rule('/servers/<int:object_id>', view_func=ServerDetail.as_view('server_detail'))

