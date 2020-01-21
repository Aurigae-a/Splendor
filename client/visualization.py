# 导入pygame包
import pygame
from pygame.locals import *
# 可视化所需要的一些控件
import widget
# 游戏中要用到的一些可视化类
import splendor as sp

class Visualization:
    """
    这个类主要是实现客户端端口的可视化的
    """
    def __init__(self,parent):
        """
        客户端可视化的初始化函数
        """
        # 记录可视化窗口类被调用的中心线程
        self.central_process = parent

    def initialization(self,width,height):
        """
        这个函数是用来做pygame模块的初始化的
        """
        # 记录从外界传来的窗口的高度和宽度
        self.width = width
        self.height = height
        # 初始化pygame模块组
        pygame.init()
        # 初始化主屏幕画布
        self.screen = pygame.display.set_mode((self.width,self.height))
        # 载入文本字体格式
        self.font1 = pygame.font.Font(None,30)
        self.font2 = pygame.font.Font(None,60)
        # 帧率控制器
        self.fpsClock = pygame.time.Clock()
        # 帧率
        self.FPS = 10
      
    def connection_init(self):
        """
        这个函数是用来对服务器连接阶段可视化窗口需要用到的变量进行初始化的
        """ 
        # 文本框
        self.connection_text_field = [
            widget.TextField(self.screen),
            widget.TextField(self.screen)
        ]
        # 初始化第1个文本框(地址文本框)
        self.connection_text_field[0].initialization(x=200, y=50, width=150, height=30, status_x=400, status_y=50, max_len=16, 
                                                     eff_in=['0','1','2','3','4','5','6','7','8','9','.'], font=self.font1, cursor_width=5)
        # 初始化第2个文本框(端口文本框)
        self.connection_text_field[1].initialization(x=200, y=100, width=150, height=30, status_x=400, status_y=100, max_len=16, 
                                                     eff_in=['0','1','2','3','4','5','6','7','8','9'], font=self.font1, cursor_width=5)

        # 文字标签
        self.connection_label = [
            widget.Label(self.screen),
            widget.Label(self.screen)
        ]
        # 初始化地址输入提示词
        self.connection_label[0].initialization(x=50, y=50, text="host address:", font=self.font1, color=pygame.Color("blue"))
        # 初始化端口输入提示词
        self.connection_label[1].initialization(x=50, y=100, text="port number:", font=self.font1, color=pygame.Color("blue"))
        
        # 按钮
        self.connection_button = [
            widget.PushButton(self.screen),
            widget.PushButton(self.screen)
        ]
        # 初始化确认按钮
        self.connection_button[0].initialization(x=150, y=250, text="Confirm", font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))
        # 初始化与取消按钮
        self.connection_button[1].initialization(x=250, y=250, text="Cancel", font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))

    def room_allocation_init(self):
        """
        房间分配的初始化函数
        """
        # 按钮
        self.room_allocation_button = []
        for index in range(4):
            self.room_allocation_button.append(widget.PushButton(self.screen))
        # 初始化确定按钮
        self.room_allocation_button[0].initialization(x=150, y=300, text="Confirm", font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))
        # 初始化取消按钮
        self.room_allocation_button[1].initialization(x=250, y=300, text="Quit", font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))
        # 初始化选项卡中的Create按钮
        self.room_allocation_button[2].initialization(x=50, y=50, text="Create", font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))
        # 初始化选项卡中的Join按钮
        self.room_allocation_button[3].initialization(x=130, y=50, text="Join", font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))

        # 初始化选项卡
        # 选项卡的选中状态 0:Create, 1:Join
        self.tab_combo_status = 0

        # 文字标签
        self.room_allocation_label = []
        for index in range(4):
            self.room_allocation_label.append(widget.Label(self.screen))
        # 设置人数标签
        self.room_allocation_label[0].initialization(x=50, y=100, text="Player # (2~4)", font=self.font1, color=pygame.Color('blue'))
        # 设置房间号码标签
        self.room_allocation_label[1].initialization(x=50, y=100, text="Room # (4 digits)", font=self.font1, color=pygame.Color('blue'))
        # 设置房间密码标签
        self.room_allocation_label[2].initialization(x=50, y=150, text="Password (6 digits)", font=self.font1, color=pygame.Color('blue'))
        # 设置用户名标签
        self.room_allocation_label[3].initialization(x=50, y=200, text="User Name", font=self.font1, color=pygame.Color('blue'))

        # 文本框
        self.room_allocation_text_field = []
        for index in range(4):
            self.room_allocation_text_field.append(widget.TextField(self.screen))
        # 初始化第1个文本框(玩家数量)
        self.room_allocation_text_field[0].initialization(x=250, y=100, width=100, height=30, status_x=380, status_y=100, max_len=1, 
                                                          eff_in=['2','3','4'], font=self.font1, cursor_width=5)
        # 初始化第2个文本框(房间名称)
        self.room_allocation_text_field[1].initialization(x=250, y=100, width=100, height=30, status_x=380, status_y=100, max_len=4, 
                                                          eff_in=['0','1','2','3','4','5','6','7','8','9'], font=self.font1, cursor_width=5)
        # 初始化第3个文本框(房间密码)
        self.room_allocation_text_field[2].initialization(x=250, y=150, width=100, height=30, status_x=380, status_y=150, max_len=6, 
                                                          eff_in=['0','1','2','3','4','5','6','7','8','9'], font=self.font1, cursor_width=5)
        # 初始化第4个文本框(用户名)
        self.room_allocation_text_field[3].initialization(x=250, y=200, width=100, height=30, status_x=380, status_y=200, max_len=8, 
                                                          eff_in=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                                                                  'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'], 
                                                          font=self.font1, cursor_width=5)

    def room_init(self):
        """
        当客户端处于房间状态时的初始化函数
        """
        # 房间号
        self.room_num = ""
        # 玩家列表控件
        self.room_player_list = []
        # 玩家准备状态
        self.room_ready = False

        # 房间号标签
        self.room_label_list = []
        for index in range(14):
            self.room_label_list.append(widget.Label(self.screen))
        # 房间号指示标签
        self.room_label_list[0].initialization(x=50, y=50, text="Room #", font=self.font1, color=pygame.Color('blue'))
        # 房间号标签
        self.room_label_list[1].initialization(x=150, y=50, text="", font=self.font1, color=pygame.Color('blue'))
        # 玩家显示标签
        for p_index in range(4):
            # player标签
            self.room_label_list[2+3*p_index+0].initialization(x=50, y=100+50*p_index, text="player:", font=self.font1, color=pygame.Color('blue'))
            # 玩家名称标签
            self.room_label_list[2+3*p_index+1].initialization(x=150, y=100+50*p_index, text="", font=self.font1, color=pygame.Color('red'))
            # 准备标签
            self.room_label_list[2+3*p_index+2].initialization(x=300, y=100+50*p_index, text="", font=self.font1, color=pygame.Color('green'))

        # 按钮控件
        self.room_button_list = []
        for index in range(2):
            self.room_button_list.append(widget.PushButton(self.screen))
        # 准备按钮
        self.room_button_list[0].initialization(x=150, y=350, text='Ready', font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))
        # 退出按钮
        self.room_button_list[1].initialization(x=250, y=350, text='Quit', font=self.font1, font_color=pygame.Color('yellow'), bg_color=pygame.Color('blue'))

    def game_init(self):
        """
        游戏状态下的初始化函数
        """
        # 初始化游戏的各个类
        sp.Player.initialization()
        sp.Token.initialization()
        sp.Card.initialization()
        sp.Noble.initialization()
        sp.CardChanger.initialization()

        # 初始化玩家的位置
        self.game_player_pos = [[10,110],[830,110],[10,340],[830,340]]
        # 初始化玩家列表
        self.game_player_list = []
        for index in range(4):
            game_player = sp.Player(parent=self.screen,name="",x=self.game_player_pos[index][0],y=self.game_player_pos[index][1])
            self.game_player_list.append(game_player)

        # 初始化贵族的位置
        self.game_noble_pos = [[200,30],[285,30],[370,30],[455,30],[540,30]]
        # 初始化贵族
        self.game_noble_list = []
        for index in range(5):
            game_noble = sp.Noble(parent=self.screen,x=self.game_noble_pos[index][0],y=self.game_noble_pos[index][1])
            self.game_noble_list.append(game_noble)
        
        # 初始化筹码的位置
        self.game_token_pos = [[200,130],[305,130],[410,130],[515,130],[620,130],[725,130]]
        # 初始化筹码
        self.game_token_list = []
        for index in range(6):
            game_token = sp.Token(parent=self.screen,color=index,x=self.game_token_pos[index][0],y=self.game_token_pos[index][1])
            self.game_token_list.append(game_token)
        
        # 初始化卡牌的位置
        self.game_card_pos = [[[305,240],[410,240],[515,240],[620,240]],
                              [[305,405],[410,405],[515,405],[620,405]],
                              [[305,570],[410,570],[515,570],[620,570]]]
        # 初始化卡牌
        self.game_card_list = []
        for level in range(3):
            # 三种不同的卡片
            card_level = []
            for card_index in range(4):
                # 每种卡片有4张
                card = sp.Card(parent=self.screen,x=self.game_card_pos[level][card_index][0],y=self.game_card_pos[level][card_index][1])
                card_level.append(card)
            self.game_card_list.append(card_level)

        # 初始化标签
        self.game_label = []
        for index in range(12):
            self.game_label.append(widget.Label(parent=self.screen))
        # 初始化4个玩家标签
        self.game_label[0].initialization(x=10,y=90,text="Player 1",font=self.font1,color=pygame.Color('blue'))
        self.game_label[1].initialization(x=830,y=90,text="Player 2",font=self.font1,color=pygame.Color('blue'))
        self.game_label[2].initialization(x=10,y=320,text="Player 3",font=self.font1,color=pygame.Color('blue'))
        self.game_label[3].initialization(x=830,y=320,text="Player 4",font=self.font1,color=pygame.Color('blue'))
        # 初始化noble标签
        self.game_label[4].initialization(x=200,y=10,text="Noble",font=self.font1,color=pygame.Color('blue'))
        # 初始化token标签
        self.game_label[5].initialization(x=200,y=110,text="Token",font=self.font1,color=pygame.Color('blue'))
        # 初始化3种card的数量标签
        self.game_label[6].initialization(x=200,y=310,text="Level 1: ",font=self.font1,color=pygame.Color('green'))
        self.game_label[7].initialization(x=200,y=475,text="Level 2: ",font=self.font1,color=pygame.Color('green'))
        self.game_label[8].initialization(x=200,y=640,text="Level 3: ",font=self.font1,color=pygame.Color('green'))
        # 初始化指示自己姓名的标签
        self.game_label[9].initialization(x=10,y=10,text="I am "+self.game_myName,font=self.font1,color=pygame.Color('red'))
        # 初始化游戏轮次指示器
        self.game_label[10].initialization(x=10,y=40,text=" ",font=self.font1,color=pygame.Color('green'))
        # 初始化提示器
        self.game_label[11].initialization(x=830,y=10,text="Hint:",font=self.font1,color=pygame.Color('green'))

        # 初始化轮次
        self.game_turn = 0
        # 初始化自己的轮次
        self.game_my_turn_num = 0
        # 初始化过程控制器
        try:
            # 进行这样的try是为了防止房间发来的当前回合信息比游戏开始信息来的更早而重置了game_my_turn的值
            if self.game_my_turn == True:
                pass
        except AttributeError:
            # 初始化是否是自己的回合的指示器
            self.game_my_turn = False
            # 初始化提示器状态
            self.game_hint_state = -1
        # 初始化操作指示器
        self.game_operation = 0
        # 初始化筹码选择器
        self.game_token_cart = []
        # 初始化卡牌选择器
        self.game_card_cart = []

        # 初始化按钮
        self.game_button_list = []
        for index in range(6):
            self.game_button_list.append(widget.PushButton(parent=self.screen))
        # 初始化“take 3”按钮
        self.game_button_list[0].initialization(x=1030,y=380,text="Take 3",font=self.font1,font_color=pygame.Color('yellow'),bg_color=pygame.Color('blue'))
        # 初始化“take 2”按钮
        self.game_button_list[1].initialization(x=1030,y=410,text="Take 2",font=self.font1,font_color=pygame.Color('yellow'),bg_color=pygame.Color('blue'))
        # 初始化“reserve”按钮
        self.game_button_list[2].initialization(x=1030,y=440,text="Reserve",font=self.font1,font_color=pygame.Color('yellow'),bg_color=pygame.Color('blue'))
        # 初始化“change”按钮
        self.game_button_list[3].initialization(x=1030,y=470,text="Change",font=self.font1,font_color=pygame.Color('yellow'),bg_color=pygame.Color('blue'))
        # 初始化“skip”按钮
        self.game_button_list[4].initialization(x=1030,y=500,text="Skip",font=self.font1,font_color=pygame.Color('yellow'),bg_color=pygame.Color('blue'))
        # 初始化“Confirm”按钮
        self.game_button_list[5].initialization(x=1030,y=530,text="Confirm",font=self.font1,font_color=pygame.Color('yellow'),bg_color=pygame.Color('blue'))

        # 初始化换牌器
        self.game_card_changer = sp.CardChanger(parent=self.screen,pos=[725,570])

    def finished_init(self,winner_index):
        """
        游戏结束的初始化
        """
        # 初始化标签
        self.finished_label = widget.Label(parent=self.screen)
        self.finished_label.initialization(x=100,y=300,text="Winner: "+self.game_player_list[winner_index].name,font=self.font1,color=pygame.Color('red'))

        # 初始化按钮
        self.finishe_button = widget.PushButton(parent=self.screen)
        self.finishe_button.initialization(x=630,y=550,text="Ok",font=self.font1,font_color=pygame.Color('yellow'),bg_color=pygame.Color('blue'))

    def connection(self):
        """
        这个部分实现可视化窗口的第一个阶段，连接请求状态
        """
        # 画出黑色背景
        self.screen.fill((0,0,0))
        
        # 画出地址与端口的提示词
        for lb in self.connection_label:
            lb.show()
    
        # 对文本框进行渲染
        for tf in self.connection_text_field:
            tf.show()
        
        # 画出两个按钮
        for bt in self.connection_button:
            bt.show()

        # 对当前屏幕进行同步与渲染
        pygame.display.update()
        # 控制帧率
        self.fpsClock.tick(self.FPS)

        """
        事件处理部分
        """
        # 处理鼠标与键盘的事件
        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出事件
                self.central_process.state = -1

            elif event.type == MOUSEBUTTONDOWN:
                # 鼠标被按下事件
                if self.connection_text_field[0].inRange(event.pos):
                    # 判断鼠标是否在地址输入框中
                    # 地址输入框激活，其他输入框锁定
                    self.connection_text_field[0].enable = True
                    self.connection_text_field[1].enable = False

                elif self.connection_text_field[1].inRange(event.pos):
                    # 判断鼠标是否在端口输入框中
                    # 端口输入框激活，其他输入框锁定
                    self.connection_text_field[0].enable = False
                    self.connection_text_field[1].enable = True

                else:
                    # 如果鼠标点在了别处，那么全部锁定
                    self.connection_text_field[0].enable = False
                    self.connection_text_field[1].enable = True
                    
                    if self.connection_button[0].inRange(event.pos):
                        # 确认按钮被点击
                        # 获得host字符串
                        self.host = self.connection_text_field[0].getText(0)
                        # 获得port数字
                        self.port = self.connection_text_field[1].getText(1)
                        # 切换状态至尝试登录状态
                        self.central_process.state = 1
                    
                    elif self.connection_button[1].inRange(event.pos):
                        #  取消按钮被按下，退出客户端程序
                        self.central_process.state = -1

            elif event.type == KEYDOWN:
                # 键盘按下事件
                if self.connection_text_field[0].enable == True:
                    self.connection_text_field[0].keyTapIn(event)
                elif self.connection_text_field[1].enable == True:
                    self.connection_text_field[1].keyTapIn(event)

    def room_allocation(self):
        """
        房间分配的绘图部分
        """
        # 将背景涂成黑色
        self.screen.fill(pygame.Color(0,0,0))

        # 画出所有按钮
        for bt in self.room_allocation_button:
            bt.show()

        # 画出文本输入框与文字标签
        if self.tab_combo_status == 0:
            # Create按钮被选中
            self.room_allocation_label[0].show()
            self.room_allocation_text_field[0].show()
        else:
            # Join按钮被选中
            self.room_allocation_label[1].show()
            self.room_allocation_text_field[1].show()
        self.room_allocation_label[2].show()
        self.room_allocation_text_field[2].show()
        self.room_allocation_label[3].show()
        self.room_allocation_text_field[3].show()

        # 同步屏幕
        pygame.display.update()
        # 控制帧率
        self.fpsClock.tick(self.FPS)

        """
        事件处理部分
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出事件
                # 将主线程的状态设置为退出状态
                self.central_process.state = -1
            
            elif event.type == KEYDOWN:
                # 键盘被按下事件
                if self.room_allocation_text_field[0].enable == True:
                    self.room_allocation_text_field[0].keyTapIn(event)
                
                elif self.room_allocation_text_field[1].enable == True:
                        self.room_allocation_text_field[1].keyTapIn(event)
                    
                elif self.room_allocation_text_field[2].enable == True:
                    self.room_allocation_text_field[2].keyTapIn(event)
                
                elif self.room_allocation_text_field[3].enable == True:
                    self.room_allocation_text_field[3].keyTapIn(event)
            
            elif event.type == MOUSEBUTTONDOWN:
                # 鼠标被按下事件
                # 获得鼠标点击位置信息
                """
                检查两个文本输入框的输入状态
                """
                if self.room_allocation_text_field[0].inRange(event.pos) == True:
                    if self.tab_combo_status==0:
                        # 第1个文本框被选中
                        self.room_allocation_text_field[0].enable = True
                        self.room_allocation_text_field[1].enable = False
                        self.room_allocation_text_field[2].enable = False
                        self.room_allocation_text_field[3].enable = False
                    else:
                        # 第2个文本框被选中
                        self.room_allocation_text_field[0].enable = False
                        self.room_allocation_text_field[1].enable = True
                        self.room_allocation_text_field[2].enable = False
                        self.room_allocation_text_field[3].enable = False

                elif self.room_allocation_text_field[2].inRange(event.pos) == True:
                    # 第3个文本框被选中
                    self.room_allocation_text_field[0].enable = False
                    self.room_allocation_text_field[1].enable = False
                    self.room_allocation_text_field[2].enable = True
                    self.room_allocation_text_field[3].enable = False
                
                elif self.room_allocation_text_field[3].inRange(event.pos) == True:
                    # 第4个文本框被选中
                    self.room_allocation_text_field[0].enable = False
                    self.room_allocation_text_field[1].enable = False
                    self.room_allocation_text_field[2].enable = False
                    self.room_allocation_text_field[3].enable = True
                    
                else:
                    # 鼠标点中了其他位置，这个时候4个文本框均被锁定
                    for index in range(len(self.room_allocation_text_field)):
                        self.room_allocation_text_field[index].enable = False
                
                """
                按钮处理界面
                """
                if self.room_allocation_button[2].inRange(event.pos):
                    # 表示鼠标点中了Create按钮
                    self.tab_combo_status = 0
                
                elif self.room_allocation_button[3].inRange(event.pos):
                    # 表示鼠标点中了Join按钮
                    self.tab_combo_status = 1
                
                elif self.room_allocation_button[0].inRange(event.pos):
                    # 表示鼠标点中了Confirm按钮
                    # 创建一个字节串作为命令
                    if self.tab_combo_status == 0:
                        cmd = b'000'
                        # 处理房间人数
                        player_num = self.room_allocation_text_field[0].getText(0)
                        if player_num != "":
                            cmd = cmd + player_num.encode(encoding='utf-8')
                        else:
                            continue
                        
                    else:
                        cmd = b'003'
                        # 处理房间号码
                        self.room_num = self.room_allocation_text_field[1].getText(0)
                        if len(self.room_num) == 4:
                            cmd = cmd + self.room_num.encode(encoding='utf-8')
                        else:
                            continue

                    # 处理密码
                    password = self.room_allocation_text_field[2].getText(0)
                    cmd = cmd + str(len(password)).encode(encoding='utf-8')
                    cmd = cmd + password.encode(encoding='utf-8')

                    # 处理玩家名称
                    username = self.room_allocation_text_field[3].getText(0)
                    cmd = cmd + str(len(username)).encode(encoding='utf-8')
                    cmd = cmd + username.encode(encoding='utf-8')
                    self.game_myName = username

                    # 向服务端发送消息
                    self.central_process.client_socket.send(cmd)
                    
                    # 将主线程的状态机设置为房间请求状态
                    self.central_process.state = 3
                
                elif self.room_allocation_button[1].inRange(event.pos):
                    # 表示鼠标点中了Quit按钮
                    # 退出连接，回到连接请求界面
                    self.central_process.state = 0
                    # 结束socket的两个线程的生命周期
                    self.central_process.client_socket.running = False
                    self.central_process.client_socket = None

    def room_apply(self):
        """
        房间申请处理函数
        """
        self.screen.fill(pygame.Color(0,0,0))

        pygame.display.update()
        # 控制帧率
        self.fpsClock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出事件
                self.central_process.state = -1

    def room(self):
        """
        当客户端处于房间状态时的可视化窗口
        """
        # 画出背景图
        self.screen.fill(pygame.Color(0,0,0))

        # 更新房间标签
        self.room_label_list[1].set_text(self.room_num)
        for index in range(len(self.room_player_list)):
            # 更新玩家名称
            self.room_label_list[3+3*index].set_text(self.room_player_list[index][0])
            # 更新玩家状态
            if self.room_player_list[index][1] == 0:
                self.room_label_list[4+3*index].set_text("Not ready")
            else:
                self.room_label_list[4+3*index].set_text("Ready")

        # 画出房间号标签
        for index in range(len(self.room_player_list)*3+2):
            self.room_label_list[index].show()

        # 画出所有按钮
        for pb in self.room_button_list:
            pb.show()

        pygame.display.update()
        # 控制帧率
        self.fpsClock.tick(self.FPS)

        """
        事件处理部分
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出事件
                self.central_process.state = -1
            
            elif event.type == MOUSEBUTTONDOWN:
                # 鼠标被按下时间
                if self.room_button_list[0].inRange(event.pos):
                    # 表示准备按钮被按下
                    if self.room_ready == False:
                        self.central_process.client_socket.send(b'0071')
                        self.room_ready = True
                    else:
                        self.central_process.client_socket.send(b'0070')
                        self.room_ready = False
                
                elif self.room_button_list[1].inRange(event.pos):
                    # 表示退出按钮被按下
                    self.central_process.client_socket.send(b'0040')
                    # 返回已登陆未加入房间状态
                    self.central_process.state = 2

    def game(self):
        """
        游戏状态下的可视化方法
        """
        # 画出背景图
        self.screen.fill(pygame.Color(0,0,0))

        # 设置hint
        if self.game_hint_state == 0:
            # 表示当前什么操作也没选
            self.game_label[11].set_text("Choose an operation")
        elif self.game_hint_state == 1:
            # 表示选择了拿三个不同颜色的token
            self.game_label[11].set_text("Choose 3 tokens with diff colors")
        elif self.game_hint_state == 2:
            # 表示选择选择数未达到3个，要求其重新选择
            self.game_label[11].set_text("Current choice is lower than 3")
        elif self.game_hint_state == 3:
            # 表示玩家手中的牌数再拿就会超出10个
            self.game_label[11].set_text("player cannot hold more than 10 tokens")
        elif self.game_hint_state == 4:
            # 表示选择了拿2个不同颜色的token
            self.game_label[11].set_text("Choose 2 tokens with same color")
        elif self.game_hint_state == 5:
            # 表示选择选择数未达到1个，要求其重新选择
            self.game_label[11].set_text("Current choice is lower than 1")
        elif self.game_hint_state == 6:
            # 表示玩家手中的金色token数大于2
            self.game_label[11].set_text("Cannot have more than 2 golden tokens")
        elif self.game_hint_state == 7:
            # 表示玩家手中reserve牌的数量大于2
            self.game_label[11].set_text("Cannot reserve more than 2 cards")
        elif self.game_hint_state == 8:
            # 表示玩家开始选牌
            self.game_label[11].set_text("Choose a card to reserve")
        elif self.game_hint_state == 9:
            # 表示当前场上已经没有金色的token了
            self.game_label[11].set_text("There's no golden tokens now")
        elif self.game_hint_state == 10:
            # 表示换牌开始
            self.game_label[11].set_text("Choose a card to change")
        elif self.game_hint_state == 11:
            # 表示换牌开始
            self.game_label[11].set_text("The given tokens don't match the demand")
        else:
            # 表示需要等待其他玩家
            self.game_label[11].set_text("Wait for other players")

        # 画出所有的标签
        for lb in self.game_label:
            lb.show()
        
        # 画出所有的按钮
        for pb in self.game_button_list:
            pb.show()

        # 画出所有的玩家
        for player in self.game_player_list:
            player.show()
        
        # 画出所有的贵族
        for noble in self.game_noble_list:
            noble.show()
        
        # 画出所有的筹码
        for token in self.game_token_list:
            token.show()
        
        # 画出所有的卡片
        for card_list in self.game_card_list:
            for card in card_list:
                card.show()
        
        # 画出自己reserved的卡片
        for card in self.game_player_list[self.game_my_turn_num].reserve:
            card.show()
        
        # 画出卡牌选择器
        self.game_card_changer.show()

        pygame.display.update()
        # 控制帧率
        self.fpsClock.tick(self.FPS)
        
        """
        事件处理部分
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出事件
                self.central_process.state = -1

            if event.type == MOUSEBUTTONDOWN:
                # 鼠标按下事件

                # # # # # # # # # #
                # 操作类型按钮被按下 #
                # # # # # # # # # #
                if self.game_button_list[0].inRange(event.pos) and self.game_my_turn:
                    # 拿3个token的按钮被按下
                    if self.game_player_list[self.game_turn].get_token_num() > 7:
                        # 表示玩家手中的手牌数不能再拿3个了
                        self.game_hint_state = 3
                    else:
                        self.game_operation = 1
                        # 对提示器进行相应设置
                        self.game_hint_state = 1
                        # 重置
                        self.game_reset()
                
                elif self.game_button_list[1].inRange(event.pos) and self.game_my_turn:
                    # 拿2个token的按钮被按下
                    if self.game_player_list[self.game_turn].get_token_num() > 8:
                        # 表示玩家手中的手牌数不能再拿2个了
                        self.game_hint_state = 3
                    else:
                        self.game_operation = 2
                        # 对提示器进行相应设置
                        self.game_hint_state = 4
                        # 重置
                        self.game_reset()
                
                elif self.game_button_list[2].inRange(event.pos) and self.game_my_turn:
                    # reserve按钮被按下
                    if self.game_player_list[self.game_turn].get_token_num() < 10:
                        if self.game_player_list[self.game_turn].token[5] < 2:
                            if self.game_player_list[self.game_turn].get_reserved_num() < 2:
                                if self.game_token_list[5].num > 0:
                                    # 进入选牌状态
                                    self.game_operation = 3
                                    # 对提示器进行相应设置
                                    self.game_hint_state = 8
                                    # 重置
                                    self.game_reset()
                                else:
                                    # 表示当前场上已经没有金色的token了
                                    self.game_hint_state = 9
                                    self.game_operation = 0
                            else:
                                # 表示该玩家手中reserve牌的数量大于2
                                self.game_hint_state = 7
                                self.game_operation = 0
                        else:
                            # 表示该玩家手中的金色token数大于2
                            self.game_hint_state = 6
                            self.game_operation = 0
                    else:
                        # 表示玩家手中的手牌数不能再拿1个了
                        self.game_hint_state = 3
                        self.game_operation = 0
                
                elif self.game_button_list[3].inRange(event.pos) and self.game_my_turn:
                    # change按钮被按下
                    self.game_operation = 4
                    self.game_hint_state = 10
                    # 重置
                    self.game_reset()
                
                # # # # # # # # #
                # 返回型按钮被按下 #
                # # # # # # # # #
                elif self.game_button_list[5].inRange(event.pos) and self.game_my_turn:
                    # confirm按钮被按下
                    if self.game_operation == 1:
                        # 表示该玩家要做的操作是拿三个不同颜色的token
                        if len(self.game_token_cart) == 3:
                            # 所选择的token共有三个颜色
                            msg = b'012'
                            for token in self.game_token_cart:
                                msg = msg + str(token.color).encode(encoding='utf-8')
                            # 向服务端发送消息
                            self.central_process.client_socket.send(msg)
                        else:
                            # 如果没有达到，则返回
                            self.game_hint_state = 2
                            continue

                    elif self.game_operation == 2:
                        # 表示该玩家要做的操作是拿两个相同颜色的token
                        if len(self.game_token_cart) == 1:
                            # 所选择的token共有1个颜色
                            msg = b'013'
                            for token in self.game_token_cart:
                                msg = msg + str(token.color).encode(encoding='utf-8')
                            # 向服务端发送消息
                            self.central_process.client_socket.send(msg)
                        else:
                            # 如果没有达到，则返回
                            self.game_hint_state = 5
                            continue
                    
                    elif self.game_operation == 3:
                        # 表示该玩家要做的操作是reserve牌
                        if len(self.game_card_cart) == 1:
                            # 所选择的card共有1张
                            msg = b'014'
                            for level in range(3):
                                for card_index in range(4):
                                    if self.game_card_list[level][card_index].selected == True:
                                        msg = msg + str(level).encode(encoding='utf-8') + str(card_index).encode(encoding='utf-8')
                                        break
                            # 向服务端发送消息
                            self.central_process.client_socket.send(msg)
                        else:
                            # 如果没有达到，则返回
                            self.game_hint_state = 5
                            continue
                    
                    elif self.game_operation == 4:
                        # 表示玩家进行的是换牌操作
                        if len(self.game_card_cart) == 1:
                            # 当前有牌被选中
                            if self.game_card_changer.checkValid():
                                # 表示换牌成功
                                found = False
                                # 从牌堆中寻找被选中牌的level和index
                                for level in range(3):
                                    for index in range(4):
                                        if self.game_card_list[level][index].selected == True:
                                            found = True
                                            break
                                    if found:
                                        break
                                if found:
                                    # 如果找到了，则按照从牌堆中换牌的指令来通信
                                    msg = b'016' + str(level).encode(encoding='utf-8') + str(index).encode(encoding='utf-8')
                                else:
                                    # 如果没找到，则要继续在reserve的牌中找
                                    for index in range(len(self.game_player_list[self.game_my_turn_num].reserve)):
                                        if self.game_player_list[self.game_my_turn_num].reserve[index].selected:
                                            break
                                    msg = b'017' + str(index).encode(encoding='utf-8')

                                # 准备筹码信息
                                token_cost = self.game_card_changer.get_decision()
                                for color in range(6):
                                    msg = msg + str(token_cost[color]).encode(encoding='utf-8')

                                # 向服务端发送消息
                                self.central_process.client_socket.send(msg)
                            else:
                                # 表示换牌没有成功
                                self.game_hint_state = 11
                                continue
                        else:
                            # 当前没有牌被选中
                            self.game_hint_state = 10
                            continue

                    if self.game_operation != 0:
                        # 自己的回合结束
                        self.game_my_turn = False
                        # 将操作指示器重置为空
                        self.game_operation = 0
                        # 重置
                        self.game_reset()
                        # 将提示器重置为等待他人
                        self.game_hint_state = -1
                
                elif self.game_button_list[4].inRange(event.pos) and self.game_my_turn:
                    # skip按钮被按下
                    self.central_process.client_socket.send(b'019')
                    # 自己的回合结束
                    self.game_my_turn = False
                    # 将操作指示器重置为空
                    self.game_operation = 0
                    # 重置
                    self.game_reset()
                    # 将提示器重置为等待他人
                    self.game_hint_state = -1

                # # # # # # # # # #
                # token 按钮被按下  #
                # # # # # # # # # #
                for token_index in range(5):
                    token = self.game_token_list[token_index]

                    if token.inRange(event.pos):
                        # 如果是前5个token被选中的话
                        if self.game_operation == 1:
                            # 选三种颜色
                            token.selete(cart=self.game_token_cart,type_num_max=3,remain_num=0)

                        elif self.game_operation == 2:
                            # 选一种颜色
                            token.selete(cart=self.game_token_cart,type_num_max=1,remain_num=3)
                
                # # # # # # # # # #
                #  card 按钮被按下  #
                # # # # # # # # # #
                for level in range(3):
                    for card in self.game_card_list[level]:
                        if card.inRange(event.pos):
                            if self.game_operation == 3:
                                # 表示当前的操作是reserve牌
                                card.select(cart=self.game_card_cart,upper_num=1)
                            
                            elif self.game_operation == 4:
                                # 表达当前的操作是换牌
                                card.select(cart=self.game_card_cart,upper_num=1)
                                # 对换牌器进行切换
                                if card.selected == True:
                                    # 表示当前有卡牌被选中
                                    self.game_card_changer.update(player=self.game_player_list[self.game_my_turn_num],card=card)
                                else:
                                    # 表示当前卡牌被取消选中
                                    self.game_card_changer.enable = False
                
                for card in self.game_player_list[self.game_my_turn_num].reserve:
                    if card.enable == True and card.inRange(event.pos):
                        # 表示reserve栏的card被选中
                        if self.game_operation == 4:
                            # 表示当前操作为换牌操作
                            card.select(cart=self.game_card_cart,upper_num=1)
                            # 对换牌器进行切换
                            if card.selected == True:
                                # 表示当前有卡牌被选中
                                self.game_card_changer.update(player=self.game_player_list[self.game_my_turn_num],card=card)
                            else:
                                # 表示当前卡牌被取消选中
                                self.game_card_changer.enable = False
                
                # # # # # # # # #
                # 选择器执行操作  # 
                # # # # # # # # #
                self.game_card_changer.mouseEvent(event.pos)
    
    def game_reset(self):
        """
        重置所有的显示组件
        """
        # 对token的选择器和每个token的选择状态进行重置
        # 清空选择器
        self.game_token_cart = []
        # 将所有的token设置为未选择状态
        for token in self.game_token_list:
            token.selected = False
        
        # 对card的选择器和每个card的选择状态进行重置
        # 清空选择器
        self.game_card_cart = []
        # 将所有的card设置为未选择状态
        for level in range(3):
            for card in self.game_card_list[level]:
                card.selected = False
        for card in self.game_player_list[self.game_my_turn_num].reserve:
            if card.enable == True:
                card.selected = False
        
        # 清空换牌器
        self.game_card_changer.enable = False
        
    def finished(self):
        """
        游戏结束后的可视化方案
        """
        # 画出黑色背景
        self.screen.fill((0,0,0))

        # 显示标签
        self.finished_label.show()
        # 显示按钮
        self.finishe_button.show()
        
        # 对当前屏幕进行同步与渲染
        pygame.display.update()
        # 控制帧率
        self.fpsClock.tick(self.FPS)

        """
        事件处理部分
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                # 退出事件
                self.central_process.state = -1
            
            elif event.type == MOUSEBUTTONDOWN:
                # 鼠标按下事件
                if self.finishe_button.inRange(event.pos):
                    # Ok按钮被按下，则主线程重新回到房间状态
                    self.central_process.state = 4