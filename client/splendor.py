import pygame as pg
import widget 

class Token:
    """
    客户端中的筹码类，包含其可视化的方法
    """
    # 静态变量
    # 尺寸
    radius = 50
    # 图片
    pic = []
    # 图片加载的位置
    pic_pos = [20,10]
    pic_size = [60,60]
    # 字体
    font = None
    # 数字的位置
    num_pos = [45,70]

    def __init__(self,parent,color,x,y):
        """
        筹码的初始化函数
        """
        # 可视化时候的父对象
        self.parent = parent
        # 颜色
        self.color = color
        # 数量
        self.num = 0
        # 显示时左上角的位置
        self.pos = [x,y]
        # 表示该token是否被选中的标签
        self.selected = False
        # 整体的rect对象
        self.object = pg.Surface((Token.radius*2,Token.radius*2))
    
    @staticmethod
    def initialization():
        """
        这个初始化函数是用来加载静态变量的，在类首次创造对象之前进行执行
        """
        # 加载静态图片
        Token.pic.append(pg.transform.scale(pg.image.load('../pic/green.png').convert(), Token.pic_size))
        Token.pic.append(pg.transform.scale(pg.image.load('../pic/red.png').convert(), Token.pic_size))
        Token.pic.append(pg.transform.scale(pg.image.load('../pic/blue.png').convert(), Token.pic_size))
        Token.pic.append(pg.transform.scale(pg.image.load('../pic/black.png').convert(), Token.pic_size))
        Token.pic.append(pg.transform.scale(pg.image.load('../pic/white.png').convert(), Token.pic_size))
        Token.pic.append(pg.transform.scale(pg.image.load('../pic/gold.png').convert(), Token.pic_size))
        # 加载静态字体
        Token.font = pg.font.Font(None,30)
    
    def update(self,num):
        """
        设置该token的数量
        """
        self.num = num

    def inRange(self,pos):
        """
        判断鼠标点击的位置是否在token的圆中
        """
        dist = ((pos[0]-self.pos[0]-Token.radius)**2 + (pos[1]-self.pos[1]-Token.radius)**2) ** 0.5
        if dist < Token.radius:
            return True
        else:
            return False
    
    def selete(self,cart,type_num_max,remain_num):
        """
        这个函数用来实现token被鼠标选中后的相应操作
        type_num_max 表示cart中最多可以装几种不同的token
        remain_num   表示当这种token大于多少时才可以被选中
        """
        if self.selected == True:
            # 表示当前token已经被选择,则应该取消选择状态，并将其从list中删除
            self.selected = False
            cart.remove(self)
        elif self.num > remain_num and len(cart) < type_num_max:
            # 表示当前token还未被选择，并且满足可选条件
            self.selected = True
            cart.append(self)

    def show(self):
        """
        筹码的可视化函数
        """
        # 画圆
        if self.selected:
            pg.draw.circle(self.object, pg.Color('red'), (Token.radius,Token.radius), Token.radius)
        else:
            pg.draw.circle(self.object, pg.Color('white'), (Token.radius,Token.radius), Token.radius)
        # 画宝石
        self.object.blit(Token.pic[self.color],Token.pic_pos)
        # 画数字
        self.object.blit(Token.font.render(str(self.num),False,pg.Color('blue')),Token.num_pos)
        # 将该图形画到背景上去
        self.parent.blit(self.object,self.pos)
        
