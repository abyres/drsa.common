from pyramid.view import view_config
from sqlalchemy.engine import create_engine
from pyramid.exceptions import NotFound
from pyramid.security import NO_PERMISSION_REQUIRED
from wraptor.decorators import memoize
from sqlalchemy.sql import text
from repoze.who.api import get_api as get_whoapi
import requests
from pyramid.httpexceptions import HTTPFound

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

@view_config(name='drsa.common.transparentlogo',
        renderer='templates/logo.pt',
        permission=NO_PERMISSION_REQUIRED)
def logo(context, request):
    return {}

@view_config(name='drsa.common.grouplogo',
        renderer='templates/grouplogo.pt',
        permission=NO_PERMISSION_REQUIRED)
def grouplogo(context, request):
    return {}

@view_config(name='drsa.common.userprofile',
        renderer='templates/userprofile.pt')
def userprofile(context, request):
    result = {
        'displayname': None,
        'username': None
    }
    user = request.getAuthenticatedUser()
    if not user:
        return {}

    identity = user['identity']
    result['username'] = user['userid']
    if identity.get('givenName', None):
        result['displayname'] = identity['givenName'][0]
    return result

@view_config(route_name='drsa.common.changepassword',
        renderer='templates/changepassword.pt')
def changepass(context, request):
    if 'form.cancelled' in request.params:
        return HTTPFound(location='/')
    if 'form.submitted' in request.params:
        old = request.params.get('old-password', '')
        new = request.params.get('new-password', '')
        confirm = request.params.get('confirm-password','x')
    
        who_api = get_whoapi(request.environ)
        user = request.getAuthenticatedUser()
        authenticated, headers = who_api.login({'login': user['userid'], 'password':
            old})
        if not authenticated:
            request.flash_message('error', 'Invalid password')
            return {}
        if new != confirm:
            request.flash_message('error', 'Passwords does not match')
            return {}
        
        resp = requests.post(
                'https://ipa01.drsa.mampu.gov.my/ipa/session/change_password', 
                verify=False,
                data={'user': user['userid'], 'old_password': old, 'new_password':
                    new})
        if not 'Password change successful' in resp.text:
            request.flash_message('error', resp.text)
            return {}
            
        request.flash_message('success', 'Password Changed')
        return HTTPFound(location='/')

    return {}
