# 进行网络通信的socket类
import socket as sk
# 多线程实现类
import threading as th
# 控制时间的类
import time
# 游戏类
import splendor as sp

class ClientConnection:
    """
    这个类主要实现的是客户端与服务器之间的沟通与联系
    """
    def __init__(self,parent):
        # 设置中心线程
        self.central_process = parent

        # 设置生命周期
        self.running = True
        # 设置发送许可
        self.send_permission = True
        
        # 客户端中接收连接服务器的地址和端口的字符串
        self.HOST = ""
        self.PORT = 0
        self.mySocket = None
        
        # 初始化发送线程与接收线程
        self.send_thread = th.Thread(target=self.message_send)
        self.recv_thread = th.Thread(target=self.message_recv)
        # 初始化信息处理线程
        self.cmd_prcs_thread = th.Thread(target=self.cmd_process)

        # 初始化发送消息队列
        self.send_message_queue = []
        # 初始化接收消息队列
        self.recv_message_queue = []


    def set_host_port(self,host,port):
        """
        这个函数用来对socket的端口和地址进行赋值
        """
        self.HOST = host
        self.PORT = port

    def connect(self,host,port):
        """
        这个函数是用来对指定的地址和端口进行创立socket连接的
        """
        # 尝试对指定地址端口进行登陆
        try:
            # 建立socket
            self.mySocket = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
            # 尝试连接
            self.mySocket.connect((host,port))
            # 设置socket的超时
            self.mySocket.settimeout(1)
            # 如果连接成功，则记录主机号与端口号
            self.HOST = host
            self.PORT = port
            # 启动接收线程和发送线程
            self.send_thread.start()
            self.recv_thread.start()
            # 启动信息处理线程
            self.cmd_prcs_thread.start()
            # 进入到登陆后状态
            self.central_process.state = 2

        except OSError:
            # 连接失败
            # 重新退回到未登录状态
            self.central_process.state = 0
        
        except TypeError:
            # 连接失败
            # 重新退回到未登录状态
            self.central_process.state = 0

    def message_send(self):
        """
        用于和服务端进行通信的信息发送函数，主要被发送线程进行调用
        """
        while self.running:
            # 当消息发送队列不为空的时候，就要不停的发送
            if len(self.send_message_queue) != 0:
                # 从消息队列中获得信息
                msg = self.send_message_queue[0]
                # 将已获得的信息从消息队列中删除
                self.send_message_queue.pop(0)
                
                # 尝试发送
                try:
                    self.mySocket.sendall(msg)
                    time.sleep(0.1)
                except BrokenPipeError:
                    # 如果丢失连接，则客户端重新回到未连接状态
                    print("lost connection")
                    self.central_process.state = 0
    
    def message_recv(self):
        """
        用于和服务端进行通信的信息接收函数，主要被接收线程进行调用
        """
        while self.running:
            try:
                # 以阻塞的方式进行接收信息
                msg = self.mySocket.recv(1024)
                # 向接收队列中加入该信息以便于处理
                self.recv_message_queue.append(msg)
                time.sleep(0.1)
            except sk.timeout:
                continue
    
    def cmd_process(self):
        """
        用于进行对从服务端接收到的信息进行处理
        """
        while self.running:

            if self.central_process.state == -1:
                # 向服务器发出结束连接信息
                self.send(b"quit")
                # 关闭发送许可
                self.send_permission = False

            if len(self.recv_message_queue) != 0:
                # 获得当前信息
                msg = self.recv_message_queue[0]
                self.recv_message_queue.pop(0)

                if msg == b'farewell':
                    # 如果来自服务器的信息是farewell，则说明服务器已经成功的结束了该用户的所有信息，结束3个线程
                    self.running = False
                    # 关闭socket
                    self.mySocket.close()
                    continue

                cmd = msg[0:3]

                if cmd == b'001':
                    # 表示服务器传回了成功创建房间的信息,将主程序的状态机切换至房间状态
                    self.central_process.state = 4
                
                elif cmd == b'002':
                    # 表示服务器传回了创建房间失败的信息
                    self.central_process.state = 2
                
                elif cmd == b'005':
                    # 表示服务器传回了加入房间的信息
                    succ = msg[3:4]

                    if succ == b'0':
                        # 加入成功
                        self.central_process.state = 4
                    else:
                        # 加入失败
                        self.central_process.state = 2
                    
                elif cmd == b'006':
                    # 服务端发来的更新房间状态的信息
                    # 房间号
                    self.central_process.main_window.room_num = msg[3:7].decode(encoding='utf-8')
                    # 获得玩家数量
                    player_num = int(msg[7:8].decode(encoding='utf-8'))
                    # 获得每个玩家的信息
                    self.central_process.main_window.room_player_list = []
                    curr_index = 8
                    for index in range(player_num):
                        try:
                            # 获得玩家的名称长度
                            name_len = int(msg[curr_index:curr_index+1].decode(encoding='utf-8'))
                            curr_index = curr_index + 1
                            # 获得玩家的名称
                            name = msg[curr_index:curr_index+name_len].decode(encoding='utf-8')
                            curr_index = curr_index + name_len
                            # 获得玩家的状态
                            status = int(msg[curr_index:curr_index+1].decode(encoding='utf-8'))
                            curr_index = curr_index + 1
                            # 将玩家信息放入到显示列表中
                            self.central_process.main_window.room_player_list.append([name,status])
                        except:
                            continue
                
                elif cmd == b'008':
                    # 服务器发来的开始游戏通知
                    self.central_process.state = 5
                
                elif cmd == b'009':
                    # 来自服务器的卡牌数据更新
                    try:
                        # 场上剩余noble的数量
                        noble_num = int(msg[3:4].decode(encoding='utf-8'))
                        # 获取noble信息
                        index = 4
                        for noble_index in range(noble_num):
                            cost = sp.Noble.decode(msg[index:index+5])
                            self.central_process.main_window.game_noble_list[noble_index].update(cost)
                            index = index + 5
                        for noble_index in range(5-noble_num):
                            self.central_process.main_window.game_noble_list[-1-noble_index].enable = False
                        # 获取token的信息
                        for token_index in range(6):
                            token_num = int(msg[index:index+1].decode(encoding='utf-8'))
                            self.central_process.main_window.game_token_list[token_index].update(token_num)
                            index = index + 1
                        # 获取card的信息
                        for card_level in range(3):
                            # 获取该卡片牌堆种的剩余数量的数字长度
                            card_num_len = int(msg[index:index+1].decode(encoding='utf-8'))
                            # 获取该卡片牌堆种的剩余数量
                            card_num = int(msg[index+1:index+1+card_num_len].decode(encoding='utf-8'))
                            self.central_process.main_window.game_label[6+card_level].set_text("level "+str(card_level+1)+": "+str(card_num))
                            # 获取该种卡片在场上的数量
                            card_num = int(msg[index+1+card_num_len:index+2+card_num_len].decode(encoding='utf-8'))
                            index = index+2+card_num_len
                            # 获取这几种卡片
                            for card_index in range(card_num):
                                color, cost, score = sp.Card.decode(msg[index:index+7])
                                self.central_process.main_window.game_card_list[card_level][card_index].update(color,cost,score)
                                index = index + 7
                            for card_index in range(4-card_num):
                                self.central_process.main_window.game_card_list[card_level][-1-card_index].enable = False
                        # 获取轮次的信息
                        self.central_process.main_window.game_turn = int(msg[index:index+1].decode(encoding='utf-8'))
                        self.central_process.main_window.game_label[10].set_text("Turn: Player "+str(self.central_process.main_window.game_turn+1))
                        # 根据玩家编号判断是否是当前回合
                        if self.central_process.main_window.game_my_turn_num == self.central_process.main_window.game_turn:
                            # 是自己当前的回合
                            if self.central_process.main_window.game_my_turn == False:
                                self.central_process.main_window.game_my_turn = True
                                self.central_process.main_window.game_operation = 0
                                self.central_process.main_window.game_reset()
                                self.central_process.main_window.game_hint_state = 0
                        else:
                            # 不是自己的回合
                            if self.central_process.main_window.game_my_turn == True:
                                # 自己的回合结束
                                self.central_process.main_window.game_my_turn = False
                                self.central_process.main_window.game_operation = 0
                                self.central_process.main_window.game_reset()
                                self.central_process.main_window.game_hint_state = -1
                    except:
                        continue

                elif cmd == b'010':
                    # 来自服务器的玩家数据更新
                    try:
                        # 玩家数量
                        player_num = int(msg[3:4].decode(encoding='utf-8'))
                        index = 4
                        for player_index in range(player_num):
                            # 玩家名称的长度
                            name_len = int(msg[index:index+1].decode(encoding='utf-8'))
                            # 玩家的名称
                            name = msg[index+1:index+1+name_len].decode(encoding='utf-8')
                            # 玩家的分数
                            player_score = int(msg[index+1+name_len:index+3+name_len].decode(encoding='utf-8'))
                            # 玩家的noble的数量
                            noble = int(msg[index+3+name_len:index+4+name_len].decode(encoding='utf-8'))
                            # 玩家五种牌的数量
                            card = []
                            index = index+4+name_len
                            for card_index in range(5):
                                card.append(int(msg[index:index+2].decode(encoding='utf-8')))
                                index = index + 2
                            # 玩家的六种token的数量
                            token = []
                            for token_index in range(6):
                                token.append(int(msg[index:index+1].decode(encoding='utf-8')))
                                index = index + 1
                            # reserve牌的数量
                            reserve_num = int(msg[index:index+1].decode(encoding='utf-8'))
                            index = index + 1
                            reserve = []
                            for card_index in range(reserve_num):
                                # 对卡片进行解码
                                color, cost, score = sp.Card.decode(msg[index:index+7])
                                reserve.append([color,cost,score])
                                # 更新卡片的信息
                                index = index + 7
                            # 更新玩家信息
                            self.central_process.main_window.game_player_list[player_index].update(name,player_score,noble,card,token,reserve)
                        for index in range(4-player_num):
                            self.central_process.main_window.game_player_list[-1-index].enable = False
                    except:
                        continue
                
                elif cmd == b'015':
                    # 来自服务器的通知该玩家是第几号的信息
                    self.central_process.main_window.game_my_turn_num = int(msg[3:4].decode(encoding='utf-8'))
                
                elif cmd == b'018':
                    # 来自服务器结束游戏的通知
                    winner_index = int(msg[3:4].decode(encoding='utf-8'))
                    # 初始化可视化界面的finished组件
                    self.central_process.main_window.finished_init(winner_index=winner_index)
                    # 游戏状态进入7
                    self.central_process.state = 7

    def send(self,msg):
        """
        用于对外界提供一种发送信息的接口
        """
        if self.send_permission:
            self.send_message_queue.append(msg)