class Card:
    """
    客户端中的卡片类，包含其可视化的方法
    """
    # 静态变量
    # 尺寸
    size = [100,160]
    # 图片
    pic_large = []
    pic_small = []
    # 图片加载的位置
    large_pic_pos = [0,0]
    large_pic_size = [60,60]
    small_pic_pos = [[20,70], [20,90], [20,110], [20,130]]
    small_pic_size = [20,20]
    # 分数的位置
    score_pos = [70,15]

    def __init__(self,parent,x,y):
        """
        卡片的初始化函数
        """
        # 可视化时候的父对象
        self.parent = parent
        # 颜色
        self.color = 0
        # 代价
        self.cost = [0,0,0,0,0]
        # 分数
        self.score = 0
        # 显示时左上角的位置
        self.pos = [x,y]
        # 整体的rect对象
        self.object = pg.Surface(Card.size)
        # 表示卡片是否处于激活状态的标志
        self.enable = False
        # 表示卡片收否被选中的标志
        self.selected = False
    
    @staticmethod
    def initialization():
        """
        这个初始化函数是用来加载静态变量的，在类首次创造对象之前进行执行
        """
        # 加载静态图片
        Card.pic_large.append(pg.transform.scale(pg.image.load('../pic/green.png').convert(), Card.large_pic_size))
        Card.pic_large.append(pg.transform.scale(pg.image.load('../pic/red.png').convert(), Card.large_pic_size))
        Card.pic_large.append(pg.transform.scale(pg.image.load('../pic/blue.png').convert(), Card.large_pic_size))
        Card.pic_large.append(pg.transform.scale(pg.image.load('../pic/black.png').convert(), Card.large_pic_size))
        Card.pic_large.append(pg.transform.scale(pg.image.load('../pic/white.png').convert(), Card.large_pic_size))
        Card.pic_small.append(pg.transform.scale(pg.image.load('../pic/green.png').convert(), Card.small_pic_size))
        Card.pic_small.append(pg.transform.scale(pg.image.load('../pic/red.png').convert(), Card.small_pic_size))
        Card.pic_small.append(pg.transform.scale(pg.image.load('../pic/blue.png').convert(), Card.small_pic_size))
        Card.pic_small.append(pg.transform.scale(pg.image.load('../pic/black.png').convert(), Card.small_pic_size))
        Card.pic_small.append(pg.transform.scale(pg.image.load('../pic/white.png').convert(), Card.small_pic_size))
        # 加载静态字体
        Card.font1 = pg.font.Font(None,45)
        Card.font2 = pg.font.Font(None,30)

    def show(self):
        """
        筹码的可视化函数
        """
        if self.enable:
            if self.selected:
                self.object.fill((0,255,0))
            else:
                self.object.fill((255,255,255))
            # 画宝石
            self.object.blit(Card.pic_large[self.color],Card.large_pic_pos)
            # 画分数
            self.object.blit(Card.font1.render(str(self.score),False,pg.Color('black')),Card.score_pos)
            # 画代价
            count = 0
            for index in range(5):
                if self.cost[index] != 0:
                    # 画出小宝石
                    self.object.blit(Card.pic_small[index],Card.small_pic_pos[count])
                    # 画出个数
                    self.object.blit(Card.font2.render(str(self.cost[index]),False,pg.Color('red')),(65,Card.small_pic_pos[count][1]))
                    count = count + 1
            # 将该图形画到背景上去
            self.parent.blit(self.object,self.pos)
    
    @staticmethod
    def decode(msg):
        """
        对描述卡牌的信息进行解码 0|12345|2
        """
        # 颜色
        color = int(msg[0:1].decode(encoding='utf-8'))
        # 代价
        cost = []
        for index in range(5):
            cost.append(int(msg[1+index:2+index].decode(encoding='utf-8')))
        # 分数
        score = int(msg[6:7].decode(encoding='utf-8'))

        return color, cost, score
    
    def update(self,color,cost,score):
        """
        对卡片的信息进行更新
        """
        self.color = color
        for index in range(5):
            self.cost[index] = cost[index]
        self.score = score
        # 使该卡的状态处于激活状态
        self.enable = True

    def select(self,cart,upper_num):
        """
        用来执行对卡牌的选择操作
        """
        if self.enable:
            if self.selected == True:
                self.selected = False
                cart.remove(self)
            elif len(cart) < upper_num:
                self.selected = True
                cart.append(self)
    
    def inRange(self,pos):
        """
        用来判断鼠标点击的位置是否在卡牌的范围内
        """
        if (pos[0]>self.pos[0] and pos[0]<self.pos[0]+Card.size[0] and 
            pos[1]>self.pos[1] and pos[1]<self.pos[1]+Card.size[1]):
            return True
        else:
            return False

