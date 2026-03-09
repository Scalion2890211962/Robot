import time
import sys
import tkinter as tk
from tkinter import ttk, messagebox


class Robot:
    """模拟可运动的机器人类"""

    def __init__(self):
        # 初始化机器人状态
        self.speed = 0  # 速度，范围 0-100
        self.direction = "stop"  # 方向：forward/backward/left/right/stop
        self.is_moving = False  # 是否处于运动状态
        # 图形化相关属性
        self.pos_x = 250  # 机器人在画布中的X坐标
        self.pos_y = 250  # 机器人在画布中的Y坐标
        self.angle = 0  # 机器人朝向角度（0=上/前，90=右，180=下/后，270=左）

    def forward(self, speed=50):
        """前进"""
        if 0 <= speed <= 100:
            self.speed = speed
            self.direction = "forward"
            self.is_moving = True
            self.angle = 0  # 前进朝向正上方
            # 模拟位置移动
            if self.pos_y > 50:
                self.pos_y -= 5
            print(f"机器人前进 | 速度：{self.speed}")
        else:
            print("速度无效！请输入 0-100 之间的数值")
            return False
        return True

    def backward(self, speed=50):
        """后退"""
        if 0 <= speed <= 100:
            self.speed = speed
            self.direction = "backward"
            self.is_moving = True
            self.angle = 180  # 后退朝向正下方
            # 模拟位置移动
            if self.pos_y < 450:
                self.pos_y += 5
            print(f"机器人后退 | 速度：{self.speed}")
        else:
            print("速度无效！请输入 0-100 之间的数值")
            return False
        return True

    def turn_left(self, speed=30):
        """左转"""
        if 0 <= speed <= 100:
            self.speed = speed
            self.direction = "left"
            self.is_moving = True
            self.angle = 270  # 左转朝向左侧
            # 模拟位置移动
            if self.pos_x > 50:
                self.pos_x -= 5
            print(f"机器人左转 | 速度：{self.speed}")
        else:
            print("速度无效！请输入 0-100 之间的数值")
            return False
        return True

    def turn_right(self, speed=30):
        """右转"""
        if 0 <= speed <= 100:
            self.speed = speed
            self.direction = "right"
            self.is_moving = True
            self.angle = 90  # 右转朝向右侧
            # 模拟位置移动
            if self.pos_x < 450:
                self.pos_x += 5
            print(f"机器人右转 | 速度：{self.speed}")
        else:
            print("速度无效！请输入 0-100 之间的数值")
            return False
        return True

    def stop(self):
        """停止运动"""
        self.speed = 0
        self.direction = "stop"
        self.is_moving = False
        print("机器人已停止")
        return True

    def get_status(self):
        """获取当前状态"""
        status = {
            "is_moving": self.is_moving,
            "direction": self.direction,
            "speed": self.speed,
            "position": (self.pos_x, self.pos_y),
            "angle": self.angle
        }
        return status


