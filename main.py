import random

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import (
    Color,
    Rectangle,
    Ellipse,
    Line,
    Triangle,
    RoundedRectangle,
    Mesh
)
from kivy.metrics import dp

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.utils import platform


# ============================================================
# APP SETTINGS
# ============================================================

if platform not in ("android", "ios"):
    Window.size = (400, 700)

Window.clearcolor = (0.20, 0.68, 0.95, 1)


# ============================================================
# COLORS
# ============================================================

BALLOON_COLORS = {
    "RED": (1.00, 0.20, 0.38, 1),
    "PURPLE": (0.58, 0.30, 1.00, 1),
    "YELLOW": (1.00, 0.72, 0.08, 1),
    "GREEN": (0.10, 0.85, 0.55, 1),
    "BLUE": (0.12, 0.55, 1.00, 1),
    "PINK": (1.00, 0.35, 0.72, 1),
}


# ============================================================
# MINI BALLOON
#
# Used only in top color counter.
# ============================================================

class MiniBalloon(Widget):

    def __init__(self, balloon_color, **kwargs):
        super().__init__(**kwargs)

        self.balloon_color = balloon_color

        self.size_hint = (None, None)
        self.size = (dp(30), dp(42))

        with self.canvas:

            # Main balloon color
            self.body_color = Color(
                *self.balloon_color
            )

            self.body = Ellipse()

            # Knot
            self.knot = Triangle()

            # String
            Color(1, 1, 1, 0.65)

            self.string = Line(
                width=0.8
            )

            # Shine
            Color(1, 1, 1, 0.45)

            self.shine = Ellipse()

        self.bind(
            pos=self.update_graphics,
            size=self.update_graphics
        )

        self.update_graphics()

    # --------------------------------------------------------

    def update_graphics(self, *args):

        self.body.pos = (
            self.x,
            self.y + dp(10)
        )

        self.body.size = (
            self.width,
            self.height - dp(12)
        )

        self.knot.points = [
            self.center_x - dp(3),
            self.y + dp(11),

            self.center_x + dp(3),
            self.y + dp(11),

            self.center_x,
            self.y + dp(5)
        ]

        self.string.points = [
            self.center_x,
            self.y + dp(5),

            self.center_x,
            self.y - dp(5)
        ]

        self.shine.pos = (
            self.x + dp(6),
            self.y + self.height - dp(18)
        )

        self.shine.size = (
            dp(6),
            dp(10)
        )

    # --------------------------------------------------------
    # Small bounce when same color is caught
    # --------------------------------------------------------

    def celebrate(self):

        Animation.cancel_all(self)

        original_width = dp(30)
        original_height = dp(42)

        animation = (
            Animation(
                width=dp(38),
                height=dp(50),
                duration=0.10
            )
            +
            Animation(
                width=original_width,
                height=original_height,
                duration=0.15
            )
        )

        animation.start(self)


# ============================================================
# GAME BALLOON
# ============================================================