class Noble:
    """
    这个类用来表示贵族，包含其在客户端中的可视化方法
    """
    # 静态变量
    # 尺寸
    size = [80,80]
    # 宝石的图片
    gem_pic = []
    gem_pic_size = [20,20]
    gem_pos = [[10,20],[10,40],[10,60]]
    # 字的位置
    font_pos = [0,0]

    def __init__(self,parent,x,y):
        """
        用来对贵族对象进行初始化
        """
        # 可视化时候的父对象
        self.parent = parent
        # 代价
        self.cost = [0,0,0,0,0]
        # 分数
        self.score = 3
        # 显示时左上角的位置
        self.pos = [x,y]
        # 整体的rect对象
        self.object = pg.Surface(Noble.size)
        # 表示贵族是否处于激活状态的标志
        self.enable = False
    
    @staticmethod
    def initialization():
        """
        静态方法，用来加载贵族类的一些静态数据
        """
        # 图片
        Noble.gem_pic.append(pg.transform.scale(pg.image.load('../pic/green.png').convert(), Noble.gem_pic_size))
        Noble.gem_pic.append(pg.transform.scale(pg.image.load('../pic/red.png').convert(), Noble.gem_pic_size))
        Noble.gem_pic.append(pg.transform.scale(pg.image.load('../pic/blue.png').convert(), Noble.gem_pic_size))
        Noble.gem_pic.append(pg.transform.scale(pg.image.load('../pic/black.png').convert(), Noble.gem_pic_size))
        Noble.gem_pic.append(pg.transform.scale(pg.image.load('../pic/white.png').convert(), Noble.gem_pic_size))
        # 字体
        Noble.font1 = pg.font.Font(None,30)
        Noble.font2 = pg.font.Font(None,30)
    
    def show(self):
        """
        可视化方法
        """
        if self.enable:
            # 画边框
            self.object.fill((255,255,255))
            # 画分数
            self.object.blit(Noble.font1.render("Score: 3",False,pg.Color('blue')), Noble.font_pos)
            # 画宝石与其相应的个数
            count = 0
            for index in range(5):
                if self.cost[index]!= 0:
                    # 画宝石
                    self.object.blit(Noble.gem_pic[index],Noble.gem_pos[count])
                    # 画分数
                    self.object.blit(Noble.font2.render(str(self.cost[index]),False,pg.Color('red')), (50,Noble.gem_pos[count][1]))
                    count = count + 1
            # 将该对象画到背景上
            self.parent.blit(self.object,self.pos)
    
    def update(self,cost):
        """
        对贵族进行更新
        """
        for index in range(5):
            self.cost[index] = cost[index]
        self.enable = True

    @staticmethod
    def decode(msg):
        cost = []
        for index in range(5):
            cost.append(int(msg[index:index+1].decode(encoding='utf-8')))
        
        return cost