class RobotGUI:
    """机器人图形化控制界面（对称布局+缩小尺寸）"""

    def __init__(self, root):
        self.root = root
        self.root.title("机器人运动控制系统")
        # 恢复适中的窗口尺寸
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # 创建机器人实例
        self.robot = Robot()

        # 初始化界面组件
        self._create_widgets()
        # 初始化画布
        self._init_canvas()
        # 定时更新界面
        self._update_gui()

    def _create_widgets(self):
        """创建界面组件（对称布局+缩小控制区，修复样式错误）"""
        # 1. 运动控制区（缩小尺寸：350x280，对称布局）
        control_frame = ttk.LabelFrame(self.root, text="运动控制", padding=15)
        control_frame.place(x=20, y=20, width=350, height=280)  # 缩小尺寸，保证对称

        # 速度调节（居中对称布局）
        speed_frame = ttk.Frame(control_frame)
        speed_frame.grid(row=0, column=0, columnspan=3, pady=10)  # 整行居中
        ttk.Label(speed_frame, text="速度调节：", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.IntVar(value=50)
        # 修复：移除自定义Scale样式，使用默认样式，直接设置滑块长度
        speed_slider = ttk.Scale(speed_frame, from_=0, to=100, variable=self.speed_var,
                                 orient="horizontal", length=200)
        speed_slider.pack(side=tk.LEFT, padx=5)
        self.speed_label = ttk.Label(speed_frame, text="50", font=("Arial", 12))
        self.speed_label.pack(side=tk.LEFT, padx=5)
        speed_slider.bind("<Motion>", lambda e: self.speed_label.config(text=str(self.speed_var.get())))

        # 自定义按钮样式（仅定义Button，避免Scale样式错误）
        btn_style = ttk.Style()
        btn_style.configure("Normal.TButton", font=("Arial", 12), padding=8)

        # 运动按钮（严格对称布局）
        # 前进按钮（居中）
        forward_btn = ttk.Button(control_frame, text="前进", style="Normal.TButton",
                                 command=lambda: self.robot.forward(self.speed_var.get()))
        forward_btn.grid(row=1, column=1, padx=25, pady=8, ipadx=15)  # 左右等距padx=25，保证对称

        # 左转+右转按钮（左右对称，等距）
        left_btn = ttk.Button(control_frame, text="左转", style="Normal.TButton",
                              command=lambda: self.robot.turn_left(self.speed_var.get()))
        left_btn.grid(row=2, column=0, padx=25, pady=8, ipadx=15)  # 左侧等距

        right_btn = ttk.Button(control_frame, text="右转", style="Normal.TButton",
                               command=lambda: self.robot.turn_right(self.speed_var.get()))
        right_btn.grid(row=2, column=2, padx=25, pady=8, ipadx=15)  # 右侧等距，与左转对称

        # 后退按钮（居中，与前进对称）
        backward_btn = ttk.Button(control_frame, text="后退", style="Normal.TButton",
                                  command=lambda: self.robot.backward(self.speed_var.get()))
        backward_btn.grid(row=3, column=1, padx=25, pady=8, ipadx=15)

        # 停止按钮（通栏居中，对称）
        stop_btn = ttk.Button(control_frame, text="停止", style="Normal.TButton",
                              command=self.robot.stop)
        stop_btn.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="we")

        # 2. 状态显示区（同步缩小，对称）
        status_frame = ttk.LabelFrame(self.root, text="机器人状态", padding=15)
        status_frame.place(x=20, y=320, width=350, height=180)
        # 状态标签居中对称
        self.status_labels = {
            "moving": ttk.Label(status_frame, text="运动状态：静止", font=("Arial", 11)),
            "direction": ttk.Label(status_frame, text="方向：停止", font=("Arial", 11)),
            "speed": ttk.Label(status_frame, text="速度：0", font=("Arial", 11)),
            "position": ttk.Label(status_frame, text="位置：(250, 250)", font=("Arial", 11))
        }
        for idx, (key, label) in enumerate(self.status_labels.items()):
            label.grid(row=idx, column=0, padx=10, pady=6, sticky="w")

        # 3. 画布显示区（恢复原尺寸，位置适配）
        self.canvas = tk.Canvas(self.root, width=400, height=550, bg="#f0f0f0")
        self.canvas.place(x=400, y=20)

        # 4. 退出按钮（对称尺寸）
        exit_btn = ttk.Button(self.root, text="退出程序", style="Normal.TButton",
                              command=self._exit_program)
        exit_btn.place(x=20, y=520, width=350, height=40)

    def _init_canvas(self):
        """初始化画布（适配对称布局）"""
        # 绘制背景网格（适中密度）
        for x in range(0, 400, 40):
            self.canvas.create_line(x, 0, x, 550, fill="#dddddd")
        for y in range(0, 550, 40):
            self.canvas.create_line(0, y, 400, y, fill="#dddddd")

        # 机器人图形尺寸适中（50x50）
        self.robot_shape = self.canvas.create_rectangle(
            self.robot.pos_x - 25, self.robot.pos_y - 25,
            self.robot.pos_x + 25, self.robot.pos_y + 25,
            fill="#0066cc", outline="#003366", width=2
        )
        # 朝向箭头尺寸适中
        self.robot_arrow = self.canvas.create_polygon(
            self.robot.pos_x, self.robot.pos_y - 30,
                              self.robot.pos_x - 8, self.robot.pos_y - 15,
                              self.robot.pos_x + 8, self.robot.pos_y - 15,
            fill="#ff3333", width=2
        )

    def _update_gui(self):
        """更新图形界面"""
        # 获取机器人状态
        status = self.robot.get_status()

        # 更新状态标签
        self.status_labels["moving"].config(text=f"运动状态：{'运动中' if status['is_moving'] else '静止'}")
        self.status_labels["direction"].config(text=f"方向：{status['direction']}")
        self.status_labels["speed"].config(text=f"速度：{status['speed']}")
        self.status_labels["position"].config(text=f"位置：{status['position']}")

        # 更新机器人位置和朝向
        self.canvas.coords(
            self.robot_shape,
            status['position'][0] - 25, status['position'][1] - 25,
            status['position'][0] + 25, status['position'][1] + 25
        )

        # 更新朝向箭头
        angle = status['angle']
        x, y = status['position']
        if angle == 0:  # 前进（上）
            arrow_coords = [x, y - 30, x - 8, y - 15, x + 8, y - 15]
        elif angle == 90:  # 右转（右）
            arrow_coords = [x + 30, y, x + 15, y - 8, x + 15, y + 8]
        elif angle == 180:  # 后退（下）
            arrow_coords = [x, y + 30, x - 8, y + 15, x + 8, y + 15]
        elif angle == 270:  # 左转（左）
            arrow_coords = [x - 30, y, x - 15, y - 8, x - 15, y + 8]
        else:  # 停止
            arrow_coords = [x, y - 30, x - 8, y - 15, x + 8, y - 15]

        self.canvas.coords(self.robot_arrow, *arrow_coords)

        # 定时刷新（50ms）
        self.root.after(50, self._update_gui)

    def _exit_program(self):
        """退出程序"""
        if messagebox.askyesno("确认退出", "确定要退出机器人控制系统吗？"):
            self.robot.stop()
            self.root.quit()
            sys.exit(0)


