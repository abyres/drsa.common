from pyramid.view import view_config
from sqlalchemy.engine import create_engine
from pyramid.exceptions import NotFound
from wraptor.decorators import memoize
from sqlalchemy.sql import text

@view_config(route_name='drsa.home',
        renderer='templates/home.pt',
        permission='pysiphae.View')
def home_view(context, request):
    items = request.main_navigation
    items = filter(lambda x: x.get('type','item') == 'item', items)
    dashboards = [{'title': i['label'], 'url': i['href']} for i in items]
    return {
        'dashboards': dashboards
    }


@view_config(name="drsa.common.links",
        renderer='templates/links.pt',
        permission='pysiphae.View')
def links(context, request):
    return {}
