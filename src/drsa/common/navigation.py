from pysiphae.interfaces import INavigationProvider, IHomeViewResolver
from pysiphae.decorators import home_url
from zope.interface import implements

class NavigationProvider(object):
    implements(INavigationProvider)

    def get_links(self):
        return [{
            'href': '/drsa.common',
            'label': 'drsa.common Dashboard',
            'order': 1
        }]

@home_url
def get_home_url(request, groups):
    return request.resource_url(request.context, 'drsa.common')