class GameBalloon(Widget):

    def __init__(
        self,
        color_name,
        balloon_color,
        game_screen,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.color_name = color_name
        self.balloon_color = balloon_color
        self.game_screen = game_screen

        self.is_popped = False
        self.has_been_missed = False

        self.size_hint = (None, None)

        balloon_size = random.randint(
            int(dp(55)),
            int(dp(75))
        )

        self.size = (
            balloon_size,
            balloon_size * 1.35
        )

        # ----------------------------------------------------
        # DRAW
        # ----------------------------------------------------

        with self.canvas:

            self.body_color = Color(
                *self.balloon_color
            )

            self.body = Ellipse()

            # Knot
            self.knot = Triangle()

            # String
            Color(1, 1, 1, 0.65)

            self.string = Line(
                width=1
            )

            # Shine
            Color(1, 1, 1, 0.48)

            self.shine = Ellipse()

        self.bind(
            pos=self.update_graphics,
            size=self.update_graphics
        )

        self.update_graphics()

    # --------------------------------------------------------

    def update_graphics(self, *args):

        body_height = self.height * 0.72

        self.body.pos = (
            self.x,
            self.y + dp(27)
        )

        self.body.size = (
            self.width,
            body_height
        )

        self.knot.points = [
            self.center_x - dp(5),
            self.y + dp(29),

            self.center_x + dp(5),
            self.y + dp(29),

            self.center_x,
            self.y + dp(18)
        ]

        self.string.points = [
            self.center_x,
            self.y + dp(19),

            self.center_x - dp(4),
            self.y - dp(18)
        ]

        self.shine.pos = (
            self.x + self.width * 0.20,
            self.y + body_height
        )

        self.shine.size = (
            self.width * 0.18,
            body_height * 0.25
        )

    # --------------------------------------------------------
    # TOUCH
    # --------------------------------------------------------

    def on_touch_down(self, touch):

        if (
            not self.is_popped
            and not self.has_been_missed
            and self.collide_point(*touch.pos)
        ):

            self.pop()

            return True

        return super().on_touch_down(touch)

    # --------------------------------------------------------
    # POP
    # --------------------------------------------------------

    def pop(self):

        if self.is_popped:
            return

        self.is_popped = True

        Animation.cancel_all(self)

        # Inform game
        self.game_screen.balloon_popped(self)

        # Save center because size changes
        old_center = self.center

        animation = Animation(
            width=self.width * 1.5,
            height=self.height * 1.5,
            opacity=0,
            duration=0.14
        )

        def keep_center(*args):
            self.center = old_center

        animation.bind(
            on_progress=keep_center
        )

        animation.bind(
            on_complete=lambda *args:
            self.remove_from_screen()
        )

        animation.start(self)

    # --------------------------------------------------------

    def remove_from_screen(self):

        if self.parent:
            self.parent.remove_widget(self)



# ============================================================
# SPECIAL BALLOONS - POSTER STYLE
# ============================================================

class SpecialBalloon(Widget):
    """Shared behaviour for all special balloons."""

    def __init__(self, game_screen, **kwargs):
        super().__init__(**kwargs)
        self.game_screen = game_screen
        self.is_popped = False
        self.has_been_missed = False
        self.size_hint = (None, None)

    def on_touch_down(self, touch):
        if (
            not self.is_popped
            and not self.has_been_missed
            and self.collide_point(*touch.pos)
        ):
            self.is_popped = True
            Animation.cancel_all(self)
            self.on_special_tap()
            self.pop_animation()
            return True
        return super().on_touch_down(touch)

    def on_special_tap(self):
        pass

    def pop_animation(self):
        old_center = self.center
        anim = Animation(
            width=self.width * 1.38,
            height=self.height * 1.38,
            opacity=0,
            duration=0.16
        )

        def keep_center(*args):
            self.center = old_center

        anim.bind(on_progress=keep_center)
        anim.bind(on_complete=lambda *args: self.remove_from_screen())
        anim.start(self)

    def remove_from_screen(self):
        if self.parent:
            self.parent.remove_widget(self)


# ------------------------------------------------------------
# GOLDEN STAR BALLOON
# Poster design: bright gold 5-point star + glow + shine
# ------------------------------------------------------------

class GoldenBalloon(SpecialBalloon):

    def __init__(self, game_screen, **kwargs):
        super().__init__(game_screen, **kwargs)
        self.size = (dp(92), dp(116))

        with self.canvas:
            Color(1.0, 0.72, 0.02, 0.20)
            self.glow = Ellipse()

            Color(1.0, 0.62, 0.01, 1)
            self.star = Mesh(mode="triangle_fan")

            Color(1.0, 0.88, 0.18, 1)
            self.inner_star = Mesh(mode="triangle_fan")

            Color(1, 1, 1, 0.82)
            self.shine = Ellipse()

            Color(1, 0.90, 0.28, 0.95)
            self.spark_h = Line(width=1.4)
            self.spark_v = Line(width=1.4)

            Color(0.82, 0.40, 0.01, 1)
            self.knot = Triangle()

            Color(1, 1, 1, 0.68)
            self.string = Line(width=1)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()

    def star_vertices(self, cx, cy, outer, inner):
        import math
        pts = [(cx, cy)]
        for i in range(11):
            angle = math.radians(-90 + i * 36)
            radius = outer if i % 2 == 0 else inner
            pts.append((
                cx + math.cos(angle) * radius,
                cy + math.sin(angle) * radius
            ))

        vertices = []
        for x, y in pts:
            vertices.extend([x, y, 0, 0])

        indices = list(range(len(pts)))
        return vertices, indices

    def update_graphics(self, *args):
        cx = self.center_x
        cy = self.y + self.height * 0.62
        outer = self.width * 0.48

        self.glow.pos = (
            cx - outer - dp(8),
            cy - outer - dp(8)
        )
        self.glow.size = (
            outer * 2 + dp(16),
            outer * 2 + dp(16)
        )

        v, i = self.star_vertices(cx, cy, outer, outer * 0.47)
        self.star.vertices = v
        self.star.indices = i

        v2, i2 = self.star_vertices(
            cx,
            cy + dp(1),
            outer * 0.78,
            outer * 0.37
        )
        self.inner_star.vertices = v2
        self.inner_star.indices = i2

        self.shine.pos = (
            cx - outer * 0.35,
            cy + outer * 0.23
        )
        self.shine.size = (dp(10), dp(17))

        sx = cx + outer * 0.55
        sy = cy + outer * 0.55
        self.spark_h.points = [sx-dp(6), sy, sx+dp(6), sy]
        self.spark_v.points = [sx, sy-dp(6), sx, sy+dp(6)]

        self.knot.points = [
            cx-dp(6), self.y+dp(28),
            cx+dp(6), self.y+dp(28),
            cx, self.y+dp(17)
        ]

        self.string.points = [
            cx, self.y+dp(18),
            cx-dp(3), self.y-dp(18)
        ]

    def on_special_tap(self):
        self.game_screen.special_reward(10, "GOLD STAR +10!")


# ------------------------------------------------------------
# RAINBOW TRICK BALLOON
# Poster design: one clean balloon with rainbow curved bands.
# DON'T POP.
# ------------------------------------------------------------

class TrickBalloon(SpecialBalloon):

    def __init__(self, game_screen, **kwargs):
        super().__init__(game_screen, **kwargs)
        self.size = (dp(92), dp(122))

        with self.canvas:
            Color(0.60, 0.18, 1.00, 0.18)
            self.glow = Ellipse()

            # Base purple balloon
            Color(0.60, 0.18, 0.92, 1)
            self.body = Ellipse()

            # Rainbow arcs - gives a clean rainbow candy look
            self.arc_colors = []
            self.arcs = []
            rainbow = [
                (1.00, 0.18, 0.28, 1),
                (1.00, 0.50, 0.05, 1),
                (1.00, 0.88, 0.08, 1),
                (0.12, 0.84, 0.42, 1),
                (0.08, 0.55, 1.00, 1),
                (0.52, 0.22, 0.95, 1),
            ]

            for rgba in rainbow:
                self.arc_colors.append(Color(*rgba))
                self.arcs.append(Line(width=8, cap="round"))

            Color(1, 1, 1, 0.72)
            self.shine = Ellipse()

            Color(1, 1, 1, 0.50)
            self.outline = Line(width=1.4)

            Color(0.72, 0.12, 0.42, 1)
            self.knot = Triangle()

            Color(1, 1, 1, 0.68)
            self.string = Line(width=1)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()

    def update_graphics(self, *args):
        bx = self.x
        by = self.y + dp(29)
        bw = self.width
        bh = self.height * 0.70

        self.glow.pos = (bx-dp(7), by-dp(7))
        self.glow.size = (bw+dp(14), bh+dp(14))

        self.body.pos = (bx, by)
        self.body.size = (bw, bh)

        # Nested rainbow arcs across the balloon.
        cx = bx + bw * 0.50
        cy = by + bh * 0.42

        for idx, arc in enumerate(self.arcs):
            pad = dp(7) + idx * dp(5)
            arc.ellipse = (
                bx + pad,
                by + pad * 0.45,
                max(dp(8), bw - pad * 2),
                max(dp(8), bh - pad * 0.75),
                12,
                174
            )

        self.shine.pos = (
            bx+bw*.18,
            by+bh*.64
        )
        self.shine.size = (
            bw*.16,
            bh*.24
        )

        self.outline.ellipse = (
            bx+dp(2),
            by+dp(2),
            bw-dp(4),
            bh-dp(4)
        )

        self.knot.points = [
            self.center_x-dp(6), self.y+dp(31),
            self.center_x+dp(6), self.y+dp(31),
            self.center_x, self.y+dp(18)
        ]

        self.string.points = [
            self.center_x, self.y+dp(19),
            self.center_x+dp(4), self.y-dp(18)
        ]

    def on_special_tap(self):
        self.game_screen.special_penalty(5, "DON'T POP! -5")


# ------------------------------------------------------------
# CRYSTAL MYSTERY BALLOON
# Poster design: glassy cyan/purple balloon + large question mark.
# ------------------------------------------------------------

class MysteryBalloon(SpecialBalloon):

    def __init__(self, game_screen, **kwargs):
        super().__init__(game_screen, **kwargs)
        self.size = (dp(86), dp(114))

        with self.canvas:
            Color(0.30, 0.88, 1.00, 0.18)
            self.glow = Ellipse()

            Color(0.52, 0.30, 1.00, 0.88)
            self.body = Ellipse()

            Color(0.30, 0.92, 1.00, 0.20)
            self.glass = Ellipse()

            Color(1.00, 0.55, 0.95, 0.20)
            self.pink_glass = Ellipse()

            Color(1, 1, 1, 0.88)
            self.shine = Ellipse()

            Color(0.70, 0.95, 1.00, 0.90)
            self.outline = Line(width=1.6)

            Color(1.0, 0.72, 0.18, 1)
            self.knot = Triangle()

            Color(1, 1, 1, 0.68)
            self.string = Line(width=1)

        self.question = Label(
            text="?",
            font_size=dp(43),
            bold=True,
            color=(1, 1, 1, 1),
            outline_width=2,
            outline_color=(0.34, 0.10, 0.68, 1),
            size_hint=(None, None)
        )
        self.add_widget(self.question)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()

    def update_graphics(self, *args):
        bx = self.x
        by = self.y + dp(28)
        bw = self.width
        bh = self.height * 0.72

        self.glow.pos = (bx-dp(8), by-dp(8))
        self.glow.size = (bw+dp(16), bh+dp(16))

        self.body.pos = (bx, by)
        self.body.size = (bw, bh)

        self.glass.pos = (
            bx+bw*.08,
            by+bh*.12
        )
        self.glass.size = (
            bw*.70,
            bh*.75
        )

        self.pink_glass.pos = (
            bx+bw*.36,
            by+bh*.10
        )
        self.pink_glass.size = (
            bw*.52,
            bh*.72
        )

        self.shine.pos = (
            bx+bw*.17,
            by+bh*.65
        )
        self.shine.size = (
            bw*.17,
            bh*.24
        )

        self.outline.ellipse = (
            bx+dp(2),
            by+dp(2),
            bw-dp(4),
            bh-dp(4)
        )

        self.question.size = (bw, bh)
        self.question.pos = (bx, by)

        self.knot.points = [
            self.center_x-dp(5), self.y+dp(30),
            self.center_x+dp(5), self.y+dp(30),
            self.center_x, self.y+dp(18)
        ]

        self.string.points = [
            self.center_x, self.y+dp(19),
            self.center_x-dp(4), self.y-dp(17)
        ]

    def on_special_tap(self):
        reward = random.choice(["score", "time", "life", "jackpot"])

        if reward == "score":
            self.game_screen.special_reward(15, "MYSTERY +15!")
        elif reward == "time":
            self.game_screen.time_left += 5
            self.game_screen.level_time_left = min(
                self.game_screen.LEVEL_TIME,
                self.game_screen.level_time_left + 5
            )
            self.game_screen.show_special_message("LEVEL TIME +5!")
        elif reward == "life":
            if self.game_screen.missed > 0:
                self.game_screen.missed -= 1
                self.game_screen.missed_label.text = (
                    f"MISSED {self.game_screen.missed}"
                )
            self.game_screen.show_special_message("MISS -1!")
        else:
            self.game_screen.special_reward(25, "JACKPOT +25!")


# ------------------------------------------------------------
# BOMB BALLOON
# Poster design: black glossy bomb, angry red eyes, fuse + flame.
# DON'T POP.
# ------------------------------------------------------------

class BombBalloon(SpecialBalloon):

    def __init__(self, game_screen, **kwargs):
        super().__init__(game_screen, **kwargs)
        self.size = (dp(88), dp(116))

        with self.canvas:
            Color(0.02, 0.02, 0.08, 0.25)
            self.glow = Ellipse()

            Color(0.055, 0.06, 0.11, 1)
            self.body = Ellipse()

            Color(0.28, 0.30, 0.42, 0.55)
            self.highlight = Ellipse()

            # Angry eye backgrounds
            Color(0.22, 0.02, 0.02, 1)
            self.eye_left_bg = Ellipse()
            self.eye_right_bg = Ellipse()

            # Bright red eyes
            Color(1.0, 0.12, 0.05, 1)
            self.eye_left = Triangle()
            self.eye_right = Triangle()

            # Fuse
            Color(0.12, 0.10, 0.10, 1)
            self.fuse = Line(width=3)

            # Flame
            Color(1.0, 0.25, 0.02, 1)
            self.flame_outer = Triangle()

            Color(1.0, 0.85, 0.05, 1)
            self.flame_inner = Triangle()

            Color(0.02, 0.02, 0.04, 1)
            self.knot = Triangle()

            Color(1, 1, 1, 0.58)
            self.string = Line(width=1)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()

    def update_graphics(self, *args):
        bx = self.x
        by = self.y + dp(28)
        bw = self.width
        bh = self.height * .70

        self.glow.pos = (bx-dp(6), by-dp(6))
        self.glow.size = (bw+dp(12), bh+dp(12))

        self.body.pos = (bx, by)
        self.body.size = (bw, bh)

        self.highlight.pos = (
            bx+bw*.13,
            by+bh*.55
        )
        self.highlight.size = (
            bw*.24,
            bh*.28
        )

        ew = bw*.22
        eh = bh*.16

        self.eye_left_bg.pos = (
            bx+bw*.20,
            by+bh*.48
        )
        self.eye_left_bg.size = (ew, eh)

        self.eye_right_bg.pos = (
            bx+bw*.58,
            by+bh*.48
        )
        self.eye_right_bg.size = (ew, eh)

        self.eye_left.points = [
            bx+bw*.21, by+bh*.62,
            bx+bw*.42, by+bh*.55,
            bx+bw*.27, by+bh*.48
        ]

        self.eye_right.points = [
            bx+bw*.79, by+bh*.62,
            bx+bw*.58, by+bh*.55,
            bx+bw*.73, by+bh*.48
        ]

        # Curved-looking fuse from balloon top
        fx = bx+bw*.55
        fy = by+bh*.96

        self.fuse.points = [
            fx, fy,
            fx+dp(5), fy+dp(9),
            fx+dp(13), fy+dp(13),
            fx+dp(18), fy+dp(20)
        ]

        tipx = fx+dp(18)
        tipy = fy+dp(20)

        self.flame_outer.points = [
            tipx-dp(7), tipy-dp(2),
            tipx+dp(2), tipy+dp(13),
            tipx+dp(8), tipy-dp(2)
        ]

        self.flame_inner.points = [
            tipx-dp(3), tipy,
            tipx+dp(1), tipy+dp(8),
            tipx+dp(4), tipy
        ]

        self.knot.points = [
            self.center_x-dp(5), self.y+dp(30),
            self.center_x+dp(5), self.y+dp(30),
            self.center_x, self.y+dp(18)
        ]

        self.string.points = [
            self.center_x, self.y+dp(19),
            self.center_x-dp(3), self.y-dp(16)
        ]

    def on_special_tap(self):
        self.game_screen.special_penalty(8, "BOOM! -8")


# ------------------------------------------------------------
# HEART BALLOON
# Poster design: glossy pink heart + mini floating hearts.
# ------------------------------------------------------------

class HeartBalloon(SpecialBalloon):

    def __init__(self, game_screen, **kwargs):
        super().__init__(game_screen, **kwargs)
        self.size = (dp(90), dp(112))

        with self.canvas:
            Color(1.0, 0.15, 0.48, 0.18)
            self.glow = Ellipse()

            Color(1.0, 0.16, 0.46, 1)
            self.left = Ellipse()
            self.right = Ellipse()
            self.bottom = Triangle()

            Color(1.0, 0.42, 0.66, 0.80)
            self.inner_left = Ellipse()
            self.inner_right = Ellipse()

            Color(1, 1, 1, 0.78)
            self.shine = Ellipse()

            # Decorative tiny hearts represented as pink bubbles
            Color(1.0, 0.35, 0.62, 0.90)
            self.bubble1 = Ellipse()
            self.bubble2 = Ellipse()

            Color(0.88, 0.05, 0.32, 1)
            self.knot = Triangle()

            Color(1, 1, 1, 0.68)
            self.string = Line(width=1)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()

    def update_graphics(self, *args):
        bx = self.x
        by = self.y + dp(31)
        bw = self.width

        self.glow.pos = (
            bx-dp(5),
            by-dp(5)
        )
        self.glow.size = (
            bw+dp(10),
            bw*.84+dp(10)
        )

        self.left.pos = (
            bx+bw*.07,
            by+bw*.30
        )
        self.left.size = (
            bw*.50,
            bw*.50
        )

        self.right.pos = (
            bx+bw*.43,
            by+bw*.30
        )
        self.right.size = (
            bw*.50,
            bw*.50
        )

        self.bottom.points = [
            bx+bw*.08, by+bw*.55,
            bx+bw*.92, by+bw*.55,
            bx+bw*.50, by
        ]

        self.inner_left.pos = (
            bx+bw*.18,
            by+bw*.43
        )
        self.inner_left.size = (
            bw*.25,
            bw*.25
        )

        self.inner_right.pos = (
            bx+bw*.48,
            by+bw*.43
        )
        self.inner_right.size = (
            bw*.25,
            bw*.25
        )

        self.shine.pos = (
            bx+bw*.22,
            by+bw*.59
        )
        self.shine.size = (
            bw*.12,
            bw*.18
        )

        self.bubble1.pos = (
            bx+bw*.87,
            by+bw*.74
        )
        self.bubble1.size = (dp(9), dp(9))

        self.bubble2.pos = (
            bx+bw*.96,
            by+bw*.60
        )
        self.bubble2.size = (dp(6), dp(6))

        self.knot.points = [
            self.center_x-dp(5), self.y+dp(32),
            self.center_x+dp(5), self.y+dp(32),
            self.center_x, self.y+dp(20)
        ]

        self.string.points = [
            self.center_x, self.y+dp(20),
            self.center_x+dp(3), self.y-dp(15)
        ]

    def on_special_tap(self):
        self.game_screen.special_reward(5, "HEART +5!")
        self.game_screen.time_left += 2
        self.game_screen.level_time_left = min(
            self.game_screen.LEVEL_TIME,
            self.game_screen.level_time_left + 2
        )
        self.game_screen.show_special_message(
            "HEART +5  LEVEL TIME +2"
        )



# ============================================================
# HOME SCREEN
# ============================================================

class HomeScreen(FloatLayout):

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)

        self.controller = controller

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        with self.canvas.before:

            Color(0.20, 0.68, 0.95, 1)

            self.background = Rectangle(
                pos=self.pos,
                size=self.size
            )

            # Decorative transparent circle
            Color(1, 1, 1, 0.08)

            self.circle1 = Ellipse(
                pos=(dp(-80), dp(430)),
                size=(dp(250), dp(250))
            )

            Color(1, 0.75, 0.15, 0.10)

            self.circle2 = Ellipse(
                pos=(dp(280), dp(70)),
                size=(dp(180), dp(180))
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        self.title_label = Label(
            text="POP",
            font_size=dp(74),
            bold=True,
            color=(1, 1, 1, 1),

            size_hint=(0.8, 0.16),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.70
            }
        )

        self.add_widget(
            self.title_label
        )

        # ----------------------------------------------------

        surprise_label = Label(
            text="SURPRISE!",
            font_size=dp(38),
            bold=True,

            color=(
                1,
                0.88,
                0.10,
                1
            ),

            size_hint=(0.9, 0.10),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.59
            }
        )

        self.add_widget(
            surprise_label
        )

        # ----------------------------------------------------

        info_label = Label(
            text="POP  -  COLLECT  -  GET BONUS",
            font_size=dp(13),
            bold=True,

            color=(1, 1, 1, 0.90),

            size_hint=(0.9, 0.07),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.49
            }
        )

        self.add_widget(
            info_label
        )

        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        play_button = Button(
            text="PLAY",

            font_size=dp(25),
            bold=True,

            size_hint=(0.60, None),

            height=dp(65),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.37
            },

            background_normal="",
            background_down="",

            background_color=(
                1,
                0.20,
                0.40,
                1
            ),

            color=(1, 1, 1, 1)
        )

        play_button.bind(
            on_release=self.start_game
        )

        self.add_widget(
            play_button
        )

        # ----------------------------------------------------

        rule_label = Label(
            text="MISS 10 BALLOONS = GAME OVER",
            font_size=dp(12),
            bold=True,

            color=(
                1,
                0.90,
                0.20,
                1
            ),

            size_hint=(0.9, 0.05),

            pos_hint={
                "center_x": 0.5,
                "y": 0.10
            }
        )

        self.add_widget(
            rule_label
        )

        self.animate_title()

    # --------------------------------------------------------

    def animate_title(self):

        animation = (
            Animation(
                font_size=dp(79),
                duration=0.7
            )
            +
            Animation(
                font_size=dp(74),
                duration=0.7
            )
        )

        animation.repeat = True

        animation.start(
            self.title_label
        )

    # --------------------------------------------------------

    def start_game(self, instance):

        self.controller.show_game()

    # --------------------------------------------------------

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size



