# 导入可视化窗口包
import visualization as vs
# 导入用于通讯的包
import client_connection as cc

class MainProcess:
    """
    这个类是客户端程序的主要调度类
    """
    def __init__(self):
        """
        主线程初始化函数：
            state: 表示状态机当前的状态
            main_window: 可视化窗口
            client_socket: 和服务器进行信息交互的封装好的socket类
        """
        # 初始化状态机的状态变量
        self.state = 0
        # 初始化主机号与端口号
        self.HOST = ""
        self.PORT = 0
        
        # 创建主窗口
        self.main_window = vs.Visualization(self)
        self.main_window.initialization(1280,720)
        # 对第一阶段可视化窗口进行初始化
        self.main_window.connection_init()

        # 创建通信组件
        self.client_socket = None
        
        # 调用主循环
        self.mainLoop()
    
    def __del__(self):
        print('Farewell')
    
    def mainLoop(self):
        """
        客户端程序的主循环
        """
        while self.state != -1:
            # -1 表示客户端程序需要退出
            if self.state == 0:
                # 0 表示客户端程序处于连接请求状态
                self.main_window.connection()
            
            elif self.state == 1:
                # 1 表示客户端程序处于尝试登录状态
                # 初始化可视化界面的登陆后状态
                self.main_window.room_allocation_init()
                # 创建通信组件
                self.client_socket = cc.ClientConnection(self)
                # 尝试登陆
                self.client_socket.connect(self.main_window.host,self.main_window.port)
            
            elif self.state == 2:
                # 2 表示登陆后状态，需要对房间进行分配
                self.main_window.room_allocation()
            
            elif self.state == 3:
                # 3 表示房间请求状态
                # 初始化房间界面
                self.main_window.room_init()
                # 处理可视化窗口
                self.main_window.room_apply()
            
            elif self.state == 4:
                # 4 房间状态
                self.main_window.room()
            
            elif self.state == 5:
                # 5 游戏前的准备状态
                self.main_window.game_init()
                self.state = 6
            
            elif self.state == 6:
                # 6 游戏状态
                self.main_window.game()
            
            elif self.state == 7:
                # 7 游戏后状态
                self.main_window.finished()

if __name__ == "__main__":
    my_process = MainProcess()
