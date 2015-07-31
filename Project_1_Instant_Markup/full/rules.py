# -*- coding: utf-8 -*-

class Rule:
    """
    所有规则的基类
    """
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    """
    标题是独立一行且小于70字的块，也不是以冒号结束。
    """
    type = 'heading'
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    """
    题目是第一次个标题
    """
    type = 'title'
    first = True
    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)
        
class ListItemRule(Rule):
    """
    列表项
    """
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        for item in block.split("\n"):
            handler.start(self.type)
            handler.feed(item[1:].strip())
            handler.end(self.type)
        return True

class ListRule(ListItemRule):
    """
    列表
    """
    type = 'list'
    inside = False
    def condition(self, block):
        return True
    def action(self, block, handler):
        if not self.inside and ListItemRule.condition(self, block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self, block):
            handler.end(self.type)
            self.inside = False
        return False
class ParagraphRule(Rule):
    """
    默认
    """
    type = 'paragraph'
    def condition(self, block):
        return True
