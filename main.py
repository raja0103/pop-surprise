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
    RoundedRectangle
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
# GAME SCREEN
# ============================================================

class GameScreen(FloatLayout):

    MAX_MISSED = 10
    GAME_TIME = 60

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

        self.game_running = True

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

            # Soft background decorations
            Color(1, 1, 1, 0.06)

            self.bg_circle1 = Ellipse(
                pos=(dp(-100), dp(250)),
                size=(dp(300), dp(300))
            )

            Color(1, 0.80, 0.20, 0.07)

            self.bg_circle2 = Ellipse(
                pos=(dp(260), dp(50)),
                size=(dp(200), dp(200))
            )

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
                0.08,
                0.25,
                0.50,
                0.25
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
        # SCORE
        # ----------------------------------------------------

        self.score_label = Label(
            text="SCORE 0",

            font_size=dp(16),
            bold=True,

            color=(1, 1, 1, 1),

            size_hint=(0.32, 0.08),

            pos_hint={
                "x": 0.02,
                "top": 0.975
            }
        )

        self.add_widget(
            self.score_label
        )

        # ----------------------------------------------------
        # MISSED
        # ----------------------------------------------------

        self.missed_label = Label(
            text="MISSED 0",

            font_size=dp(16),
            bold=True,

            color=(
                1,
                0.90,
                0.20,
                1
            ),

            size_hint=(0.34, 0.08),

            pos_hint={
                "center_x": 0.5,
                "top": 0.975
            }
        )

        self.add_widget(
            self.missed_label
        )

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        self.timer_label = Label(
            text=f"TIME {self.GAME_TIME}",

            font_size=dp(16),
            bold=True,

            color=(1, 1, 1, 1),

            size_hint=(0.30, 0.08),

            pos_hint={
                "right": 0.98,
                "top": 0.975
            }
        )

        self.add_widget(
            self.timer_label
        )

        # ----------------------------------------------------
        # COLOR COUNTER AREA
        # ----------------------------------------------------

        self.create_color_counter()

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

        self.spawn_event = Clock.schedule_interval(
            self.spawn_balloon,
            0.70
        )

        # ----------------------------------------------------
        # TIMER
        # ----------------------------------------------------

        self.timer_event = Clock.schedule_interval(
            self.update_timer,
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
                    0.855
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
                        0.795
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

        speed_reduction = (
            seconds_played * 0.025
        )

        duration = max(
            2.8,
            random.uniform(
                4.3,
                5.3
            )
            - speed_reduction
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

        self.score += 1

        self.score_label.text = (
            f"SCORE {self.score}"
        )

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

            self.score_label.text = (
                f"SCORE {self.score}"
            )

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
    # TIMER
    # ========================================================

    def update_timer(self, dt):

        if not self.game_running:
            return

        self.time_left -= 1

        self.timer_label.text = (
            f"TIME {self.time_left}"
        )

        # Last 10 seconds
        if self.time_left <= 10:

            self.timer_label.color = (
                1,
                0.25,
                0.25,
                1
            )

        # Time finished
        if self.time_left <= 0:

            self.end_game(
                reason="TIME UP!"
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

        # Stop/remove balloons
        for child in self.children[:]:

            if isinstance(
                child,
                GameBalloon
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