# ============================================================
# SCORE BUCKET
# ============================================================

class ScoreBucket(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(58), dp(48))

        with self.canvas:
            Color(1.00, 0.22, 0.38, 1)
            self.b1 = Ellipse()
            Color(1.00, 0.76, 0.08, 1)
            self.b2 = Ellipse()
            Color(0.16, 0.84, 0.54, 1)
            self.b3 = Ellipse()
            Color(0.18, 0.56, 1.00, 1)
            self.b4 = Ellipse()
            Color(0.67, 0.28, 1.00, 1)
            self.b5 = Ellipse()

            Color(1, 1, 1, 0.55)
            self.shine1 = Ellipse()
            self.shine2 = Ellipse()

            Color(0.98, 0.55, 0.10, 1)
            self.bucket = Mesh(mode="triangle_fan")

            Color(1.00, 0.76, 0.20, 1)
            self.rim = RoundedRectangle(radius=[dp(4)])

            Color(1, 1, 1, 0.25)
            self.bucket_shine = RoundedRectangle(radius=[dp(3)])

            Color(1, 0.90, 0.55, 0.85)
            self.handle = Line(width=1.4)

        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()

    def update_graphics(self, *args):
        x, y, w, h = self.x, self.y, self.width, self.height

        balloons = [
            (self.b1, .07, .46, .23, .32),
            (self.b2, .23, .58, .24, .34),
            (self.b3, .40, .50, .23, .33),
            (self.b4, .57, .59, .24, .34),
            (self.b5, .72, .45, .22, .31),
        ]
        for balloon, px, py, pw, ph in balloons:
            balloon.pos = (x+w*px, y+h*py)
            balloon.size = (w*pw, h*ph)

        self.shine1.pos = (x+w*.28, y+h*.78)
        self.shine1.size = (dp(3), dp(5))
        self.shine2.pos = (x+w*.62, y+h*.79)
        self.shine2.size = (dp(3), dp(5))

        top_y = y+h*.47
        bottom_y = y+h*.05
        self.bucket.vertices = [
            x+w*.12, top_y, 0, 0,
            x+w*.88, top_y, 0, 0,
            x+w*.76, bottom_y, 0, 0,
            x+w*.24, bottom_y, 0, 0,
        ]
        self.bucket.indices = [0, 1, 2, 3]

        self.rim.pos = (x+w*.08, top_y-dp(3))
        self.rim.size = (w*.84, dp(8))
        self.bucket_shine.pos = (x+w*.28, y+h*.15)
        self.bucket_shine.size = (w*.10, h*.24)
        self.handle.ellipse = (
            x+w*.20, y+h*.14, w*.60, h*.50, 195, 345
        )

    def celebrate(self):
        Animation.cancel_all(self)
        anim = (
            Animation(width=dp(65), height=dp(54), duration=.08)
            +
            Animation(width=dp(58), height=dp(48), duration=.12)
        )
        anim.start(self)


