"""rmon.views.index
the view for index 
"""

from flask import render_template 
from flask.views import MethodView

class IndexView(MethodView):
    """index view 
    """

    def get(self):
        """
        render template 
        called when requested by the "GET" method 
        """
        return render_template('index.html')
