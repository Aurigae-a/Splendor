# 导入通讯组件包
import client_manager as cm
# 导入房间包
import room as ro
# 导入splendor游戏组件包
import splendor as sp

class Player:
    """
    这个类用来表示玩家
    """
    def __init__(self,room_manager,conn,addr):
        """
        初始化构造函数
        """
        # 记录父对象
        self.room_manager = room_manager
        # 创建套接字
        self.myClient = cm.ClientManager(self,conn,addr)

        # 初始化玩家名称
        self.name = ""

        # 初始化是否加入了房间以及房间的对象
        self.room_joined = False
        self.room = None
        
        # 初始化是否请求删除的标签
        self.please_delete = False

        # 初始化玩家准备状态
        self.ready = False

        # 初始化游戏组件
        self.game = sp.SplendorPlayer(self)
    
    def create_room(self,player_num,password):
        """
        创建房间
        """
        # 创建房间
        cmd,room = self.room_manager.room_create(player=self, player_num=player_num, password=password)

        if cmd == 0:
            # 表示创建成功
            # 对客户端的登记进行操作
            self.room_joined = True
            self.room = room
            # 玩家准备状态设置为未准备
            self.ready = False
            # 向客户端发出成功创建的信息
            room_num = str(self.room.number).encode(encoding='utf-8')
            self.send(b'001'+room_num)
        else:
            # 创建失败,向客户端发出创建失败的信息
            self.send(b'002')
    
    def join_room(self,room_num,pw):
        """
        玩家加入某一房间
        """
        # 检查该房间是否存在
        room = self.room_manager.room_search(room_num=room_num)
        
        if not room:
            # 该房间不存在
            self.send(b'0053')
        else:
            # 尝试加入房间
            cmd = room.client_join(player=self, password=pw)
            
            if cmd == 1:
                # 密码错误
                self.send(b'0051')
            elif cmd == 2:
                # 房间已满
                self.send(b'0052')
            elif cmd == 4:
                # 房间已开始游戏
                self.send(b'0054')
            else:
                # 加入成功，将玩家的房间信息进行修改
                self.room_joined = True
                self.room = room
                # 玩家准备状态设置为未准备
                self.ready = False
                self.send(b'0050')
    
    def quit_room(self):
        """
        玩家正常退出房间，但仍然与服务器保持连接
        """
        # 从房间登记中将该用户删除
        self.room.client_leave(self)
        # 重制玩家状态
        self.name = ""
        self.ready = False
        self.room = None
        self.room_joined = False

    def exception_quit(self):
        """
        表示由于意外，与客户端失去联系
        """
        # 从room中将其删除
        if self.room_joined:
            # 如果正在游戏，则通知下一玩家回合开始，然后对turn进行操作
            if self.room.gameStarted and self.room.player_list[self.room.turn]==self:
                self.room.next_turn()
                if self.room.turn != 0:
                    self.room.turn = self.room.turn - 1

            self.room.client_leave(player=self)
            self.room_joined = False
            self.room = None
        # 结束发送和处理线程
        self.myClient.running = False
        # 关闭套接字
        while not self.myClient.isFinished():
            continue
        self.myClient.conn.close()
        # 删除玩家
        self.please_delete = True
    
    def normal_quit(self):
        """
        表示玩家的正常退出
        """
        # 从room中将其删除
        if self.room_joined:
            # 如果正在游戏，则通知下一玩家回合开始，然后对turn进行操作
            if self.room.gameStarted:
                if self.room.player_list[self.room.turn]==self:
                    # 如果当前是自己的回合，则需要通知下一个玩家开始回合
                    if len(self.room.player_list) != 1:
                        # 如果房间内只剩下自己一个用户，那么就不需要通知了
                        self.room.next_turn()
                    if self.room.turn != 0:
                        self.room.turn = self.room.turn - 1
                else:
                    # 如果不是自己的回合
                    # 查找自己的位置
                    for self_index in range(len(self.room.player_list)):
                        if self.room.player_list[self_index] == self:
                            break
                    if self_index < self.room.turn:
                        # 如果自己的位置在当前游戏玩家之前，则需要重新调整turn
                        self.room.turn = self.room.turn - 1
            cmd = self.room.client_leave(player=self)
            
            if cmd == 0:
                # 表示删除成功，向客户端发出退出告知
                self.room_joined = False
                self.room = None
                self.send(b'0041')

        # 向客户端发出断开连接告知
        self.send(b'farewell')
        # 关闭发送许可
        self.myClient.send_permision = False
        # 结束3个线程
        self.myClient.running = False
        # 关闭套接字
        while not self.myClient.isFinished():
            continue
        self.myClient.conn.close()
        # 删除玩家
        self.please_delete = True

    def set_name(self,username):
        """
        设置客户端用户的名称
        """
        self.name = username
    
    def send(self,msg):
        """
        用于对客户端进行信息的发送
        """
        if self.myClient.send_permision == True:
            self.myClient.send_msg_queue.append(msg)

    def get_delete(self):
        return self.please_delete
    
    def set_ready(self,ready):
        """
        设置是否准备完毕
        """
        self.ready = ready
    
    def prepareInfo(self):
        """
        准备玩家的相关信息
        """
        # 玩家名称的长度
        msg = str(len(self.name)).encode(encoding='utf-8')
        # 玩家名称
        msg = msg + self.name.encode(encoding='utf-8')
        # 玩家的卡牌信息
        msg = msg + self.game.prepareInfo()

        return msg