class Player:
    """
    这个类用来表示玩家，包含着它的可视化方法
    """
    # 静态变量
    # 图片
    gem_pic = []
    gem_pic_size = [20,20]
    reserved_card_pos = [[1030,30],[1030,200]]

    def __init__(self,parent,name,x,y):
        """
        初始化方法
        """
        # 可视化时候的父对象
        self.parent = parent
        # 玩家的名称
        self.name = name
        # 玩家的分数
        self.score = 0
        # 玩家拥有noble的数量
        self.noble = 0
        # 玩家拥有5种卡片的数量
        self.card = [0,0,0,0,0]
        # 玩家拥有的六种token的数量
        self.token = [0,0,0,0,0,0]
        # 玩家拥有的reserve牌的数量
        self.reserve = [Card(parent=self.parent, x=Player.reserved_card_pos[0][0], y=Player.reserved_card_pos[0][1]), 
                        Card(parent=self.parent, x=Player.reserved_card_pos[1][0], y=Player.reserved_card_pos[1][1])]
        # 显示时左上角的位置
        self.pos = [x,y]
        # 整体的rect对象
        self.object = pg.Surface((185,200))
        # 表示该玩家是否处在激活状态的标志
        self.enable = False
    
    @staticmethod
    def initialization():
        """
        静态方法，用来加载Player类种要用到的图片
        """
        # 图片
        Player.gem_pic.append(pg.transform.scale(pg.image.load('../pic/green.png').convert(), Player.gem_pic_size))
        Player.gem_pic.append(pg.transform.scale(pg.image.load('../pic/red.png').convert(), Player.gem_pic_size))
        Player.gem_pic.append(pg.transform.scale(pg.image.load('../pic/blue.png').convert(), Player.gem_pic_size))
        Player.gem_pic.append(pg.transform.scale(pg.image.load('../pic/black.png').convert(), Player.gem_pic_size))
        Player.gem_pic.append(pg.transform.scale(pg.image.load('../pic/white.png').convert(), Player.gem_pic_size))
        Player.gem_pic.append(pg.transform.scale(pg.image.load('../pic/gold.png').convert(), Player.gem_pic_size))
        # 字体
        Player.font1 = pg.font.Font(None,30)
        Player.font2 = pg.font.Font(None,20)

    def show(self):
        """
        用来进行可视化的方法
        """
        if self.enable:
            # 画出底色
            self.object.fill((255,255,255))
            # 画出玩家名称
            self.object.blit(Player.font1.render("Player:",False,pg.Color('blue')),(0,0))
            self.object.blit(Player.font1.render(self.name,False,pg.Color('red')),(100,0))
            # 画出分数
            self.object.blit(Player.font1.render("Score:",False,pg.Color('blue')),(0,20))
            self.object.blit(Player.font1.render(str(self.score),False,pg.Color('red')),(100,20))
            # 画出贵族的数量
            self.object.blit(Player.font1.render("Noble:",False,pg.Color('blue')),(0,40))
            self.object.blit(Player.font1.render(str(self.noble),False,pg.Color('red')),(100,40))
            # 画出卡片
            self.object.blit(Player.font1.render("Card:",False,pg.Color('blue')),(0,60))
            x_pos = 20
            for index in range(5):
                self.object.blit(Player.gem_pic[index], (x_pos,80))
                self.object.blit(Player.font2.render(str(self.card[index]),False,pg.Color('red')), (x_pos+10,100))
                x_pos = x_pos + 25
            # 画出筹码的数量
            self.object.blit(Player.font1.render("Token:",False,pg.Color('blue')),(0,120))
            x_pos = 20
            for index in range(6):
                self.object.blit(Player.gem_pic[index], (x_pos,140))
                self.object.blit(Player.font2.render(str(self.token[index]),False,pg.Color('red')), (x_pos+10,160))
                x_pos = x_pos + 25
            # 画出reserved的牌数
            self.object.blit(Player.font1.render("Reserved:",False,pg.Color('blue')),(0,180))
            self.object.blit(Player.font1.render(str(self.get_reserved_num()),False,pg.Color('red')),(100,180))
            
            self.parent.blit(self.object,self.pos)
    
    def get_reserved_num(self):
        """
        获得该玩家当前reserved牌的数量
        """
        count = 0
        for card in self.reserve:
            if card.enable == True:
                count = count + 1
        return count

    def update(self,name,score,noble,card,token,reserve):
        """
        对玩家的信息进行更新
        """
        # 更新基本信息
        self.name = name
        self.score = score
        self.noble = noble
        for index in range(5):
            self.card[index] = card[index]
        for index in range(6):
            self.token[index] = token[index]
        # 对该玩家保留的牌进行更新
        for index in range(len(reserve)):
            info = reserve[index]
            self.reserve[index].update(info[0],info[1],info[2])
        for index in range(2-len(reserve)):
            self.reserve[-1-index].enable = False
        # 使该玩家的状态处于激活状态
        self.enable = True
    
    def get_token_num(self):
        """
        获取当前玩家手中token的数量
        """
        sum = 0
        for num in self.token:
            sum = sum + num
        
        return sum

