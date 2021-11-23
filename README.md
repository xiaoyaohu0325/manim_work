## A brief history of Manim
Manim was originally created by Grant Sanderson as a personal project and for use in his YouTube channel, 3Blue1Brown. As his channel gained popularity, many grew to like the style of his animations and wanted to use manim for their own projects. However, as manim was only intended for personal use, it was very difficult for other users to install and use it.

In late 2019, Grant started working on faster OpenGL rendering in a new branch, known as the shaders branch. In mid-2020, a group of developers forked it into what is now the community edition; this is the version documented on this website. In early 2021, Grant merged the shaders branch back into master, making it the default branch in his repository. The old version is still available as the branch cairo-backend.

There are currently three main versions of manim. They are as follows:

* ManimCE: The community edition of manim. This is the version documented by this website, and is named manim on pip.
* ManimGL: The current version of manim that is used by 3blue1brown. It supports OpenGL rendering and interactivity, and is named manimgl on pip. You can find documentation for it here.
* ManimCairo: The old version of manim originally used by 3blue1brown. It is not available on pip.

# quick start
Every animation must be contained within the construct() method of a class that derives from Scene.
Other code, for example auxiliary or mathematical functions, may reside outside the class.

manim -pql scene.py SquareToCircle

This command executes manim on the file scene.py and SquareToCircle is the scene to render.
This is necessary because a single scene file may contain more than one scene.

-p means play the scene once it's rendered
-ql tells manim to render the scene in low quality, which is 480 resolution and 15 fps
Another options: -qm, -qh, -qk for medium, high and 4k quality, respectively.

* ql - 480 resolution at 15 fps
* qh - 1080 resolution at 60 fps

By default manim will output .mp4 files. If you want your animations in .gif format instead, use the -i flag.

> Every animation must be contained within the construct() method of a class that derives from Scene.
> Other code, for example auxiliary or mathematical functions, may reside outside the class.

## Sections
Each section produces its own output video.

```
def construct(self):
    # play the first animations...
    # you don't need a section in the very beginning as it gets created automatically
    self.next_section()
    # play more animations...
    self.next_section("this is an optional name that doesn't have to be unique")
    # play even more animations...
    self.next_section("this is a section without any animations, it will be removed")
```

For videos to be created for each section you have to add the --save_sections flag to the Manim call like this:

> manim --save_sections scene.py

# Building blocks
Essentially, manim puts at your disposal three different concepts that you can orchestrate together to produce
mathematical animations: the **mathematical object** (or **mobject** for short) the **animation**, and the **scene**.
Each of these three concepts is implemented in mainm as a separate class: the MObject, Animation and Scene classes.

## MObjects
Each class that derives from Mobject represents an object that can be displayed on the screen. For example, simple
shapes such as Circle, Arrow, and Rectangle are all mobjects. More complicated constructs such as Axes, FunctionGraph,
or BarChart are mobjects as well.

 you will rarely need to use plain instances of Mobject; instead, you will most likely create instances of its derived
 classes. One of these derived classes is VMobject. The V stands for Vectorized Mobject. In essence, a vmobject is a
 mobject that uses vector graphics to be displayed. Most of the time, you will be dealing with vmobjects.

 > Unlike other graphics software, manim places the center of coordinates at the center of the screen. The positive
 > vertical direction is up, and the positive horizontal direction is right.

```
class MobjectPlacement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # place the circle two units left from the origin
        circle.move_to(LEFT * 2)
        # place the square to the left of the circle
        square.next_to(circle, LEFT)
        # align the left border of the triangle to the left border of the circle
        triangle.align_to(circle, LEFT)

        self.add(circle, square, triangle)
        self.wait(1)
```

This scene uses two of the main functions that change the visual style of a mobject: set_stroke() and set_fill().
The former changes the visual style of the mobject’s border while the latter changes the style of the interior.
By default, most mobjects have a fully transparent interior so you must specify the opacity parameter to display the color.


## Animations
At the heart of manim is animation. Generally, you can add an animation to your scene by calling the **play()** method.

