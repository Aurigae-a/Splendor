# 导入多线程的包
import threading
# 导入socket的包
import socket
# 玩家类
import player
# 房间管理相关类
import room

class CentralThread():
    """
    这个类是服务器的主线程，主要用来进行服务器端的总流程控制
    """

    def __init__(self):
        """
        主控制类的初始化函数，需要做到如下几件事情：
        """
        # 初始化登入用户清单
        self.player_list = []
        # 初始化游戏房间
        self.room_manager = room.RoomManager()

        # 设置服务端的服务器IP地址号和端口号
        self.HOST = "192.168.1.2"
        self.PORT = 5050

        # 开始用户管理线程
        self.player_th = threading.Thread(target=self.client_daemon)
        self.player_th.start()
        # 开始监听客户端登陆申请
        self.create_connection()
    
    def __del__(self):
        """
        析构函数，关闭监听套接字
        """
        if self.mySocket != None:
            self.mySocket.close()
            
    def client_daemon(self):
        """
        这个函数用来将指定的客户端从登记列表中删除
        """
        while True:
            for player in self.player_list:
                if player.get_delete():
                    # 如果客户端已经出现了删除申请，那么直接将它从玩家列表中删除
                    self.player_list.remove(player)
    
    def create_connection(self):
        """
        这个函数是这个客户准入线程中的主函数，主要用来实现阻塞式的批准
        """
        # 创建socket
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定服务端主机号与端口号
        self.mySocket.bind((self.HOST,self.PORT))
        # 开始监听该主机号和端口号传入的信息
        self.mySocket.listen()

        while True:
            # 以阻塞式的方式来等待新的用户的接入
            conn, addr = self.mySocket.accept()
            # 创建针对于该客户端的玩家对象
            player1 = player.Player(room_manager=self.room_manager, conn=conn, addr=addr)
            # 将该玩家加入到list中
            self.player_list.append(player1)


if __name__ == "__main__":
    c1 = CentralThread()