class CardChanger:
    """
    这个类是用来进行换牌操作时对所需要的筹码数量进行确认的
    """
    # 静态变量
    # 控件的大小
    size = [110,160]
    # 照片的位置
    pic_pos = [[10,10],[10,40],[10,70],[10,100],[10,130]]
    # 数字选择器的位置
    ns_pos = [[40,10],[40,40],[40,70],[40,100],[40,130]]
    # 宝石照片的大小
    gem_pic_size = [20,20]
    gem_pic = []

    @staticmethod
    def initialization():
        """
        静态函数，用来进行类的初始化，加载相应图片
        """
        # 图片
        CardChanger.gem_pic.append(pg.transform.scale(pg.image.load('../pic/green.png').convert(), CardChanger.gem_pic_size))
        CardChanger.gem_pic.append(pg.transform.scale(pg.image.load('../pic/red.png').convert(), CardChanger.gem_pic_size))
        CardChanger.gem_pic.append(pg.transform.scale(pg.image.load('../pic/blue.png').convert(), CardChanger.gem_pic_size))
        CardChanger.gem_pic.append(pg.transform.scale(pg.image.load('../pic/black.png').convert(), CardChanger.gem_pic_size))
        CardChanger.gem_pic.append(pg.transform.scale(pg.image.load('../pic/white.png').convert(), CardChanger.gem_pic_size))
        CardChanger.gem_pic.append(pg.transform.scale(pg.image.load('../pic/gold.png').convert(), CardChanger.gem_pic_size))
        # 字体
        CardChanger.font1 = pg.font.Font(None,30)
    
    def __init__(self,parent,pos):
        """
        对象初始化函数
        """
        # 可视化时候的父对象
        self.parent = parent
        # 该控件在主画布伤的位置
        self.pos = pos
        # 该控件的底板
        self.object = pg.Surface(CardChanger.size)
        # 控制是否进行画图的指标
        self.enable = False
        # token需求的类型
        self.token_type = []
        # token需求个数计数器
        self.token_demand = []
        # token拥有数量计数器
        self.token_max = []
        # 数字选择器控件
        self.ns_list = []
        for index in range(5):
            self.ns_list.append(widget.NumberSelector(parent=self.object))
            self.ns_list[index].initialization(x=CardChanger.ns_pos[index][0],y=CardChanger.ns_pos[index][1],width=60,height=20,font=CardChanger.font1,
                                               button_color=pg.Color(255,255,255),font_color=pg.Color('green'))

    def update(self,player,card):
        """
        对token选择器的信息进行更新
        """
        # 对卡牌所需要的token的类型和个数进行登记，这里要自动除去玩家已有的相应card的数量
        self.token_type = []
        self.token_demand = []
        for color in range(5):
            if card.cost[color] <= player.card[color]:
                # 如果卡片中该颜色的需求数量小于等于这个玩家手中已有的该颜色的card的数量时，不再需要额外的token
                pass
            else:
                # 如果卡牌的需求数量大于玩家手中已持有的卡牌数量，则需要额外的token
                self.token_type.append(color)
                self.token_demand.append(card.cost[color]-player.card[color])
        # 将金token加入
        self.token_type.append(5)
        self.token_demand.append(0)

        # 对玩家手中的token数量进行更新
        self.token_max = []
        for color in self.token_type:
            self.token_max.append(player.token[color])

        # 更新数字选择器
        for index in range(len(self.token_type)):
            self.ns_list[index].set_range(num_min=0,num_max=self.token_max[index])
        for index in range(5-len(self.token_type)):
            self.ns_list[-1-index].enable = False

        # 设置该控件为显示状态
        self.enable = True
    
    def mouseEvent(self,pos):
        """
        对于鼠标点击事件的反应
        """
        cc_local_pos = [pos[0]-self.pos[0],pos[1]-self.pos[1]]
        for index in range(len(self.token_type)):
            ns_local_pos = [cc_local_pos[0]-CardChanger.ns_pos[index][0],
                            cc_local_pos[1]-CardChanger.ns_pos[index][1]]
            self.ns_list[index].checkMouseEvent(ns_local_pos)

    def show(self):
        """
        可视化函数
        """
        if self.enable == True:
            # 画出底色
            self.object.fill((0,0,0))
            
            for index in range(len(self.token_type)):
                # 画出宝石
                self.object.blit(CardChanger.gem_pic[self.token_type[index]],CardChanger.pic_pos[index])
                # 画出数字选择弃
                self.ns_list[index].show()
            # 将该控件画到主画布上去
            self.parent.blit(self.object,self.pos)

    def checkValid(self):
        """
        检查给出的token方案是否有效
        """
        # 最终的token方案
        self.token_decision = []
        gold_decision = 0
        # 数字选择器中金色token的数量
        gold_num = self.ns_list[len(self.token_type)-1].num
        # 判断是否成功的标签
        success = True

        for index in range(len(self.token_type)-1):
            # 获取当前单色token在数字选择器中的数量
            token_num = self.ns_list[index].num
            token_demand = self.token_demand[index]
            # 遍历所有的非gold的token
            if token_num >= token_demand:
                # 如果本身单色筹码的数量已经大于需求时，直接采用需求数量作为最终决定
                self.token_decision.append(token_demand)
            elif token_num + gold_num >= token_demand:
                # 如果本身的单色筹码不满足需求，但是加上了金色的token之后满足了需求，则仍视为有效
                self.token_decision.append(token_num)
                gold_decision = gold_decision + token_demand - token_num
                gold_num = gold_num - gold_decision
            else:
                # 如果仍不行，则视为失败
                success = False
                break
        
        if success:
            self.token_decision.append(gold_decision)
            return True
        else:
            return False
    
    def get_decision(self):
        """
        获得当前数量选择器所做出的选择
        """
        return_token = [0,0,0,0,0,0]
        for index in range(len(self.token_type)):
            color = self.token_type[index]
            return_token[color] = self.token_decision[index]
        
        return return_token
