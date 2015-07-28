# -*- coding: utf-8 -*-
#最小实现

from block import *
import sys,re

#html文件的头部和尾部
head=r"<html><head><title>...</title><body>"
ends=r"</body></html>"


#处理文件块
def mark(Blocks):
    #假设第一块为大标题
    Blocks[0]='<h1>'+Blocks[0]+'</h1>'
    #给每一块加上段落标记
    for num in range(len(Blocks)-1):
        #处理斜体
        Blocks[num+1] = re.sub(r'\*(.+?)\*', r'<em>\1</em>',Blocks[num+1])
        Blocks[num+1]='<p>'+Blocks[num+1]+'</p>'
    

if __name__ == '__main__':
    #打开测试文件
    infile=open("input.txt","r")
    Blocks=[s for s in blocks(infile)]
    mark(Blocks)
    print head
    for block in Blocks:
        print block
    print ends
    
        