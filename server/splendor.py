# 生成随机数的工具包
import random

class Splendor:
    """
    用来实现游戏规则的类
    """
    def __init__(self,parent):
        """
        初始化函数
        """
        # 上级房间
        self.parent = parent
        
    def initialization(self):
        """
        读取卡牌数据
        """
        # 卡牌列表
        self.card_untoken_list = [[],[],[]]
        # 读取文件
        f = open('../cardinfo.db','r')
        while True:
            # 读取一整行
            line = f.readline()

            if line == '':
                # 表示已读到文件的结尾
                break
            else:
                # 以逗号为分隔符进行分割
                pcs = line[:-1].split(',')
                # 读取颜色
                color = int(pcs[0])
                # 读取代价
                cost = []
                for index in range(5): 
                    cost.append(int(pcs[index+1]))
                # 读取分数
                score = int(pcs[6])
                # 读取牌的类型
                level = int(pcs[7])
            # 生成卡牌对象
            card = Card(color=color, cost=cost, score=score, level=level)
            # 将其添加到卡牌数组中
            self.card_untoken_list[card.level].append(card)
            
        f.close()

        # 对三种牌进行洗牌
        for index in range(3):
            random.shuffle(self.card_untoken_list[index])

        """
        读取贵族数据
        """
        noble_list = []
        # 读取文件
        f = open('../nobleinfo.db','r')
        while True:
            # 读取一整行
            line = f.readline()

            if line == '':
                # 表示已读到文件的结尾
                break
            else:
                # 以逗号为分隔符进行分割
                pcs = line[:-1].split(',')
                # 读取代价
                cost = []
                for index in range(5): 
                    cost.append(int(pcs[index]))
            # 生成贵族对象
            noble = Noble(cost=cost)
            # 将其添加到卡牌数组中
            noble_list.append(noble)
            
        f.close()

        # 对noble进行洗牌
        random.shuffle(noble_list)
        # 从中取出 玩家数+1 个作为游戏用
        player_num = self.parent.get_player_num()
        self.noble_list = []
        for index in range(player_num+1):
            self.noble_list.append(noble_list[index])
        
        """
        对筹码Token进行初始化
        """
        if player_num == 2:
            # 两个玩家进行游戏，此时每种筹码为4个
            self.token_list = [4,4,4,4,4,5]
        elif player_num == 3:
            # 三个玩家进行游戏，此时每种筹码为5个
            self.token_list = [5,5,5,5,5,5]
        else:
            # 四个玩家进行游戏，此时每种筹码为7个
            self.token_list = [7,7,7,7,7,5]

    def prepareInfo(self):
        """
        向用户的客户端准备待发送的信息
        """
        msg = b'009'
        # 场上剩余noble的数量
        msg = msg + str(len(self.noble_list)).encode(encoding='utf-8')
        # 场上每个noble的cost
        for noble in self.noble_list:
            msg = msg + noble.prepareInfo()
        # 场上6种token的数量
        for index in range(6):
            msg = msg + str(self.token_list[index]).encode(encoding='utf-8')
        # 牌堆中三种牌
        for level in range(3):
            # 牌堆中的数量与场上牌的数量
            heap_card_num = len(self.card_untoken_list[level]) - 4
            if heap_card_num < 0:
                heap_card_num = 0
                curr_card_num = len(self.card_untoken_list[level])
            else:
                curr_card_num = 4
            # 准备信息
            msg = msg + str(len(str(heap_card_num))).encode(encoding='utf-8')
            msg = msg + str(heap_card_num).encode(encoding='utf-8')
            msg = msg + str(curr_card_num).encode(encoding='utf-8')
            # 准备牌的信息
            for index in range(curr_card_num):
                msg = msg + self.card_untoken_list[level][index].prepareInfo()
        
        # 准备玩家的信息
        msg = msg + str(self.parent.turn).encode(encoding='utf-8')

        return msg
    
    def take_token(self,color_list,num):
        """
        玩家拿token
        """
        for color in color_list:
            self.token_list[color] = self.token_list[color] - num
    
    def reserve(self,level,index):
        """
        玩家reserve牌
        """
        self.card_untoken_list[level].pop(index)
        self.token_list[5] = self.token_list[5] - 1
    
    def change_card(self,level,index):
        """
        玩家换牌
        """
        # 获取这张牌，并返回
        card = self.card_untoken_list[level][index]
        # 将这张牌从牌堆中移除
        self.card_untoken_list[level].pop(index)
        return card
    
    def return_token(self,cost):
        """
        玩家把token还回到token组中
        """
        for index in range(6):
            self.token_list[index] = self.token_list[index] + cost[index]
    
    def check_noble(self,player):
        """
        检查某个玩家是否满足noble的标准
        """
        index = 0
        while (index < len(self.noble_list)):
            noble = self.noble_list[index]
            # 遍历当前场上的卡片
            if noble.check(player):
                # 如果玩家满足该贵族的换取条件
                player.noble_list.append(noble)
                self.noble_list.remove(noble)
                # 玩家记分
                player.score = player.score + noble.score
            else:
                index = index + 1

