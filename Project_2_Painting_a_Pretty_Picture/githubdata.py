# -*- coding: utf-8 -*-

import urllib2
import bs4 as B
import os

class GitHubData:
    '''
    数据类
    用来从github下载用户提交次数的数据
    '''
    def __init__(self,username):
        self.username=username or "czfshine"
        self.commit=[]
    def load(self):
        '''
        装载数据
        如果有数据文件就从文件读取，不然才从github下载
        返回True说明数据载入成功
        '''
        try:
            #尝试从现有数据文件读取
            f=open("test.dat")
            self.commit=eval(f.read())
            return True
        except:
            try:
                #尝试下载并解析
                page=urllib2.urlopen("https://github.com/"+self.username).read()
                #用库解析html文件，方便处理
                S = B.BeautifulSoup(page)
                #在页面中寻找指定的Dom
                D=S.find(class_='js-calendar-graph-svg').find_all("rect")
                for d in D :
                    #把所有的Dom中的数据压入列表中
                    self.commit.append((d.attrs['data-count'] or 0,d.attrs['data-date']))
                return True
            except:
                return False
            
    def save(self):
        '''
        将数据保存进文件，防止重复下载数据，提高运行速度
        '''
        try :
            f=open("test.dat","wb")
            f.write(str(self.commit))
            f.close()
            return True
        except:
            return False
    def get(self):
        '''
        返回数据
        数据为二元组列表：
        [(str提交数量,str时间<2015-07-05>),...]
        '''
        return self.commit
    def clean(self):
        '''
        清空本地数据文件
        '''
        try:
            os.remove("./test.dat")
        except:
            pass

if __name__=="__main__" :
    '''
    测试
    '''
    #模拟第一次载入数据，从互联网下载
    test=GitHubData()
    test.clean()
    print test.load() and  "1st load data succes" or "1st load data fail"
    print test.save() and  "1st save data succes" or "1st save data fail"
    print test.get()  and  "1st get data succes"  or "1st get data fail"
    
    #模拟第二次载入数据，从文件装载
    test=None
    test=GitHubData()
    test.load()      and  "2nd load data succes" or "2nd load data fail"
    print test.get() and  "2nd get data succes"  or "2nd get data fail"