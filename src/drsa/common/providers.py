from zope.interface import Interface
import urllib

class SASIFrameProvider(object):
   
    def __init__(self, title, report_path, report_name,
        server=None, height=500, anonymous=True):
        self.title = title
        self.report_path = report_path
        self.report_name = report_name
        self.server = server
        self.height = height
        self.server = None
        self.anonymous = anonymous

    def iframe_url(self, request):
        server = self.server
        if not server:
            server = request.registry.settings.get('drsa.sas.url', '')
        server_url = server.strip().split("/")
        if self.anonymous:
            va_path = ["SASVisualAnalyticsViewer",
                    "VisualAnalyticsViewer_guest.jsp"]
        else:
            va_path = ["SASVisualAnalyticsViewer",
                   "VisualAnalyticsViewer.jsp"]
        reportPath = self.report_path.strip().replace(" ","+")
        reportName = self.report_name.strip().replace(" ","+")

        url = '/'.join(server_url + va_path)
        param = {
            "reportPath": reportPath,
            "reportName": reportName,
            "appSwitcherDisabled": "true",
            "reportViewOnly": "true"
        }

        return url + "?" + urllib.urlencode(param)

    def iframe_style(self, request):
        return "height:%spx;width:100%%" % self.height 

    def iframe(self, request):
        return '''<iframe src="%s" style="%s" frameborder="0"></iframe>''' % (
            self.iframe_url(request), self.iframe_style(request)
        )

    def asDict(self, request):
        return {
            'title': self.title,
            'iframe_url': self.iframe_url(request),
            'iframe_style': self.iframe_style(request)
        }

