# -*- coding: utf-8 -*-
from sys import  stdout, modules

#配置
_doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
_charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />\n'

#所有标签，用来自动生成标签类
_tags = ['html', 'body', 'head', 'link', 'meta', 'div', 'p', 'form', 'legend', 
        'input', 'select', 'span', 'b', 'i', 'option', 'img', 'script',
        'table', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'fieldset', 'a', 'title', 'body', 'head', 'title', 'script', 'br', 'table',
        'ul', 'li', 'ol']

#独立标签
_selfClose = ['input', 'img', 'link', 'br']


class Tag(list):
    '''
    所有标签的父类
    '''
    tagname = ''
    def __init__(self, *arg, **kw):
        self.attributes = kw
        if self.tagname : 
            name = self.tagname
            self.isSeq = False
        else: 
            name = 'sequence'
            self.isSeq = True
        self.id = kw.get('id', name)
        #self.extend(arg)
        for a in arg: self.addObj(a)

    def __iadd__(self, obj):
        '''
        自增操作
        '''
        if isinstance(obj, Tag) and obj.isSeq:
            for o in obj: self.addObj(o)
        else: self.addObj(obj)
        return self
    
    def addObj(self, obj):
        '''
        增加子对象
        '''
        if not isinstance(obj, Tag): obj = str(obj)
        # 设置id        
        id=self.setID(obj)
        #以id当做索引        
        setattr(self, id, obj)
        self.append(obj)

    def setID(self, obj):
        '''
        给每个子对象设置一个id
        '''
        if isinstance(obj, Tag):
            id = obj.id
            n = len([t for t in self if isinstance(t, Tag) and t.id.startswith(id)])
        else:
            id = 'content'
            n = len([t for t in self if not isinstance(t, Tag)])
        if n: id = '%s_%03i' % (id, n)
        if isinstance(obj, Tag): obj.id = id
        return id

    def __add__(self, obj):
        '''
        重载+运算符，在该标签内加上子标签。
        '''
        if self.tagname: return Tag(self, obj)
        self.addObj(obj)
        return self

    def __lshift__(self, obj):
        '''
        重载<<运算符，替代二元运算符+，在该标签内加上子标签。
        '''
        self += obj
        if isinstance(obj, Tag): return obj

    def render(self):
        '''
        生成该标签对应的字符串
        '''
        result = ''
        if self.tagname:
            result = '<%s%s%s>' % (self.tagname, self.renderAtt(), self.selfClose()*' /')
        if not self.selfClose():
            for c in self:
                if isinstance(c, Tag):
                    result += c.render()
                else: result += c
            if self.tagname: 
                result += '</%s>' % self.tagname
        result += '\n'
        return result

    def renderAtt(self):
        '''
        输出标签属性对应的字符串
        '''
        result = ''
        for n, v in self.attributes.iteritems():
            if n != 'txt' and n != 'open':
                if n == 'cl': n = 'class'
                result += ' %s="%s"' % (n, v)
        return result

    def selfClose(self):
        '''
        是否属于独立标签
        '''
        return self.tagname in _selfClose        
    
#生成标签类
def TagFactory(name):
    class f(Tag):
        tagname = name
    f.__name__ = name
    return f

#得到该模块的命名空间
thisModule = modules[__name__]

#迭代所有标签名，生成对应的标签类，并加入到模块的命名空间里面
for t in _tags: setattr(thisModule, t, TagFactory(t)) 


class html(Tag):
    '''
    html标签类
    '''
    tagname = 'html'
    
    def __init__(self, name='MyPyHPage'):
        self += head()
        self += body()
        self.attributes = dict(xmlns='http://www.w3.org/1999/xhtml', lang='en')
        self.head += title(name)

    def __iadd__(self, obj):
        if isinstance(obj, head) or isinstance(obj, body): self.addObj(obj)
        elif isinstance(obj, meta) or isinstance(obj, link): self.head += obj
        else:
            self.body += obj
            id=self.setID(obj)
            setattr(self, id, obj)
        return self

    def addJS(self, *arg):
        for f in arg: self.head += script(type='text/javascript', src=f)

    def addCSS(self, *arg):
        for f in arg: self.head += link(rel='stylesheet', type='text/css', href=f)
    
    def printOut(self,file=''):
        '''
        输出网页
        '''
        if file: f = open(file, 'w')
        else: f = stdout
        f.write(_doctype)
        f.write(self.render())
        f.flush()
        if file: f.close()

if __name__=="__main__":
    #新建html页面
    page = html('My wonderful PyH page')
    #增加css和js
    page.addCSS('myStylesheet1.css', 'myStylesheet2.css')
    page.addJS('myJavascript1.js', 'myJavascript2.js')
    #可以用左移操作符把内容加入
    page << h1('My big title', cl='center')
    #连续多个
    page << div(cl='myCSSclass1 myCSSclass2', id='myDiv1') << p('I love PyH!', id='myP1')
    #会返回对象
    mydiv2 = page << div(id='myDiv2')
    #可以直接在对象里加入
    #+代表两个对象并列
    mydiv2 << h2('A smaller title') + p('Followed by a paragraph.')
    #给对象加id可以用来做索引
    page << div(id='myDiv3')
    #直接用id索引
    #直接修改属性
    page.myDiv3.attributes['cl'] = 'myCSSclass3'
    #当然代表了那个对象
    page.myDiv3 << p('Another paragraph')
    #输出
    page.printOut()
      