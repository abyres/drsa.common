from pyramid.view import view_config
from pysiphae.views import Views as BaseViews
from sqlalchemy.engine import create_engine
from pyramid.exceptions import NotFound
from wraptor.decorators import memoize
from sqlalchemy.sql import text

class Views(BaseViews):

    @view_config(route_name='drsa.home',
            renderer='templates/home.pt',
            permission='pysiphae.View')
    def home_view(self):
        items = self.main_navigation
        dashboards = [{'title': i['label'], 'url': i['href']} for i in items]
        return {
            'dashboards': dashboards
        }

