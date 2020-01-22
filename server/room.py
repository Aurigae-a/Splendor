# 导入多线程包
import threading as th
# 导入时间类
import time
# 导入splendor游戏主题
import splendor as sp

class RoomManager:
    """
    对房间进行管理
    """
    def __init__(self):
        """
        房间管理的初始化构造函数
        """
        # 初始化房间字典
        self.room_list = {}
        for index in range(1000,10000):
            self.room_list[index] = None
        # 创建并启动房间监视器线程
        self.th_room_supervisor = th.Thread(target=self.room_supervise)
        self.th_room_supervisor.start()
    
    def room_create(self,player,player_num,password):
        """
        新建一个房间
        """
        # 生成房间号
        room_found = False
        for index in range(1000,10000):
            if self.room_list[index] == None:
                room_num = index
                room_found = True
                break
        
        # 判断房间管理器是否已经满了
        if room_found == True:
            # 如果房间没满，返回0
            # 判断是否有密码
            if not password:
                pw_enable = False
                password = ""
            else:
                pw_enable = True
            # 生成房间
            self.room_list[index] = Room(room_number=room_num, pw_enable=pw_enable, password=password ,p_number=player_num, p_master=player)
            
            return 0, self.room_list[index]
        else:
            # 如果房间已经满了，则返回1
            return 1, None
    
    def room_search(self,room_num):
        """
        寻找指定的房间号，看该房间是否存在
        """
        if self.room_list[room_num] != None:
            # 该房间存在
            return self.room_list[room_num]
        else:
            # 该房间不存在
            return None
    
    def room_supervise(self):
        """
        用来对各个房间进行监控，当房间中玩家数量为0的时候，将该房间从房间列表中删除
        """
        while True:
            for index in range(1000,10000):
                if self.room_list[index] != None and self.room_list[index].isFinished:
                    self.room_list[index] = None