def main():
    """主程序"""
    # 创建GUI主窗口
    root = tk.Tk()
    # 初始化机器人GUI
    gui = RobotGUI(root)

    # 命令行交互（保留）
    def cli_interface():
        print("\n机器人控制系统启动！")
        print("可用指令（命令行）：")
        print("  forward [速度] - 前进（默认50）")
        print("  backward [速度] - 后退（默认50）")
        print("  left [速度] - 左转（默认30）")
        print("  right [速度] - 右转（默认30）")
        print("  stop - 停止")
        print("  exit - 退出程序")
        print("-" * 40)

        while True:
            try:
                command = input("\n请输入指令：").strip().lower().split()
                if not command:
                    continue

                cmd = command[0]
                speed = None
                if len(command) >= 2:
                    speed = int(command[1])

                if cmd == "forward":
                    gui.robot.forward(speed=50 if speed is None else speed)
                elif cmd == "backward":
                    gui.robot.backward(speed=50 if speed is None else speed)
                elif cmd == "left":
                    gui.robot.turn_left(speed=30 if speed is None else speed)
                elif cmd == "right":
                    gui.robot.turn_right(speed=30 if speed is None else speed)
                elif cmd == "stop":
                    gui.robot.stop()
                elif cmd == "exit":
                    print("机器人控制系统关闭")
                    gui.robot.stop()
                    root.quit()
                    sys.exit(0)
                else:
                    print("未知指令！")
            except ValueError:
                print("速度必须是数字！")
            except Exception as e:
                print(f"程序出错：{e}")

    # 启动命令行线程
    import threading
    cli_thread = threading.Thread(target=cli_interface, daemon=True)
    cli_thread.start()

    # 启动GUI主循环
    root.mainloop()


if __name__ == "__main__":
    main()