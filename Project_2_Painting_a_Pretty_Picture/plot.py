# -*- coding: utf-8 -*-


from pylab import *
from githubdata import GitHubData
from bar import showbardata

def toarray(commit):
    '''
    将提交参数转换成X，Y轴数据
    '''
    counts=[int(a) for a,b in commit]
    return np.arange(len(counts)),np.array(counts)
    
def plotbar(commit):
    '''
    绘制条形图
    数据量大时，把size设置大一点
    '''
    showbardata(toarray(commit),size=(32,8))

def plotline(commit):
    '''
    绘制折线图
    '''
    X,Y=toarray(commit)
    plot(Y)
    show()


if __name__ =="__main__":
    '''
    装载数据，绘制两种图形
    '''
    odj=GitHubData()
    if odj.load():
        plotdata(odj.get())
        plotline(odj.get())
