

from reddit import reddit
from reddit import getFrontPage
from task import Task
import re
from markdown2 import Markdown

class rPost:
    url = ""
    title = ""
    body = ""
    sub = ""
    score = 0
    topComment = ""
    imageUrl = ""

    def __init__(self, title):
        self.title = title
        url = ""
        sub = ""
        self.score = 0
        self.topComment = ""
        self.imageUrl = ""

class Summary(Task):
    tops = []

    def run(self):
        self.update()
        self.title = "Top Posts Of The Day"


    def update(self):
        self.populateTops()
        self.setTaskBody()

    def populateTops(self):
        i = 0
        for item in getFrontPage(limit = 10):
            self.tops.append(rPost(item.title))
            self.tops[i].body = item.selftext
            self.tops[i].score = item.score
            self.tops[i].topComment = self.getTopComment(item)
            self.tops[i].sub = item.subreddit
            self.tops[i].url = item.url
            i+=1

    def getTopComment(self, item):
        for comm in item.comments:
            result = comm.body
            # if "http://" in comm.body:
            try:
                url = re.search("(?P<url>https?://[^\s]+)", result).group("url")
                # print url
                self.imageUrl = re.search("(?P<url>https?://[^\s]+)", result).group("url")

            except:
                continue
            return result

    def setTaskBody(self):
        markdowner = Markdown()
        self.body = ""
        for post in self.tops:
            self.body += "<h3><span style='font-weight:bold; color:orange;'>" + str(post.score) + "</span> : r/" + str(post.sub) + " <a href=" + post.url + ">" + post.title + "</a></h3>"
            self.body += "<p>" + post.body + "</p>"
            self.body += "<div style='margin-left:10px; border-left: 3px solid gray; padding-left: 5px; font-size: 15px;'><p>" + markdowner.convert(post.topComment) + "<img src='" + post.imageUrl + "'>" + '''</p></div>
            '''

    def printTops(self):
        for post in self.tops:
            print str(post.score) + " : " + post.title , " : " , post.topComment
            print ""

summary = Summary()