Put simply, animations are procedures that interpolate between two mobjects. For example, FadeIn(square) starts with a
fully transparent version of square and ends with a fully opaque version, interpolating between them by gradually increasing
the opacity. As another example, Rotate starts with the mobject passed to it as argument, and ends with the same object but
rotated by a certain amount, this time interpolating the mobject’s angle instead of its opacity.

Any property of a mobject that can be changed can be animated. In fact, any method that changes a mobject’s property can be
used as an animation, through the use of **animate()**. animate() is a property of all mobjects that
**animates the methods that come afterward**. For example, square.set_fill(WHITE) sets the fill color of the square,
while sqaure.animate.set_fill(WHITE) animates this action.

```
# animate the change of position and the rotation at the same time
self.play(square.animate.shift(UP).rotate(PI / 3))
self.wait(1)
```

By default, any animation passed to play() lasts for exactly one second. Use the run_time argument to control the duration.

> self.play(square.animate.shift(UP), run_time=3)

Mobjects contains points that define their boundaries. These points can be used to add other mobjects respectively to each other,
e.g. by methods like get_center() , get_top() and get_start().

The Transform function **maps points of the previous mobject to the points of the next mobject**. This might result in strange
behaviour, e.g. when the dots of one mobject are arranged clockwise and the other points are arranged counterclockwise.
Here it might help to use the flip function and reposition the points via the roll function of numpy.

```
class ExampleRotation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1a = Square().set_color(RED).shift(LEFT)
        m1b = Circle().set_color(RED).shift(LEFT)
        m2a= Square().set_color(BLUE).shift(RIGHT)
        m2b= Circle().set_color(BLUE).shift(RIGHT)

        points = m2a.points
        points = np.roll(points, int(len(points)/4), axis=0)
        m2a.points = points

        self.play(Transform(m1a,m1b),Transform(m2a,m2b), run_time=1)
```

## Scenes
The Scene class is the connective tissue of manim. Every mobject has to be added to a scene to be displayed, or removed from
it to cease being displayed. Every animation has to be played by a scene, and every time interval where no animation occurs
is determined by a call to **wait()**. All of the code of your video must be contained in the construct() method of a class that
derives from Scene. Finally, a single file may contain multiple Scene subclasses if multiple scenes are to be rendered at the same time.

# Configuration
Manim provides an extensive configuration system that allows it to adapt to many different use cases. There are many configuration options that can be configured at different times during the scene rendering process. Each option can be configured programmatically via the ManimConfig class, at the time of command invocation via command-line arguments, or at the time the library is first imported via the config files.

The most direct way of configuring manim is through the global config object, which is an instance of **ManimConfig**.
Most classes, including Camera, Mobject, and Animation, read some of their default configuration from the global config.

```
>>> from manim import *
>>> config.background_color = WHITE
>>> config["background_color"] = WHITE
```

# Text
There are two different ways by which you can render Text in videos:
* Using Pango (text_mobject)
* Using LaTeX (tex_mobject)

If you want to render simple text, you should use either Text or MarkupText, or one of its derivatives like Paragraph.
LaTeX should be used when you need mathematical typesetting.

Simple Text
```
def construct(self):
    text = Text("Hello world", font_size=144)
    self.add(text)
```

MarkupText, which is similar to Text, the only difference between them is that this accepts and processes PangoMarkup (which is similar to html), instead of just rendering plain text.
```
def construct(self):
    text = MarkupText(f'all in red <span fgcolor="{YELLOW}">except this</span>', color=RED)
    self.add(text)
```

LaTex
```
def construct(self):
    tex = Tex(r"\LaTeX", font_size=144)
    self.add(tex)
```

MathTex
Everything passed to MathTex is in math mode by default. To be more precise, MathTex is processed within an align* environment. You can achieve a similar effect with Tex by enclosing your formula with $ symbols: $\xrightarrow{x^6y^8}$:
```
def construct(self):
    rtarrow0 = MathTex(r"\xrightarrow{x^6y^8}", font_size=96)
    rtarrow1 = Tex(r"$\xrightarrow{x^6y^8}$", font_size=96)

    self.add(VGroup(rtarrow0, rtarrow1).arrange(DOWN))
```
