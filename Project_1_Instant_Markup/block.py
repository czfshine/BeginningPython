# -*- coding: utf-8 -*-

#文件行迭代器
def lines(file):
    #弹出文件的每一行
    for line in file.readlines(): yield line
    #最后要弹出一个空行，标志着最后一个块结束
    yield "\n"
        
#文件块迭代器
def blocks(file):
    #用来临时存放文本块
    block =[]
    #迭代每一行
    for line in lines(file):
        #判断是不是空行
        if line.strip():
            #print  line.strip()
            #把非空行加入文本块
            block.append(line)
        #如果文本块不为空的话
        elif block:
            #以字符串的形式弹出块
            yield ''.join(block).strip()
            #清空文本块            
            block = []

#测试
#下面的代码只有直接运行时才会执行
if __name__ == '__main__':
    #打开测试文件
    infile=open("input.txt","r")
    #看分块情况
    print [s for s in blocks(infile)]