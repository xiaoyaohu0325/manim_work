from manim import *

class Add(Scene):
    def construct(self):
        da,db=Dot(point=[-3, 1, 0], color=BLUE), Dot(point=[1, 1, 0], color=BLUE)
        a_text = Text("A").next_to(da, LEFT)
        b_text = Text("B").next_to(db, RIGHT)
        l1=Line(da.get_center(),db.get_center()).set_color(BLUE)

        dc,dd=Dot(point=[-1.5, -1, 0], color=GREEN), Dot(point=[0.8, -1, 0], color=GREEN)
        c_text = Text("C").next_to(dc, LEFT)
        d_text = Text("D").next_to(dd, RIGHT)
        l2=Line(dc.get_center(),dd.get_center()).set_color(GREEN)

        d1,d2=Dot(point=[0, 0, 0], color=RED), Dot(point=[0, 0, 0], color=RED)
        line = Line(d1.get_center(), d2.get_center()).set_color(RED)
        line.add_updater(lambda z: z.become(Line(d1.get_center(),d2.get_center()).set_color(RED)))

        circle = Circle(arc_center=db.get_center(), radius=l2.get_length())

        self.add(da, db, a_text, b_text, l1, dc, dd, c_text, d_text, l2, d1, d2, line)

        self.play(d1.animate.move_to(dc.get_center()), d2.animate.move_to(dd.get_center()))
        self.wait()
        self.play(d1.animate.move_to(db.get_center()), d2.animate.move_to(db.get_center() + [l2.get_length(), 0, 0]))
        self.wait()
        self.play(Create(Arc(radius=l2.get_length(), arc_center=db.get_center(), angle=PI*2)), MoveAlongPath(d2, circle), run_time=2, rate_func=linear)
        self.wait()
        self.remove(d1, d2, line)
        d_start = Dot(point=[-1.3, 1, 0], color=RED)
        d_end = Dot(point=[3.3, 1, 0], color=RED)
        e_text = Text("E").next_to(d_end, RIGHT)
        self.play(Create(d_start))
        self.play(Create(Line([-1.3, 1, 0], [4, 1, 0]).set_color(RED)))
        self.play(Create(d_end), Create(e_text))
        self.wait()