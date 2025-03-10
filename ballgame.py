from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from plyer import accelerometer
from kivy.clock import Clock

class BallGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ball_size = 50
        self.ball_x = self.center_x
        self.ball_y = self.center_y
        self.vx = 0  # X 軸速度
        self.vy = 0  # Y 軸速度
        self.friction = 0.98  # 摩擦力，讓球逐漸停下來

        with self.canvas:
            self.ball = Ellipse(pos=(self.ball_x, self.ball_y), size=(self.ball_size, self.ball_size))

        # 啟動手機加速度計
        try:
            accelerometer.enable()
        except NotImplementedError:
            print("該設備不支援加速度計")

        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 每秒更新 60 次

    def update(self, dt):
        try:
            acc = accelerometer.acceleration  # 讀取重力感應數據
            if acc is not None:
                ax, ay, _ = acc  # 取得 x 軸和 y 軸加速度
                self.vx += ax * 2  # 根據手機的傾斜角度來改變速度
                self.vy += ay * 2

            # **更新球的位置**
            self.ball_x += self.vx
            self.ball_y += self.vy

            # **邊界檢查，碰到邊界時反彈**
            if self.ball_x < 0:  # 左邊界
                self.ball_x = 0
                self.vx *= -0.8  # 速度反向，並稍微減速（模擬能量損失）
            if self.ball_x > self.width - self.ball_size:  # 右邊界
                self.ball_x = self.width - self.ball_size
                self.vx *= -0.8

            if self.ball_y < 0:  # 下邊界
                self.ball_y = 0
                self.vy *= -0.8
            if self.ball_y > self.height - self.ball_size:  # 上邊界
                self.ball_y = self.height - self.ball_size
                self.vy *= -0.8

            # **摩擦力讓球慢慢停下來**
            self.vx *= self.friction
            self.vy *= self.friction

            self.ball.pos = (self.ball_x, self.ball_y)
        except:
            pass

class BallApp(App):
    def build(self):
        return BallGame()

if __name__ == '__main__':
    BallApp().run()
