# -*- coding: utf-8 -*-

class Handler:
    """
    An object that handles method calls from the Parser.
    The Parser will call the start() and end() methods at the
    beginning of each block, with the proper block name as a
    parameter. The sub() method will be used in regular expression
    substitution. When called with a name such as 'emphasis', it will
    return a proper substitution function.
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method): return method(*args)
    def start(self, name):
        self.callback('start_', name)
    def end(self, name):
        self.callback('end_', name)
    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: match.group(0)
            return result
        return substitution

def getoutput(filename="temp",tofile=False):
    '''
    得到输出函数，
    如果tofile参数为true，则输出到文件，
    不然输出到标准输出文件
    '''
    if tofile:
        outfile=open(filename,"wb")
        def output(data):
            '''
            数据统一用这个函数输出到指定文件
            '''
            try :
                outfile.write(str(data))
            except:
                pass
    else:
        def output(data):
            '''
            数据统一用这个函数输出到标准输出文件
            '''
            print str(data)
    return output

class HTMLRenderer(Handler):
    """
    A specific handler used for rendering HTML.
    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end(), and sub() methods. They implement basic
    markup as used in HTML documents.
    """
    def __init__(self):
        self.o=getoutput()
    def start_document(self):
        self.o('<html><head><title>...</title></head><body>')
    def end_document(self):
        self.o('</body></html>')
    def start_paragraph(self):
        self.o('<p>')
    def end_paragraph(self):
        self.o('</p>')
    def start_heading(self):
        self.o('<h2>')
    def end_heading(self):
        self.o('</h2>')
    def start_list(self):
        self.o('<ul>')
    def end_list(self):
        self.o('</ul>')
    def start_listitem(self):
        self.o('<li>')
    def end_listitem(self):
        self.o('</li>')
    def start_title(self):
        self.o('<h1>')
    def end_title(self):
        self.o('</h1>')
    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, data):
        self.o(data)