# ============================================================
# GAME SCREEN
# ============================================================

class GameScreen(FloatLayout):

    MAX_MISSED = 10

    # 10 levels x 60 seconds = 10 minute full game
    TOTAL_LEVELS = 10
    LEVEL_TIME = 60
    GAME_TIME = TOTAL_LEVELS * LEVEL_TIME

    # First real bonus target
    BONUS_TARGET = 100

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)

        self.controller = controller

        # ----------------------------------------------------
        # GAME DATA
        # ----------------------------------------------------

        self.score = 0
        self.missed = 0
        self.time_left = self.GAME_TIME
        self.current_level = 1
        self.level_time_left = self.LEVEL_TIME

        self.game_running = True

        # Combo / special-balloon system
        self.combo = 0
        self.next_special_in = random.uniform(8.0, 12.0)
        self.special_elapsed = 0.0

        # Count each color
        self.color_counts = {
            name: 0
            for name in BALLOON_COLORS
        }

        # Target for each color
        self.color_targets = {
            name: self.BONUS_TARGET
            for name in BALLOON_COLORS
        }

        # Mini balloon widgets
        self.mini_balloons = {}

        # Mini count labels
        self.count_labels = {}

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        with self.canvas.before:

            Color(
                0.20,
                0.68,
                0.95,
                1
            )

            self.background = Rectangle(
                pos=self.pos,
                size=self.size
            )

            # Sunny glow
            Color(1.0, 0.92, 0.35, 0.24)
            self.sun_glow = Ellipse()

            Color(1.0, 0.90, 0.25, 0.90)
            self.sun = Ellipse()

            # Clouds
            Color(1, 1, 1, 0.70)
            self.cloud1a = Ellipse()
            self.cloud1b = Ellipse()
            self.cloud1c = Ellipse()
            self.cloud2a = Ellipse()
            self.cloud2b = Ellipse()

            # Mountains
            Color(0.18, 0.48, 0.70, 0.75)
            self.mountain1 = Triangle()
            self.mountain2 = Triangle()
            self.mountain3 = Triangle()

            Color(0.35, 0.67, 0.50, 0.75)
            self.hill1 = Ellipse()
            self.hill2 = Ellipse()

            # Lake / ground
            Color(0.18, 0.66, 0.82, 0.38)
            self.lake = Rectangle()

            Color(0.16, 0.55, 0.26, 0.78)
            self.grass = Rectangle()

            # Soft background decorations
            Color(1, 1, 1, 0.05)
            self.bg_circle1 = Ellipse()

            Color(1, 0.80, 0.20, 0.06)
            self.bg_circle2 = Ellipse()

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # ----------------------------------------------------
        # TOP BAR BACKGROUND
        # ----------------------------------------------------

        self.top_panel = Widget(
            size_hint=(0.94, None),
            height=dp(65),

            pos_hint={
                "center_x": 0.5,
                "top": 0.98
            }
        )

        with self.top_panel.canvas:

            Color(
                0.02,
                0.20,
                0.48,
                0.88
            )

            self.top_panel_bg = RoundedRectangle(
                pos=self.top_panel.pos,
                size=self.top_panel.size,
                radius=[dp(18)]
            )

        self.top_panel.bind(
            pos=self.update_top_panel,
            size=self.update_top_panel
        )

        self.add_widget(
            self.top_panel
        )

        # ----------------------------------------------------
        # SCORE BUCKET + CURRENT LEVEL + MISSED
        # ----------------------------------------------------

        self.score_bucket = ScoreBucket(
            pos_hint={"x": 0.035, "top": 0.985}
        )
        self.add_widget(self.score_bucket)

        self.score_label = Label(
            text="0",
            font_size=dp(21),
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(0.17, 0.08),
            pos_hint={"x": 0.17, "top": 0.975}
        )
        self.add_widget(self.score_label)

        # No visible timer. Only current level is shown.
        self.level_label = Label(
            text="LEVEL 1",
            font_size=dp(19),
            bold=True,
            color=(1, 0.92, 0.18, 1),
            size_hint=(0.34, 0.08),
            pos_hint={"center_x": 0.52, "top": 0.975}
        )
        self.add_widget(self.level_label)

        self.missed_label = Label(
            text="MISSED 0",
            font_size=dp(15),
            bold=True,
            color=(1, 0.90, 0.20, 1),
            size_hint=(0.29, 0.08),
            pos_hint={"right": 0.98, "top": 0.975}
        )
        self.add_widget(self.missed_label)

        # ----------------------------------------------------
        # COLOR COUNTER AREA
        # ----------------------------------------------------

        self.create_color_counter()

        # ----------------------------------------------------
        # BOTTOM FUN BANNER
        # ----------------------------------------------------

        self.fun_banner = Label(
            text="POP SMART  •  SCORE HIGH!",
            font_size=dp(13),
            bold=True,
            color=(1, 0.92, 0.22, 1),
            size_hint=(0.82, None),
            height=dp(34),
            pos_hint={
                "center_x": 0.5,
                "y": 0.012
            }
        )

        with self.fun_banner.canvas.before:
            Color(0.35, 0.16, 0.04, 0.82)
            self.fun_banner_bg = RoundedRectangle(
                pos=self.fun_banner.pos,
                size=self.fun_banner.size,
                radius=[dp(12)]
            )

        self.fun_banner.bind(
            pos=lambda *args: setattr(
                self.fun_banner_bg, "pos", self.fun_banner.pos
            ),
            size=lambda *args: setattr(
                self.fun_banner_bg, "size", self.fun_banner.size
            )
        )

        self.add_widget(self.fun_banner)

        # ----------------------------------------------------
        # MESSAGE
        # ----------------------------------------------------

        self.message_label = Label(
            text="",

            font_size=dp(30),
            bold=True,

            halign="center",

            color=(1, 1, 1, 1),

            opacity=0,

            size_hint=(0.9, 0.20),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.55
            }
        )

        self.add_widget(
            self.message_label
        )

        # ----------------------------------------------------
        # START SPAWNING
        # ----------------------------------------------------

        # Level 1 starts relaxed. Each level spawns balloons faster.
        self.spawn_interval = 0.90
        self.spawn_event = Clock.schedule_interval(
            self.spawn_balloon,
            self.spawn_interval
        )

        # ----------------------------------------------------
        # TIMER
        # ----------------------------------------------------

        self.timer_event = Clock.schedule_interval(
            self.update_timer,
            1
        )

        # Special balloon controller.
        # Checks once per second and releases one surprise balloon
        # roughly every 8-14 seconds.
        self.special_event = Clock.schedule_interval(
            self.update_specials,
            1
        )

    # ========================================================
    # TOP PANEL
    # ========================================================

    def update_top_panel(self, *args):

        self.top_panel_bg.pos = (
            self.top_panel.pos
        )

        self.top_panel_bg.size = (
            self.top_panel.size
        )

    # ========================================================
    # COLOR COUNTER
    # ========================================================

    def create_color_counter(self):

        color_names = list(
            BALLOON_COLORS.keys()
        )

        # Six equally spaced positions
        x_positions = [
            0.05,
            0.21,
            0.37,
            0.53,
            0.69,
            0.85
        ]

        for index, color_name in enumerate(color_names):

            # ------------------------------------------------
            # MINI BALLOON
            # ------------------------------------------------

            mini = MiniBalloon(
                balloon_color=
                BALLOON_COLORS[color_name]
            )

            mini.pos_hint = {
                "center_x":
                    x_positions[index] + 0.05,

                "top":
                    0.835
            }

            self.mini_balloons[
                color_name
            ] = mini

            self.add_widget(
                mini
            )

            # ------------------------------------------------
            # COUNT
            # ------------------------------------------------

            count = Label(
                text="0",

                font_size=dp(15),
                bold=True,

                color=(1, 1, 1, 1),

                size_hint=(
                    0.10,
                    0.05
                ),

                pos_hint={
                    "center_x":
                        x_positions[index] + 0.05,

                    "top":
                        0.775
                }
            )

            self.count_labels[
                color_name
            ] = count

            self.add_widget(
                count
            )

    # ========================================================
    # SPAWN BALLOON
    # ========================================================

    def spawn_balloon(self, dt):

        if not self.game_running:
            return

        # ----------------------------------------------------
        # RANDOM COLOR
        # ----------------------------------------------------

        color_name = random.choice(
            list(
                BALLOON_COLORS.keys()
            )
        )

        balloon_color = (
            BALLOON_COLORS[color_name]
        )

        # ----------------------------------------------------
        # CREATE
        # ----------------------------------------------------

        balloon = GameBalloon(
            color_name=color_name,
            balloon_color=balloon_color,
            game_screen=self
        )

        # ----------------------------------------------------
        # RANDOM X
        # ----------------------------------------------------

        maximum_x = (
            self.width
            - balloon.width
            - dp(10)
        )

        balloon.x = random.uniform(
            dp(10),
            max(
                dp(10),
                maximum_x
            )
        )

        balloon.y = (
            -balloon.height
        )

        # Add behind UI
        self.add_widget(
            balloon,
            index=1
        )

        # ----------------------------------------------------
        # SPEED
        #
        # Game slowly becomes faster.
        # ----------------------------------------------------

        seconds_played = (
            self.GAME_TIME
            - self.time_left
        )

        # LEVEL DIFFICULTY:
        # Level 1 = slow/easy, Level 10 = very fast.
        # Animation duration gets smaller as level increases.
        level_durations = {
            1: (5.2, 6.0),
            2: (4.9, 5.7),
            3: (4.6, 5.4),
            4: (4.3, 5.1),
            5: (4.0, 4.8),
            6: (3.7, 4.5),
            7: (3.4, 4.2),
            8: (3.1, 3.9),
            9: (2.8, 3.6),
            10: (2.5, 3.3),
        }

        min_duration, max_duration = level_durations[
            self.current_level
        ]

        # Small speed increase during each individual level too.
        level_progress = (
            self.LEVEL_TIME - self.level_time_left
        ) / self.LEVEL_TIME

        duration = max(
            2.2,
            random.uniform(
                min_duration,
                max_duration
            ) - (level_progress * 0.20)
        )

        # ----------------------------------------------------
        # MOVE UP
        # ----------------------------------------------------

        animation = Animation(
            y=self.height + dp(80),
            duration=duration
        )

        animation.bind(
            on_complete=
            lambda *args:
            self.balloon_missed(balloon)
        )

        animation.start(
            balloon
        )

    # ========================================================
    # POPPED
    # ========================================================

    def balloon_popped(self, balloon):

        if not self.game_running:
            return

        color_name = (
            balloon.color_name
        )

        # ----------------------------------------------------
        # SCORE +1
        # ----------------------------------------------------

        # Combo grows while the player keeps popping correctly.
        self.combo += 1

        multiplier = 1
        if self.combo >= 10:
            multiplier = 3
        elif self.combo >= 5:
            multiplier = 2

        self.score += multiplier

        self.score_label.text = str(self.score)
        self.score_bucket.celebrate()

        if self.combo == 5:
            self.show_special_message("COMBO x2!")
        elif self.combo == 10:
            self.show_special_message("COMBO x3!")

        # ----------------------------------------------------
        # COLOR +1
        # ----------------------------------------------------

        self.color_counts[
            color_name
        ] += 1

        current_count = (
            self.color_counts[
                color_name
            ]
        )

        # Update small number
        self.count_labels[
            color_name
        ].text = str(
            current_count
        )

        # Animate small balloon
        self.mini_balloons[
            color_name
        ].celebrate()

        # ----------------------------------------------------
        # BONUS CHECK
        # ----------------------------------------------------

        target = (
            self.color_targets[
                color_name
            ]
        )

        if current_count >= target:

            # +50 bonus
            self.score += 50

            self.score_label.text = str(self.score)

            self.show_bonus(
                color_name,
                target
            )

            # Next:
            # 100 -> 200
            # 200 -> 300
            self.color_targets[
                color_name
            ] += 100

        else:

            self.show_pop_message()

    # ========================================================
    # BALLOON MISSED
    # ========================================================

    def balloon_missed(self, balloon):

        if (
            not self.game_running
            or balloon.is_popped
            or balloon.has_been_missed
        ):
            return

        balloon.has_been_missed = True

        # Remove balloon
        if balloon.parent:

            balloon.parent.remove_widget(
                balloon
            )

        # ----------------------------------------------------
        # MISSED +1
        # ----------------------------------------------------

        self.missed += 1
        self.combo = 0

        self.missed_label.text = (
            f"MISSED {self.missed}"
        )

        # ----------------------------------------------------
        # SMALL MISSED ANIMATION
        # ----------------------------------------------------

        Animation.cancel_all(
            self.missed_label
        )

        self.missed_label.color = (
            1,
            0.25,
            0.25,
            1
        )

        animation = (
            Animation(
                font_size=dp(21),
                duration=0.10
            )
            +
            Animation(
                font_size=dp(16),
                duration=0.15
            )
        )

        animation.bind(
            on_complete=
            lambda *args:
            self.reset_missed_color()
        )

        animation.start(
            self.missed_label
        )

        # ----------------------------------------------------
        # 10 MISSED = GAME OVER
        # ----------------------------------------------------

        if self.missed >= self.MAX_MISSED:

            self.end_game(
                reason="TOO MANY MISSES!"
            )

    # ========================================================
    # RESET MISSED COLOR
    # ========================================================

    def reset_missed_color(self):

        if self.game_running:

            self.missed_label.color = (
                1,
                0.90,
                0.20,
                1
            )

    # ========================================================
    # NORMAL POP MESSAGE
    # ========================================================

    def show_pop_message(self):

        messages = [
            "POP!",
            "NICE!",
            "WOW!",
            "GREAT!",
            "+1"
        ]

        Animation.cancel_all(
            self.message_label
        )

        self.message_label.text = (
            random.choice(messages)
        )

        self.message_label.color = (
            1,
            1,
            1,
            1
        )

        self.message_label.opacity = 1

        self.message_label.font_size = (
            dp(22)
        )

        animation = Animation(
            font_size=dp(36),
            opacity=0,
            duration=0.40
        )

        animation.start(
            self.message_label
        )

    # ========================================================
    # BONUS
    # ========================================================

    def show_bonus(
        self,
        color_name,
        target
    ):

        Animation.cancel_all(
            self.message_label
        )

        self.message_label.text = (
            f"{color_name} {target}!\n"
            f"BONUS +50"
        )

        self.message_label.color = (
            1,
            0.88,
            0.10,
            1
        )

        self.message_label.opacity = 1

        self.message_label.font_size = (
            dp(25)
        )

        animation = (
            Animation(
                font_size=dp(40),
                duration=0.20
            )
            +
            Animation(
                font_size=dp(30),
                duration=0.20
            )
            +
            Animation(
                opacity=0,
                duration=1.30
            )
        )

        animation.start(
            self.message_label
        )

        # Bigger celebration on mini balloon
        mini = (
            self.mini_balloons[
                color_name
            ]
        )

        Animation.cancel_all(mini)

        animation2 = (
            Animation(
                width=dp(48),
                height=dp(62),
                duration=0.18
            )
            +
            Animation(
                width=dp(30),
                height=dp(42),
                duration=0.25
            )
        )

        animation2.start(mini)


    # ========================================================
    # SPECIAL BALLOONS
    # ========================================================

    def update_specials(self, dt):
        if not self.game_running:
            return

        self.special_elapsed += dt

        if self.special_elapsed >= self.next_special_in:
            self.special_elapsed = 0
            min_gap = max(5.0, 9.0 - (self.current_level - 1) * 0.35)
            max_gap = max(8.0, 14.0 - (self.current_level - 1) * 0.45)
            self.next_special_in = random.uniform(min_gap, max_gap)
            self.spawn_special_balloon()

    def spawn_special_balloon(self):
        if not self.game_running:
            return

        # Weighted choices:
        # golden/mystery are rewarding,
        # trick/bomb test restraint,
        # heart is a rarer recovery balloon.
        # Special-balloon difficulty changes with the level.
        # Early levels: more rewards.
        # Later levels: more Trick and Bomb balloons.
        difficulty_weights = {
            1:  [35, 12, 28, 20, 5],
            2:  [33, 14, 27, 19, 7],
            3:  [31, 16, 26, 17, 10],
            4:  [29, 18, 25, 15, 13],
            5:  [27, 20, 24, 14, 15],
            6:  [25, 22, 23, 12, 18],
            7:  [23, 24, 22, 10, 21],
            8:  [21, 26, 21, 9, 23],
            9:  [19, 28, 20, 8, 25],
            10: [17, 30, 18, 7, 28],
        }

        balloon_class = random.choices(
            [
                GoldenBalloon,
                TrickBalloon,
                MysteryBalloon,
                HeartBalloon,
                BombBalloon
            ],
            weights=difficulty_weights[self.current_level],
            k=1
        )[0]

        balloon = balloon_class(self)

        maximum_x = self.width - balloon.width - dp(12)
        balloon.x = random.uniform(
            dp(12),
            max(dp(12), maximum_x)
        )
        balloon.y = -balloon.height

        # Same bottom-to-top motion family as normal balloons.
        self.add_widget(balloon, index=1)

        # Special balloons also become faster level by level.
        special_durations = {
            1: (5.3, 6.2),
            2: (5.0, 5.9),
            3: (4.7, 5.6),
            4: (4.4, 5.3),
            5: (4.1, 5.0),
            6: (3.8, 4.7),
            7: (3.5, 4.4),
            8: (3.2, 4.1),
            9: (2.9, 3.8),
            10: (2.6, 3.5),
        }

        special_min, special_max = special_durations[
            self.current_level
        ]

        duration = random.uniform(
            special_min,
            special_max
        )

        # Slight side movement makes special balloons feel alive,
        # while still travelling upward like the normal balloons.
        target_x = balloon.x + random.uniform(-dp(45), dp(45))
        target_x = max(
            dp(8),
            min(target_x, self.width - balloon.width - dp(8))
        )

        anim = Animation(
            x=target_x,
            y=self.height + dp(100),
            duration=duration
        )

        anim.bind(
            on_complete=lambda *args:
            self.special_balloon_escaped(balloon)
        )

        anim.start(balloon)

    def special_balloon_escaped(self, balloon):
        if (
            not self.game_running
            or balloon.is_popped
            or balloon.has_been_missed
        ):
            return

        balloon.has_been_missed = True

        # Danger balloons reward the player for NOT touching them.
        if isinstance(balloon, (TrickBalloon, BombBalloon)):
            self.special_reward(5, "SAFE! +5")

        if balloon.parent:
            balloon.parent.remove_widget(balloon)

    def special_reward(self, points, message):
        if not self.game_running:
            return

        self.score += points
        self.score_label.text = str(self.score)
        self.score_bucket.celebrate()
        self.show_special_message(message)

    def special_penalty(self, points, message):
        if not self.game_running:
            return

        self.score = max(0, self.score - points)
        self.combo = 0
        self.score_label.text = str(self.score)
        self.show_special_message(message, danger=True)

    def show_special_message(self, text, danger=False):
        Animation.cancel_all(self.message_label)

        self.message_label.text = text
        self.message_label.opacity = 1
        self.message_label.font_size = dp(25)

        if danger:
            self.message_label.color = (1, 0.28, 0.28, 1)
        else:
            self.message_label.color = (1, 0.90, 0.18, 1)

        anim = (
            Animation(
                font_size=dp(38),
                duration=0.16
            )
            +
            Animation(
                font_size=dp(29),
                duration=0.16
            )
            +
            Animation(
                opacity=0,
                duration=0.85
            )
        )
        anim.start(self.message_label)

    # ========================================================
    # TIMER
    # ========================================================

    def update_timer(self, dt):

        if not self.game_running:
            return

        self.time_left -= 1
        self.level_time_left -= 1

        # Total game clock: 10:00 -> 00:00
        minutes = max(0, self.time_left) // 60
        seconds = max(0, self.time_left) % 60


        # Final 10 seconds of the complete 10-minute game
