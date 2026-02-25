from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.graphics import (
    Color, Ellipse, Triangle,
    PushMatrix, PopMatrix,
    Rotate, Scale, Rectangle
)
from kivy.core.window import Window
from kivy.core.text import Label as CoreLabel
import random
import math

Window.size = (400, 700)

RESPUESTAS = [
    "SI",
    "SIN DUDA",
    "PROBABLE",
    "TODO INDICA QUE SI",
    "PREGUNTA MAS TARDE",
    "NO PUEDO DECIRLO",
    "NO",
    "MUY DUDOSO"
]


class Bola8Widget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.angle = 0
        self.velocity = 0
        self.deform = 1
        self.animating = False

        self.answer_visible = False
        self.answer_text = ""
        self.answer_alpha = 0
        self.answer_scale = 0.5

        self.bind(pos=self.update_canvas, size=self.update_canvas)
        Clock.schedule_interval(self.update_physics, 1/60)

    # -------------------
    # GEOMETRÍA
    # -------------------

    def ball_size(self):
        size = min(self.width, self.height) * 0.75
        return (size, size)

    def ball_pos(self):
        s = self.ball_size()
        return (self.center_x - s[0]/2, self.center_y - s[1]/2)

    def center_circle_size(self):
        d = self.ball_size()[0] * 0.45
        return (d, d)

    def center_circle_pos(self):
        s = self.center_circle_size()
        return (self.center_x - s[0]/2, self.center_y - s[1]/2)

    def triangle_points(self):
        size = self.ball_size()[0] * 0.35
        return [
            self.center_x, self.center_y - size/2,
            self.center_x - size/2, self.center_y + size/2,
            self.center_x + size/2, self.center_y + size/2
        ]

    # -------------------
    # DIBUJO
    # -------------------

    def update_canvas(self, *args):
        self.canvas.clear()

        with self.canvas:

            # ---------- SOMBRA ----------
            Color(0, 0, 0, 0.25)
            shadow_w = self.ball_size()[0] * 0.7
            shadow_h = self.ball_size()[0] * 0.25
            Ellipse(
                pos=(self.center_x - shadow_w/2,
                     self.center_y - self.ball_size()[1]/2 - shadow_h/3),
                size=(shadow_w, shadow_h)
            )

            # =============================
            # BOLA (GIRA)
            # =============================
            PushMatrix()
            Rotate(angle=self.angle, origin=self.center)
            Scale(self.deform, 1/self.deform, 1, origin=self.center)

            # esfera gris
            Color(0.15, 0.15, 0.15)
            Ellipse(pos=self.ball_pos(), size=self.ball_size())

            # brillo
            Color(0.7, 0.7, 0.7, 0.25)
            highlight = self.ball_size()[0] * 0.3
            Ellipse(
                pos=(self.center_x - highlight/2,
                     self.center_y + highlight/4),
                size=(highlight, highlight)
            )

            # círculo blanco
            Color(1, 1, 1)
            Ellipse(pos=self.center_circle_pos(),
                    size=self.center_circle_size())

            # número 8 (gira con la bola)
            self.draw_text(
                "8",
                self.center_x,
                self.center_y,
                self.ball_size()[0] * 0.15,
                (0, 0, 0, 1)
            )

            PopMatrix()

            # =============================
            # TRIÁNGULO (NO GIRA)
            # =============================
            if self.answer_visible:

                # sombra profundidad
                Color(0, 0, 0.3, self.answer_alpha)
                shadow_points = [p + 4 if i % 2 == 0 else p - 4
                                 for i, p in enumerate(self.triangle_points())]
                Triangle(points=shadow_points)

                # triángulo principal
                Color(0, 0.1, 0.7, self.answer_alpha)
                Triangle(points=self.triangle_points())

                # texto respuesta
                self.draw_text(
                    self.answer_text,
                    self.center_x,
                    self.center_y + 10,
                    self.ball_size()[0] * 0.07 * self.answer_scale,
                    (1, 0, 0, self.answer_alpha)
                )

    def draw_text(self, text, x, y, size, color):
        label = CoreLabel(
            text=text,
            font_size=size,
            bold=True
        )
        label.refresh()
        texture = label.texture

        Color(*color)
        Rectangle(
            texture=texture,
            pos=(x - texture.size[0]/2,
                 y - texture.size[1]/2),
            size=texture.size
        )

    # -------------------
    # FÍSICA
    # -------------------

    def update_physics(self, dt):

        if self.animating:
            self.angle += self.velocity
            self.velocity *= 0.94
            self.deform = 1 + math.sin(self.angle * 0.05) * 0.05

            if abs(self.velocity) < 0.5:
                self.animating = False
                self.show_answer()

        if self.answer_visible:
            self.answer_alpha = min(1, self.answer_alpha + dt * 2)
            self.answer_scale = min(1, self.answer_scale + dt * 1.5)

        self.update_canvas()

    # -------------------
    # ACCIONES
    # -------------------

    def shake(self):
        self.answer_visible = False
        self.answer_alpha = 0
        self.answer_scale = 0.5
        self.velocity = random.uniform(40, 60)  # más visible
        self.animating = True

    def show_answer(self):
        self.answer_text = random.choice(RESPUESTAS)
        self.answer_visible = True


class Bola8App(App):

    def build(self):
        layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10
        )

        self.input = TextInput(
            hint_text="Haz tu pregunta...",
            multiline=False,
            size_hint_y=0.1
        )

        self.button = Button(
            text="Agitar",
            size_hint_y=0.1
        )

        self.ball = Bola8Widget()

        self.button.bind(on_press=self.on_shake)

        layout.add_widget(self.input)
        layout.add_widget(self.button)
        layout.add_widget(self.ball)

        return layout

    def on_shake(self, instance):
        if not self.input.text.strip():
            return
        self.ball.shake()


if __name__ == "__main__":
    Bola8App().run()