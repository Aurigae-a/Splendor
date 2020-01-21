import pygame as pg
from pygame.locals import *

class TextField:
    """
    这个类用来实现可视化窗口中的文字输入框
    """
    def __init__(self,parent):
        """
        实现文本框的初始设置
        """
        # 文本框的父对象
        self.parent = parent
    
    def initialization(self,x,y,width,height,status_x,status_y,max_len,eff_in,font,cursor_width):
        """
        生成文本框的几何尺寸
        """
        # 文本框的水平和竖直位置
        self.pos = [x,y]
        # 文本框的水平方向和竖直方向宽度
        self.size = [width,height]
        # 文本框的状态的显示位置
        self.status_pos = [status_x,status_y]
        # 文本框的底色背景矩形
        self.bg_rect = pg.Rect((self.pos[0], self.pos[1], self.size[0], self.size[1]))
        # 文本框的文字字体
        self.font = font
        
        """
        生成文本框的内容信息
        """
        # 文本框的有效长度
        self.text_length = 0
        # 文本框是否被选中
        self.enable = False
        # 第一个文本框的指定输入上限
        self.text_max_len = max_len
        # 文本框的内容
        self.text = []
        for index in range(self.text_max_len):
            self.text.append(' ')
        # 规定文本框所允许的所有字符
        self.eff_in = []
        for index in range(len(eff_in)):
            self.eff_in.append(eff_in[index])
        
        """
        生成光标的信息
        """
        self.cursor = 0
        self.cursor_size = [cursor_width,self.size[1]]

    def inRange(self,pos):
        """
        主要用来检测某一位置是否在文本框范围中
        """
        if (pos[0]>self.pos[0] and pos[0]<self.pos[0]+self.size[0] and 
            pos[1]>self.pos[1] and pos[1]<self.pos[1]+self.size[1]):
            return True
        else:
            return False
    
    def keyTapIn(self,event):
        """
        用来处理键盘输入事件
        """
        # 判断当前文本框是否被选中
        if self.enable:
            # 判断按键是否是功能键
            if len(event.unicode) != 0:
                # 获得当前键的unicode值
                char = event.unicode[0]

                # 判断该字符是否是有效字符
                if self.isEffective(char) and self.text_length<self.text_max_len:
                    # 光标之后的数字依次向后移动一位
                    for index in range(self.text_length-self.cursor):
                        self.text[self.text_length-index] = self.text[self.text_length-index-1]
                    # 在光标位置插入数字
                    self.text[self.cursor] = event.unicode[0]
                    self.cursor = self.cursor + 1
                    # 长度增长
                    self.text_length = self.text_length + 1
                    
                # 退格键被按下
                elif event.key == K_BACKSPACE and self.cursor>0:
                    # 光标之后的每一项向前移动一位
                    for index in range(self.text_max_len-self.cursor):
                        self.text[self.cursor+index-1] = self.text[self.cursor+index]
                    # 在结尾处插入空白符
                    self.text[-1] = ' '
                    self.cursor = self.cursor - 1
                    # 长度减小
                    self.text_length = self.text_length - 1
                
                # 键盘向左键被按下
                elif event.key == K_LEFT and self.cursor>0:
                    self.cursor = self.cursor - 1
                
                # 键盘向右键被按下
                elif event.key == K_RIGHT and self.cursor<self.text_length:
                    self.cursor = self.cursor + 1

    def isNumber(self,char):
        """
        判断该字符是否是数字0～9
        """
        char_num = char.encode(encoding='utf-8')[0]
        comp_num = b'0'[0]
        if char_num-comp_num >-1 and char_num-comp_num < 10:
            return True
        else:
            return False

    def isLowercase(self,char):
        """
        判断该字符是否是小写字母a～z
        """
        char_num = char.encode(encoding='utf-8')[0]
        comp_num = b'a'[0]
        if char_num-comp_num >-1 and char_num-comp_num < 26:
            return True
        else:
            return False

    def isUppercase(self,char):
        """
        判断该字符是否是小写字母A～Z
        """
        char_num = char.encode(encoding='utf-8')[0]
        comp_num = b'A'[0]
        if char_num-comp_num >-1 and char_num-comp_num < 26:
            return True
        else:
            return False

    def isEffective(self,char):
        """
        判断输入的字符是否是该文本框所允许输入的字符
        """
        isEff = False
        for obj_char in self.eff_in:
            if char == obj_char:
                isEff = True
                break
        
        return isEff

    def show(self):
        """
        将该文本框渲染出来
        """
        # 画背景底色
        pg.draw.rect(self.parent, pg.Color("red"), self.bg_rect)
        # 渲染具体的字符串
        text_str = self.font.render("".join(self.text),False,pg.Color("blue"))
        self.parent.blit(text_str, (self.pos[0],self.pos[1]))
        # 画出状态栏
        if self.enable == True:
            self.parent.blit(self.font.render("Tap in",False,pg.Color('green')),(self.status_pos[0],self.status_pos[1]))
        else:
            self.parent.blit(self.font.render("Locked",False,pg.Color('green')),(self.status_pos[0],self.status_pos[1]))

        # 画出光标
        if self.enable:
            # 计算初始位置
            cursor_x = self.pos[0]
            cursor_y = self.pos[1]
            # 根据文字长度计算位置
            for index in range(self.cursor):
                if self.isNumber(self.text[index]):
                    # 数字
                    cursor_x = cursor_x + 11
                elif self.isLowercase(self.text[index]):
                    # 小写字母
                    cursor_x = cursor_x + 12
                elif self.isUppercase(self.text[index]):
                    # 大写字母
                    cursor_x = cursor_x + 14
                elif self.text[index] == ".":
                    cursor_x = cursor_x + 5
                else:
                    cursor_x = cursor_x + 0
            # 画
            pg.draw.rect(self.parent, pg.Color('yellow'), (cursor_x,cursor_y,self.cursor_size[0],self.cursor_size[1]))

    def getText(self,rtype):
        """
        返回这个文本输入框中的内容
        """
        text_str = ""
        # 获得字符串
        for index in range(self.text_length):
            text_str = text_str + str(self.text[index])
        
        """
        rtype=0: 以字符串的形式返回
        """
        if rtype == 0:
            return text_str
        
        """
        rtype=1: 以整数的形式返回
        """
        if rtype == 1:
            try:
                text_int = int(text_str)
                return text_int
            except ValueError:
                return "-1"