# Complete current 60-second level
        if self.level_time_left <= 0 and self.time_left > 0:
            if self.current_level < self.TOTAL_LEVELS:
                completed_level = self.current_level
                self.current_level += 1
                self.level_time_left = self.LEVEL_TIME

                # Level-clear reward
                level_bonus = completed_level * 5
                self.score += level_bonus
                self.score_label.text = str(self.score)

                self.level_label.text = (
                    f"LEVEL {self.current_level}"
                )

                # Increase speed + spawn rate for the new level.
                self.update_level_difficulty()

                self.show_level_message(
                    completed_level,
                    level_bonus
                )

        # Full 10 minutes completed
        if self.time_left <= 0:
            self.end_game(
                reason="ALL 10 LEVELS COMPLETE!"
            )

    def update_level_difficulty(self):
        """Restart normal balloon scheduler with this level's spawn rate."""

        spawn_intervals = {
            1: 0.90,
            2: 0.84,
            3: 0.78,
            4: 0.72,
            5: 0.66,
            6: 0.60,
            7: 0.55,
            8: 0.50,
            9: 0.45,
            10: 0.40,
        }

        new_interval = spawn_intervals[
            self.current_level
        ]

        if abs(new_interval - self.spawn_interval) > 0.001:
            self.spawn_interval = new_interval

            if hasattr(self, "spawn_event"):
                self.spawn_event.cancel()

            self.spawn_event = Clock.schedule_interval(
                self.spawn_balloon,
                self.spawn_interval
            )

    def show_level_message(self, completed_level, bonus):

        Animation.cancel_all(
            self.message_label
        )

        self.message_label.text = (
            f"LEVEL {completed_level} COMPLETE!\n"
            f"BONUS +{bonus}\n"
            f"LEVEL {self.current_level}"
        )

        self.message_label.color = (
            1,
            0.90,
            0.12,
            1
        )

        self.message_label.opacity = 1
        self.message_label.font_size = dp(23)

        animation = (
            Animation(
                font_size=dp(36),
                duration=0.20
            )
            +
            Animation(
                font_size=dp(27),
                duration=0.20
            )
            +
            Animation(
                opacity=0,
                duration=1.35
            )
        )

        animation.start(
            self.message_label
        )

    # ========================================================
    # END GAME
    # ========================================================

    def end_game(self, reason):

        if not self.game_running:
            return

        self.game_running = False

        # Stop scheduler
        self.spawn_event.cancel()
        self.timer_event.cancel()
        self.special_event.cancel()

        # Stop/remove balloons
        for child in self.children[:]:

            if isinstance(
                child,
                (GameBalloon, SpecialBalloon)
            ):

                Animation.cancel_all(
                    child
                )

                if child.parent:
                    self.remove_widget(
                        child
                    )

        self.show_game_over(
            reason
        )

    # ========================================================
    # GAME OVER
    # ========================================================

    def show_game_over(self, reason):

        overlay = FloatLayout()

        # ----------------------------------------------------
        # DARK OVERLAY
        # ----------------------------------------------------

        with overlay.canvas.before:

            Color(
                0.04,
                0.08,
                0.20,
                0.94
            )

            overlay.background = Rectangle(
                pos=overlay.pos,
                size=overlay.size
            )

        def update_overlay(*args):

            overlay.background.pos = (
                overlay.pos
            )

            overlay.background.size = (
                overlay.size
            )

        overlay.bind(
            pos=update_overlay,
            size=update_overlay
        )

        # ----------------------------------------------------
        # GAME OVER
        # ----------------------------------------------------

        game_over = Label(
            text="GAME OVER",

            font_size=dp(42),
            bold=True,

            color=(
                1,
                0.85,
                0.10,
                1
            ),

            size_hint=(0.9, 0.12),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.76
            }
        )

        overlay.add_widget(
            game_over
        )

        # ----------------------------------------------------
        # REASON
        # ----------------------------------------------------

        reason_label = Label(
            text=reason,

            font_size=dp(18),
            bold=True,

            color=(
                1,
                0.45,
                0.45,
                1
            ),

            size_hint=(0.9, 0.08),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.67
            }
        )

        overlay.add_widget(
            reason_label
        )

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        final_score = Label(
            text=(
                f"SCORE\n"
                f"{self.score}"
            ),

            font_size=dp(31),
            bold=True,

            halign="center",

            color=(1, 1, 1, 1),

            size_hint=(0.8, 0.16),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.55
            }
        )

        overlay.add_widget(
            final_score
        )

        # ----------------------------------------------------
        # MISSED
        # ----------------------------------------------------

        missed_result = Label(
            text=f"MISSED {self.missed}",

            font_size=dp(17),
            bold=True,

            color=(
                1,
                0.80,
                0.20,
                1
            ),

            size_hint=(0.8, 0.06),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.43
            }
        )

        overlay.add_widget(
            missed_result
        )

        # ----------------------------------------------------
        # PLAY AGAIN
        # ----------------------------------------------------

        play_again = Button(
            text="PLAY AGAIN",

            font_size=dp(20),
            bold=True,

            size_hint=(0.62, None),

            height=dp(60),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.30
            },

            background_normal="",
            background_down="",

            background_color=(
                1,
                0.20,
                0.40,
                1
            ),

            color=(1, 1, 1, 1)
        )

        play_again.bind(
            on_release=
            lambda instance:
            self.controller.show_game()
        )

        overlay.add_widget(
            play_again
        )

        # ----------------------------------------------------
        # HOME
        # ----------------------------------------------------

        home = Button(
            text="HOME",

            font_size=dp(17),
            bold=True,

            size_hint=(0.45, None),

            height=dp(50),

            pos_hint={
                "center_x": 0.5,
                "center_y": 0.19
            },

            background_normal="",
            background_down="",

            background_color=(
                0.25,
                0.45,
                0.75,
                1
            ),

            color=(1, 1, 1, 1)
        )

        home.bind(
            on_release=
            lambda instance:
            self.controller.show_home()
        )

        overlay.add_widget(
            home
        )

        self.add_widget(
            overlay
        )

    # ========================================================
    # BACKGROUND UPDATE
    # ========================================================

    def update_background(self, *args):

        self.background.pos = self.pos
        self.background.size = self.size

        # Illustrated game-world background
        if hasattr(self, "sun_glow"):
            self.sun_glow.pos = (self.x - dp(45), self.top - dp(210))
            self.sun_glow.size = (dp(180), dp(180))
            self.sun.pos = (self.x + dp(8), self.top - dp(155))
            self.sun.size = (dp(72), dp(72))

            self.cloud1a.pos = (self.x + self.width * .18, self.top - dp(175))
            self.cloud1a.size = (dp(78), dp(34))
            self.cloud1b.pos = (self.x + self.width * .27, self.top - dp(187))
            self.cloud1b.size = (dp(92), dp(43))
            self.cloud1c.pos = (self.x + self.width * .38, self.top - dp(174))
            self.cloud1c.size = (dp(65), dp(31))

            self.cloud2a.pos = (self.x + self.width * .67, self.top - dp(230))
            self.cloud2a.size = (dp(86), dp(38))
            self.cloud2b.pos = (self.x + self.width * .78, self.top - dp(220))
            self.cloud2b.size = (dp(70), dp(32))

            ground_y = self.y + self.height * .10
            mountain_y = self.y + self.height * .16

            self.mountain1.points = [
                self.x-dp(40), mountain_y,
                self.x+self.width*.25, self.y+self.height*.48,
                self.x+self.width*.52, mountain_y
            ]
            self.mountain2.points = [
                self.x+self.width*.18, mountain_y,
                self.x+self.width*.52, self.y+self.height*.42,
                self.x+self.width*.78, mountain_y
            ]
            self.mountain3.points = [
                self.x+self.width*.55, mountain_y,
                self.x+self.width*.84, self.y+self.height*.46,
                self.right+dp(45), mountain_y
            ]

            self.hill1.pos = (self.x-dp(80), self.y+self.height*.10)
            self.hill1.size = (self.width*.75, self.height*.23)
            self.hill2.pos = (self.x+self.width*.40, self.y+self.height*.09)
            self.hill2.size = (self.width*.75, self.height*.24)

            self.lake.pos = (self.x, self.y+self.height*.07)
            self.lake.size = (self.width, self.height*.14)
            self.grass.pos = (self.x, self.y)
            self.grass.size = (self.width, self.height*.075)

            self.bg_circle1.pos = (self.x-dp(100), self.y+dp(250))
            self.bg_circle1.size = (dp(300), dp(300))
            self.bg_circle2.pos = (self.right-dp(140), self.y+dp(50))
            self.bg_circle2.size = (dp(200), dp(200))


# ============================================================
# ROOT / SCREEN CONTROLLER
# ============================================================

class GameRoot(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.show_home()

    # --------------------------------------------------------

    def stop_current_game(self):

        for child in self.children:

            if isinstance(
                child,
                GameScreen
            ):

                child.game_running = False

                if hasattr(
                    child,
                    "spawn_event"
                ):
                    child.spawn_event.cancel()

                if hasattr(
                    child,
                    "timer_event"
                ):
                    child.timer_event.cancel()

                if hasattr(
                    child,
                    "special_event"
                ):
                    child.special_event.cancel()

    # --------------------------------------------------------

    def show_home(self):

        self.stop_current_game()

        self.clear_widgets()

        home = HomeScreen(
            controller=self
        )

        self.add_widget(
            home
        )

    # --------------------------------------------------------

    def show_game(self):

        self.stop_current_game()

        self.clear_widgets()

        game = GameScreen(
            controller=self
        )

        self.add_widget(
            game
        )


# ============================================================
# APP
# ============================================================

class PopSurpriseApp(App):

    def build(self):

        self.title = "Pop Surprise"

        return GameRoot()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    PopSurpriseApp().run()