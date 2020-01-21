# 用于多线程的包
import threading
# 用于实现网络编程的包
import socket
# 时间控制
import time

class ClientManager:
    """
    这个类是用来实现服务端与客户端之间的信息交互，主要有以下几个方面的工作：
        1. 来自客户端的消息的接收
        2. 发送给客户端的信息
    """
    def __init__(self, parent, conn, addr):
        # 该客户端的生命周期
        self.running = True

        # 服务端的总体运营类
        self.parent = parent

        # 对服务器的主机地址和端口号进行初始化
        self.conn = conn
        self.addr = addr
        # 设置socket的超时时长
        self.conn.settimeout(1)

        # 接收消息队列
        self.recv_msg_queue = []
        # 发送消息队列
        self.send_msg_queue = []

        # 用于管理发送和接收线程结束时的标签
        self.recv_finish = False
        self.send_finish = False
        # 用于管理是否允许发送的标签
        self.send_permision = True

        # 创建接收信息的线程
        self.th_recv = threading.Thread(target=self.client_reveive)
        self.th_recv.start()

        # 创建发送信息的线程
        self.th_send = threading.Thread(target=self.client_send)
        self.th_send.start()

        # 创建命令处理的线程
        self.th_prcs = threading.Thread(target=self.cmd_process)
        self.th_prcs.start()

    def isFinished(self):
        """
        当要对其进行删除时，通过这一函数来判断是否所有的线程都已经结束
        """
        if self.recv_finish and self.send_finish:
            return True
        else:
            return False

    def client_reveive(self):
        """
        这个函数用来实现从客户端监听数据的工作
        """
        while self.running:
            try:
                data = self.conn.recv(1024)
                print(data)
                
                if data != None:
                    # 其他输入,放入接收消息队列
                    self.recv_msg_queue.append(data)
            
            except socket.timeout:
                # 若超时而没有任何输入则重新回到循环
                continue
        
        # 当线程结束时，将recv结束的标签设置为True
        self.recv_finish = True

    def client_send(self):
        """
        这个函数用来实现向客户端发送数据的工作
        """
        while self.running or len(self.send_msg_queue)!=0:
            if len(self.send_msg_queue) != 0:
                # 获取待发送的信息
                msg = self.send_msg_queue[0]
                self.send_msg_queue.pop(0)
                
                try:
                    # 向客户端发送信息
                    self.conn.sendall(msg)
                    # 等待0.5秒
                    time.sleep(0.1)
                except BrokenPipeError:
                    # socket意外关闭，则执行意外关闭的后续处理
                    self.send_msg_queue = []
                    self.recv_msg_queue = [b'']
        
        # 当线程结束时，将send结束的标签设置为True
        self.send_finish = True

    def cmd_process(self):
        """
        这个函数是用来处理接收消息队列中来自各个客户端发出的命令的
        """
        while self.running:
            # 如果消息队列不为空的话，则取出第一个进行处理
            if len(self.recv_msg_queue) != 0:
                msg = self.recv_msg_queue[0]
                self.recv_msg_queue.pop(0)

                if msg == b'':
                    # 表示该客户端意外的退出，执行用户意外退出程序
                    self.parent.exception_quit()
                
                elif msg == b'quit':
                    # 表示客户端正常的退出
                    self.parent.normal_quit()

                else:
                    # 获取操作指令
                    cmd = msg[0:3]
                    
                    if cmd == b'000':
                        # 来自客户端的请求创建房间的指令
                        isSucc = True
                        try:
                            # 人数
                            player_num = int(msg[3:4].decode(encoding='utf-8'))
                            # 获取密码长度
                            pw_length = int(msg[4:5].decode(encoding='utf-8'))
                            # 获取密码
                            pw = msg[5:5+pw_length].decode(encoding='utf-8')
                            # 获取玩家名称长度
                            username_length = int(msg[5+pw_length:6+pw_length].decode(encoding='utf-8'))
                            # 获取玩家名称
                            username = msg[6+pw_length:6+pw_length+username_length].decode(encoding='utf-8')

                        except ValueError:
                            isSucc = False
                            
                        if isSucc:
                            print('create succ')
                            # 创建房间
                            self.parent.create_room(player_num=player_num,password=pw)
                            # 更改玩家姓名
                            self.parent.set_name(username=username)
                    
                    elif cmd == b'003':
                        # 来自客户端的请求加入房间的指令
                        isSucc = True
                        try:
                            # 获取房间号
                            room_num = int(msg[3:7].decode(encoding='utf-8'))
                            # 获取密码长度
                            pw_length = int(msg[7:8].decode(encoding='utf-8'))
                            # 获取密码
                            pw = msg[8:8+pw_length].decode(encoding='utf-8')
                            # 获取玩家名称长度
                            username_length = int(msg[8+pw_length:9+pw_length].decode(encoding='utf-8'))
                            # 获取玩家名称
                            username = msg[9+pw_length:9+pw_length+username_length].decode(encoding='utf-8')
                        except:
                            isSucc = False
                            
                        if isSucc:
                            print('join succ')
                            # 创建房间
                            self.parent.join_room(room_num=room_num, pw=pw)
                            # 更改玩家姓名
                            self.parent.set_name(username=username)
                    
                    elif cmd == b'004':
                        # 来自客户端的请求退出房间的信息
                        self.parent.quit_room()
                    
                    elif cmd == b'007':
                        # 来自客户端的请求玩家准备状态变更的信息
                        ready_info = int(msg[3:4].decode(encoding='utf-8'))
                        print(ready_info)
                        if ready_info == 0:
                            self.parent.set_ready(ready=False)
                        else:
                            self.parent.set_ready(ready=True)
                    
                    elif cmd == b'012':
                        # 来自客户端发出的拿三个token的请求
                        color_list = []
                        for index in range(3):
                            color_list.append(int(msg[3+index:4+index].decode(encoding='utf-8')))
                        # 玩家进行取token的操作
                        self.parent.game.take_token(color_list=color_list,num=1)
                        # 牌桌进行去token的操作
                        self.parent.room.game.take_token(color_list=color_list,num=1)
                        # 通知下一个玩家开始回合
                        self.parent.room.next_turn()
                    
                    elif cmd == b'013':
                        # 来自客户端发出的拿2个token的请求
                        color_list = [int(msg[3:4].decode(encoding='utf-8'))]
                        # 玩家进行取token的操作
                        self.parent.game.take_token(color_list=color_list,num=2)
                        # 牌桌进行去token的操作
                        self.parent.room.game.take_token(color_list=color_list,num=2)
                        # 通知下一个玩家开始回合
                        self.parent.room.next_turn()
                    
                    elif cmd == b'014':
                        # 来自客户端的要reserve牌的操作
                        level = int(msg[3:4].decode(encoding='utf-8'))
                        index = int(msg[4:5].decode(encoding='utf-8'))
                        # 玩家执行reserve该card的操作
                        self.parent.game.reserve(level=level,index=index)
                        # 房间执行reserve该card的操作
                        self.parent.room.game.reserve(level=level,index=index)
                        # 通知下一个玩家开始回合
                        self.parent.room.next_turn()
                    
                    elif cmd == b'016':
                        # 来自客户端的要从牌堆中换牌的操作
                        level = int(msg[3:4].decode(encoding='utf-8'))
                        index = int(msg[4:5].decode(encoding='utf-8'))
                        token_demand = []
                        for color in range(6):
                            token_demand.append(int(msg[5+color:6+color].decode(encoding='utf-8')))
                        # 房间执行将该牌从牌堆中删除的操作
                        card = self.parent.room.game.change_card(level=level,index=index)
                        # 房间执行将兑换时需要的token还回到牌堆的操作
                        self.parent.room.game.return_token(cost=token_demand)
                        # 玩家执行将该牌放入自己牌组的操作
                        self.parent.game.change_card(card=card,cost=token_demand)
                        # 房间检查是否满足换取noble的操作
                        self.parent.room.game.check_noble(player=self.parent.game)
                        # 检查该玩家是否取得胜利
                        if self.parent.game.check_win():
                            self.parent.room.winner = self
                            self.parent.room.gameFinished = True
                        else:
                            # 通知下一个玩家开始回合
                            self.parent.room.next_turn()
                    
                    elif cmd == b'017':
                        # 来自客户端的要从reserve的牌中换牌的操作
                        # reserve牌的index
                        index = int(msg[3:4].decode(encoding='utf-8'))
                        # 该玩家愿意花出的代价
                        token_demand = []
                        for color in range(6):
                            token_demand.append(int(msg[4+color:5+color].decode(encoding='utf-8')))
                        # 获得该牌
                        card = self.parent.game.reserved_list[index]
                        # 将该牌从reserve的牌中删除
                        self.parent.game.reserved_list.remove(card)
                        # 房间执行将兑换时需要的token还回到牌堆的操作
                        self.parent.room.game.return_token(cost=token_demand)
                        # 玩家执行将该牌放入自己牌组的操作
                        self.parent.game.change_card(card=card,cost=token_demand)
                        # 房间检查是否满足换取noble的操作
                        self.parent.room.game.check_noble(player=self.parent.game)
                        # 检查该玩家是否取得胜利
                        if self.parent.game.check_win():
                            self.parent.room.winner = self
                            self.parent.room.gameFinished = True
                        else:
                            # 通知下一个玩家开始回合
                            self.parent.room.next_turn()
                    
                    elif cmd == b'019':
                        # 表示该玩家跳过了该回合,通知下一个玩家开始回合
                        self.parent.room.next_turn()
