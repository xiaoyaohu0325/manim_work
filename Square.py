from manim import *

class Square(Scene):
    def construct(self):
        dot = Dot(color=RED)
        trace = TracedPath(dot.get_center)
        self.add(dot, trace)
        for i in range(60):
            self.draw_rect(dot, 2.0, ORIGIN, i * 5)


    def draw_rect(self, dot, length, start_pos, angle):
        rad = np.radians(angle)
        rad1 = np.radians(angle + 45)
        rad2 = np.radians(angle + 90)
        self.play(dot.animate.move_to([length * np.cos(rad), length * np.sin(rad), 0]), run_time=0.15, rate_func=linear)
        self.play(dot.animate.move_to([length * np.sqrt(2.0) * np.cos(rad1), length * np.sqrt(2.0) * np.sin(rad1), 0]), run_time=0.15, rate_func=linear)
        self.play(dot.animate.move_to([length * np.cos(rad2), length * np.sin(rad2), 0]), run_time=0.15, rate_func=linear)
        self.play(dot.animate.move_to(start_pos), run_time=0.15, rate_func=linear)