import os
import webapp2
import jinja2
import cgi
import re
from google.appengine.ext import db
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
class Handler(webapp2.RequestHandler):
    def renderError(self, error_code):
        self.error(error_code)
        self.response.write("Oops! Something went wrong.")
class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", post = self)

class HomePage(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post  order by created desc LIMIT 5")
        t = jinja_env.get_template("base.html")
        content = t.render(posts = posts)
        self.response.write(content)
class PostHandler(webapp2.RequestHandler):
    def get(self, id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        self.render("permalink.html", post = post)
class NewPost(webapp2.RequestHandler):
    def get(self):

        t = jinja_env.get_template("post.html")
        content = t.render(post = self)
        self.response.write(content)
    def post(self):
        title = self.request.get("title")
        body = self.request.get("body")
        post = Post(parent=blog_key(), title=title, body=body)
        post.put()
        self.redirect('/blog/?%s' % str(post.key().id()))


app = webapp2.WSGIApplication([
    ('/blog/?', HomePage),
    ('/blog/([0-9]+)', PostHandler),
    ('/blog/newpost/?', NewPost)

], debug=True)
