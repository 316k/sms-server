from html.parser import HTMLParser

class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
        self.ignore = 0
        self.ignore_tags = ['script', 'head', 'table', 'ul']

    def handle_starttag(self, tag, attrs):
        print('start', tag)
        if tag in self.ignore_tags:
            self.ignore += 1

    def handle_endtag(self, tag):
        if tag in self.ignore_tags:
            self.ignore -= 1

    def handle_data(self, d):
        if not self.ignore:
            self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()

