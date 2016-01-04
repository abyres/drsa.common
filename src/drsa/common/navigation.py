from pysiphae.interfaces import INavigationProvider, IHomeViewResolver
from pysiphae.decorators import home_url
from zope.interface import implements

class NavigationProvider(object):
    implements(INavigationProvider)

    def get_links(self):
        return []