class Card:
    """
    用来实现卡片的类
    """
    def __init__(self,color,cost,score,level):
        """
        生成卡牌的初始化函数
        颜色的统一规范：绿0，红1，蓝2，黑3，白4
        """
        # 卡牌所代表的颜色
        self.color = color
        # 换取此卡牌所需要的代价，一个5位的list
        self.cost = cost
        # 此卡牌的额外分数
        self.score = score
        # 此卡牌的类别（1级，2级，3级）
        self.level = level
    
    def prepareInfo(self):
        """
        获得该牌的byte信息的函数
        """
        # 牌的颜色
        msg = str(self.color).encode(encoding='utf-8')
        # 牌的cost
        for index in range(5):
            msg = msg + str(self.cost[index]).encode(encoding = 'utf-8')
        # 牌的分数
        msg = msg + str(self.score).encode(encoding='utf-8')

        return msg


class Noble:
    """
    用来实现人物的类
    """
    def __init__(self,cost):
        """
        生成贵族的初始化函数
        """
        # 代价
        self.cost = cost
        # 分数
        self.score = 3
    
    def prepareInfo(self):
        """
        返回noble的cost信息的byte数组
        """
        msg = b''
        for index in range(5):
            msg = msg + str(self.cost[index]).encode(encoding='utf-8')
        
        return msg
    
    def check(self,player):
        """
        检查该玩家是否满足换取该贵族的条件
        """
        success = True
        for color in range(5):
            if len(player.card_list[color]) < self.cost[color]:
                success = False
                break
        
        return success

class SplendorPlayer:
    """
    用来代表splendor游戏中玩家的类
    """
    def __init__(self,parent):
        """
        splendor玩家的初始化函数
        """
        self.parent = parent
    
    def initialization(self):
        """
        每次游戏开始前进行的初始化
        """
        # 玩家的分数
        self.score = 0
        # 玩家获得的noble
        self.noble_list = []
        # 玩家获得的card的list
        self.card_list = [[],[],[],[],[]]
        # 玩家获得的token的list
        self.token_list = [0,0,0,0,0,0]
        # 玩家保留牌的list
        self.reserved_list = []

    def prepareInfo(self):
        """
        准备玩家的信息
        """
        # 玩家的分数
        msg = str(self.score).zfill(2).encode(encoding='utf-8')
        # 贵族的数量
        msg = msg + str(len(self.noble_list)).encode(encoding='utf-8')
        # 5种card的数量
        for card_type in self.card_list:
            msg = msg + str(len(card_type)).zfill(2).encode(encoding='utf-8')
        # 6种token的数量
        for token_num in self.token_list:
            msg = msg + str(token_num).encode(encoding='utf-8')
        # reserve牌的信息
        msg = msg + str(len(self.reserved_list)).encode(encoding='utf-8')
        for card in self.reserved_list:
            msg = msg + card.prepareInfo()
        
        return msg
    
    def take_token(self,color_list,num):
        """
        玩家拿token
        """
        for color in color_list:
            self.token_list[color] = self.token_list[color] + num
    
    def reserve(self,level,index):
        """
        玩家reserve牌
        """
        self.reserved_list.append(self.parent.room.game.card_untoken_list[level][index])
        self.token_list[5] = self.token_list[5] + 1
    
    def change_card(self,card,cost):
        # 将这张卡片放置到自己的牌组中
        self.card_list[card.color].append(card)
        # 记分
        self.score = self.score + card.score
        # 将消耗的cost从自己的token list中去掉
        for index in range(6):
            self.token_list[index] = self.token_list[index] - cost[index]
    
    def check_win(self):
        """
        检查是否已经取得了胜利
        """
        if self.score >= 15:
            return True
        else:
            return False

if __name__ == "__main__":
    test = Splendor(None)
    test.initialization()