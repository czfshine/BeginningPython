# -*- coding: utf-8 -*-

from pylab import *
from scipy import stats

def showbardata(x_data,y_data,hastext=False,xticks=False,size=(4,4)):
    '''
    以条形图显示数据
    '''
    
    #统一类型
    if type(x_data) =="<type 'numpy.ndarray'>":
        x_data=x_data.tolist() 
    if type(y_data) =="<type 'numpy.ndarray'>":
        y_data=y_data.tolist()
    
    #初始化数据，长度要一致，用0补足。
    n=len(x_data)
    ym=len(y_data)
    if ym< n:
        y_data+=[0]*(n-ym)
    
    #图片画布
    figure(figsize=size, dpi=80)
    #生成数据
    X = np.array(x_data)
    Y= np.array(y_data)
    #画布子区
    axes([0.025,0.025,0.95,0.95])
    #画条形图
    bar(X,+Y, facecolor='#9999ff',width=0.9, edgecolor='white')
    
    #数值文字
    if hastext :
        Xpos=np.arange(n)
        for x,y in zip(Xpos,Y):
            text(x+0.4, y+min(y_data), '%.2f' % y, ha='center', va= 'bottom')
    #x轴，如果太多就把xticks设置为False，不显示x轴
    if xticks:
        #x坐标轴标记位置，向右移0.5单位，才能居中
        xtickspos=[0.0]*n
        for num in range(n):
            xtickspos[num]=num+0.5
        #x坐标轴数据
        xlim(0,n)
        #       位置       显示
        xticks(xtickspos,x_data)
    #y轴数据
    ylim(0,max(y_data)*1.1)
    yticks([0,max(y_data)])
    
    #坐标轴
    ax = gca()
    #上和右没有
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    #x置于最下面
    ax.xaxis.set_ticks_position('bottom')
    #ax.xaxis.set_major_locator(AutoLocator())
    ax.spines['bottom'].set_position(('data',0))
    #y轴
    ax.yaxis.set_ticks_position('left')
    #自动调整数值间距
    ax.yaxis.set_major_locator(AutoLocator())
    ax.spines['left'].set_position(('data',0)) 
    #画
    show()

#test
#
#'''
#with plt.xkcd():
#    for n1 in range(20,200,40):
#         k = np.arange(n1+1)
#         pcoin = stats.binom.pmf(k, n1, 0.5)
#         showbardata(range(n1+1),pcoin)
#'''
if __name__ =="__main__":
    '''
    以xkcd风格绘制二项分布列条形图
    '''
    with plt.xkcd():
        n1=10
        k = np.arange(n1+1)
        pcoin = stats.binom.pmf(k, n1, 0.5)
        showbardata(range(n1+1),pcoin)
