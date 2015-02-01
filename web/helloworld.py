import webapp2
from webob import Request
from google.appengine.ext import ndb

MAIN_PAGE_HTML = """\
<html>
    <body>
    <form action="/search" method="post">
    <div><input type="text" name="name"></div>
    <div><input type="submit" value="Search"></div>
    </form>
    </body>
</html>
"""

class Data(ndb.Model):
    ip = ndb.StringProperty(indexed=False);
    name = ndb.StringProperty(indexed=False);
    date = ndb.DateTimeProperty(auto_now_add=True);


class MainPage(webapp2.RequestHandler):
    def get(self):
        #ip = self.request.remote_addr;
        #self.response.headers['Content-Type'] = 'text/plain';
        #self.response.write('[' + ip +']:Hello, World!');
        self.response.write(MAIN_PAGE_HTML);

class RecordIP(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name');
        ip = self.request.remote_addr;
        self.response.headers['Content-Type'] = 'text/plain';
        self.response.write('[' + ip +']\t' + name +'\t');

        ndb_ip_addr = ndb.Key('IP_RECORD','record');
        data = Data(parent = ndb_ip_addr);
        data.ip = ip;
        data.name = name;
        data.put();

class SearchRecord(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/plain';
        name = self.request.get('name');

        ndb_ip_addr = ndb.Key('IP_RECORD','record');
        datas_query = Data.query(ancestor = ndb_ip_addr).order(-Data.date);
        datas = datas_query.fetch(10);

        for data in datas:
            if data.name == name:
                ip = data.ip;
                date = data.date;
                self.response.write(str(date) + '\t[' + ip +']\t' + name +'\n');

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/record', RecordIP),
    ('/search', SearchRecord),
    ], debug=True);