class Label:
    """
    这个类是用来实现文字标签
    """
    def __init__(self,parent):
        """
        初始化函数，设置父对象
        """
        self.parent = parent
    
    def initialization(self,x,y,text,font,color):
        """
        对文本标签实现初始化
        """
        # 设置位置
        self.pos = [x,y]
        # 设置文本内容
        self.text = text
        # 设置文字的字体
        self.font = font
        # 设置文字的颜色
        self.color = color
    
    def set_text(self,text):
        """
        从外界对该标签的显示内容进行修改
        """
        self.text = text
    
    def show(self):
        """
        文本显示
        """
        self.parent.blit(self.font.render(self.text,False,self.color),(self.pos[0],self.pos[1]))

class PushButton:
    """
    这个类用来表示按钮
    """
    def __init__(self,parent):
        """
        初始化函数，对父对象进行分配
        """
        self.parent = parent

    def initialization(self,x,y,text,font,font_color,bg_color):
        """
        对按钮实现初始化
        """
        # 设置位置
        self.pos = [x,y]
        # 设置文本内容
        self.text = text
        # 设置文字的字体
        self.font = font
        # 设置文字的颜色
        self.color = [font_color, bg_color]

        # 对按钮进行渲染
        self.button = self.font.render(self.text,False,self.color[0],self.color[1])
        # 获得按钮的背景方块
        self.rect = self.button.get_rect()
        # 获得按钮的大小
        self.size = [self.rect.width, self.rect.height]
    
    def show(self):
        """
        将按钮进行可视化
        """
        self.parent.blit(self.button, (self.pos[0],self.pos[1]))
    
    def inRange(self,pos):
        """
        判断指定的位置是否在按钮的范围中
        """
        if (pos[0]>self.pos[0] and pos[0]<self.pos[0]+self.size[0] and
            pos[1]>self.pos[1] and pos[1]<self.pos[1]+self.size[1]):
            return True
        else:
            return False

class NumberSelector:
    """
    这个类用来实现通过点击鼠标来改变数字
    """
    def __init__(self,parent):
        """
        初始化函数,设置显示时候需要的父对象
        """
        self.parent = parent
    
    def initialization(self,x,y,width,height,font,button_color,font_color):
        """
        数字选择按钮的初始化函数
        """
        # 数字选择按钮左上角的位置
        self.pos = [x,y]
        # 数字选择按钮的大小
        self.size = [width,height]
        # 左侧三角形的三个点的位置
        self.left_tri_point = [[0,self.size[1]/2],[self.size[0]/3,0],[self.size[0]/3,self.size[1]]]
        # 右侧三角形的三个点的位置
        self.right_tri_point = [[self.size[0]*2/3,0],[self.size[0]*2/3,self.size[1]],[self.size[0],self.size[1]/2]]
        # 三角形的正负斜率
        self.pos_slope = self.size[1]*3/(2*self.size[0])
        # 字体的类型和颜色
        self.font = font
        self.font_color = font_color
        # 按钮的颜色
        self.button_color = button_color
        # 数值
        self.num = 0
        # 数值的下限与上限
        self.num_min = 0
        self.num_max = 0
        # 该数字选择器的底层surface
        self.object = pg.Surface(self.size)
        # 控制该数字选择器是否进行绘画
        self.enable = False

    def show(self):
        """
        在图形可视化界面中画出这个按钮
        """
        if self.enable:
            # 画背景图
            self.object.fill((0,0,0))
            # 画出左三角
            pg.draw.polygon(self.object,self.button_color,self.left_tri_point)
            # 画出右三角
            pg.draw.polygon(self.object,self.button_color,self.right_tri_point)
            # 渲染文字
            self.object.blit(self.font.render(str(self.num),False,self.font_color),(self.size[0]*3/7,0))
            # 将整个图像渲染到主界面上
            self.parent.blit(self.object,self.pos)

    def set_range(self,num_min,num_max):
        """
        对数字选择器的选择范围进行限定
        """
        self.num_min = num_min
        self.num_max = num_max
        self.num = self.num_min
        self.enable = True
    
    def checkMouseEvent(self,pos):
        """
        对鼠标事件进行的相应的操作
        """
        if (pos[1] > self.left_tri_point[0][1]-(pos[0]-self.left_tri_point[0][0])*self.pos_slope and 
            pos[1] < self.left_tri_point[0][1]+(pos[0]-self.left_tri_point[0][0])*self.pos_slope and 
            pos[0] < self.left_tri_point[1][0]):
            # 左箭头被选中
            if self.num > self.num_min:
                self.num = self.num - 1

        if (pos[1] > self.right_tri_point[2][1]-(self.right_tri_point[2][0]-pos[0])*self.pos_slope and 
            pos[1] < self.right_tri_point[2][1]+(self.right_tri_point[2][0]-pos[0])*self.pos_slope and 
            pos[0] > self.right_tri_point[0][0]):
            # 右箭头被选中
            if self.num < self.num_max:
                self.num = self.num + 1