class Room:
    """
    这个类是表述房间管理的，它负责管理游戏房间中的人员。游戏运行机制是它的一个从属对象。
    """
    def __init__(self,room_number,pw_enable,password,p_number,p_master):
        """
        房间管理的初始化函数
        """
        # 房间号
        self.number = room_number
        # 是否有密码
        self.pw_enable = pw_enable
        # 密码
        self.password = password
        # 房间人数
        self.p_number = p_number
        # 玩家列表
        self.player_list = [p_master]

        # 用于判断该房间是否已经结束的标签
        self.isFinished = False
        # 用于判断该房间是否开始游戏的标签
        self.gameStarted = False
        # 用于判断该房间的游戏是否完成标签
        self.gameFinished = False
        # 赢家记录
        self.winner = None

        # 初始化游戏主题
        self.game = sp.Splendor(self)
        # 回合制游戏表示谁的回合的标签
        self.turn = 0

        # 初始化房间主线程
        self.main_thread = th.Thread(target=self.main_process)
        self.main_thread.start()
    
    def client_join(self,player,password):
        """
        用户请求加入房间，返回值0表示成功加入，1表示密码不正确，2表示房间已满
        """
        if password == self.password:
            # 检查房间是否已满
            if len(self.player_list) == self.p_number:
                isFull = True
            else:
                isFull = False
            
            if not isFull:
                if not self.gameStarted: 
                    # 将玩家添加到房间的玩家列表当中
                    self.player_list.append(player)
                    return 0
                else:
                    # 表示房间已开始了游戏
                    return 4
            else:
                # 表示房间已满
                return 2
        else:
            # 表示密码错误
            return 1
    
    def client_leave(self,player):
        """
        用户离开房间
        """
        # 遍历玩家登记列表，从中寻找指定的要删除的用户
        isFound = False
        for myPlayer in self.player_list:
            if myPlayer == player:
                isFound = True
                break
        
        if isFound == False:
            # 未在玩家列表中找到该玩家，返回2
            return 2
        else:
            # 将该用户从房间的玩家列表中删除
            self.player_list.remove(player)
            return 0
    
    def isEmpty(self):
        """
        判断这个房间是否是空房间
        """
        if len(self.player_list) == 0:
            return True
        else:
            return False

    def broadcast_room_state(self):
        """
        向该房间的所有用户广播当前的玩家状态
        """
        # 准备待发送的信息
        # 操作代码 + 房间名称 + 玩家数量
        msg = b'006' + str(self.number).encode(encoding='utf-8') + str(len(self.player_list)).encode(encoding='utf-8')
        for player in self.player_list:
            # 用户名长度
            msg = msg + str(len(player.name)).encode(encoding='utf-8')
            # 用户名
            msg = msg + player.name.encode(encoding='utf-8')
            # 准备状态
            if player.ready:
                msg = msg + b'1'
            else:
                msg = msg + b'0'
        
        # 向每一位玩家进行发送
        for player in self.player_list:
            player.send(msg)
    
    def broadcast_turn_state(self):
        """
        向房间的每一位用户广播当前玩家是第几个
        """
        for player_index in range(len(self.player_list)):
            self.player_list[player_index].send(b'015'+str(player_index).encode(encoding='utf-8'))

    def broadcast_game_state(self):
        """
        向房间的每一位用户广播玩家信息和卡牌信息
        """
        # 准备信息
        table_info, player_info = self.prepareInfo()
        # 对每一位用户进行广播
        for player in self.player_list:
            player.send(table_info)
            player.send(player_info)
    
    def broadcast_winner_state(self):
        """
        想房间中的每一个用户广播游戏结束的信息及胜者的编号
        """
        # 查找胜者的编号
        for index in range(len(self.player_list)):
            if self.player_list[index] == self.winner:
                break
        # 准备信号
        msg = b'018' + str(index).encode(encoding='utf-8')
        # 对每一位用户进行广播
        for player in self.player_list:
            player.send(msg)

    def get_curr_player(self):
        """
        获得当前回合的玩家的指针
        """
        return self.player_list[self.turn]

    def get_player_num(self):
        """
        获得玩家的数量
        """
        return len(self.player_list)

    def next_turn(self):
        """
        下一玩家
        """
        self.turn = self.turn + 1
        if self.turn >= len(self.player_list):
            self.turn = 0
    
    def prepareInfo(self):
        """
        准备游戏时向各个玩家发送的信息
        """
        # 桌上剩余牌的信息
        table_info = self.game.prepareInfo()
        # 玩家信息
        player_info = b'010' + str(len(self.player_list)).encode(encoding='utf-8')
        for player in self.player_list:
            player_info = player_info + player.prepareInfo()
        
        return table_info, player_info

    def main_process(self):
        """
        该房间的主线程，当房间中无人时，结束该线程
        """
        while not self.isEmpty():
            if self.gameStarted == False:
                # 查看是否所有玩家已准备完毕
                allReady = True
                for player in self.player_list:
                    if player.ready == False:
                        allReady = False
                        break
                
                if self.get_player_num()>1 and allReady:
                    # 如果已经全部准备完毕，则开始游戏
                    self.gameStarted = True
                    self.gameFinished = False
                    # 对游戏进行初始化
                    self.game.initialization()
                    # 向每个玩家进行广播，告知已开始游戏
                    for player in self.player_list:
                        player.send(b'008')
                    # 对各个玩家的组件进行初始化
                    for player in self.player_list:
                        player.game.initialization()
                    # 广播游戏信息
                    self.broadcast_game_state()
                    self.turn  = 0
                    # 通知第一个玩家开始游戏
                    self.player_list[0].send(b'011')

                else:
                    # 表示游戏还没有开始，处于准备阶段，则对所有的用户广播该房间的状态
                    self.broadcast_room_state()
                    time.sleep(1)
            
            else:
                if self.gameFinished == False:
                    # 开始游戏
                    self.broadcast_game_state()
                    self.broadcast_turn_state()
                    time.sleep(1)
                else:
                    # 游戏结束
                    # 广播结束信息
                    self.broadcast_winner_state()
                    # 游戏重新进入准备阶段
                    self.gameStarted = False
                    # 所有玩家的准备状态重置
                    for player in self.player_list:
                        player.ready == False


        # 将该房间设置为已完成，便于房间管理器线程进行删除
        self.isFinished = True
