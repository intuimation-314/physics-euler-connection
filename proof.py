from manim import *


class VectorsInPlane(Scene):
    def construct(self):
        # Number of vectors
        n = 9  # Set number of vectors to 9
        radius = 2  # Radius of the circle
        center = 3 * LEFT  # Center of the circle

        # Create axes with grids
        axes = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        ).scale(0.6).shift(center)  # Shift axes to match the new center
        self.play(Create(axes))

        # Create vectors and display them
        vectors = VGroup()
        vector_labels = VGroup()
        for i in range(n):
            angle = TAU * i / n  # Angle in radians
            end_point = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
            vector = Arrow(
                start=center,
                end=end_point,
                buff=0,
                color=BLUE,
                stroke_width=2,  # Thin arrows
            )
            # Add labels based on conditions
            if i == 4:
                label = MathTex(r"k").move_to(1.15 * (end_point - center) + center).scale(0.6)
            elif i == n - 2:
                label = MathTex(r"n-2").move_to(1.15 * (end_point - center) + center).scale(0.6)
            elif i == n - 1:
                label = MathTex(r"n-1").move_to(1.15 * (end_point - center) + center).scale(0.6)
            elif 4 < i < n - 2:  # Dots for mid-section
                label = MathTex(r"\cdots").move_to(1.15 * (end_point - center) + center).scale(0.6)
            else:
                label = MathTex(f"{i}").move_to(1.15 * (end_point - center) + center).scale(0.6)

            vectors.add(vector)
            vector_labels.add(label)

        # Animate vectors and labels
        self.play(Create(vectors))
        self.play(Create(vector_labels))
        self.wait(2)

        # Highlight vector labeled "k"
        k_vector = vectors[4]  # Get the vector at index 4 (labeled "k")
        k_end = k_vector.get_end()  # Get the end point of vector "k"
        k_angle = TAU * 4 / n  # Angle for the "k" vector

        # Projections of "k" vector
        x_projection = DashedLine(start=center, end=[k_end[0], center[1], 0], color=GREEN)
        y_projection = DashedLine(start=[k_end[0], center[1], 0], end=k_end, color=GREEN)

        # Animate projections
        self.play(Create(x_projection), Create(y_projection))

        # Angle arc and label
        theta_arc = Arc(
            radius=0.5,
            start_angle=0,
            angle=k_angle,
            color=RED,
            stroke_width=2
        ).move_arc_center_to(center)
        theta_label = MathTex(r"\theta_k").scale(0.7).next_to(theta_arc, RIGHT)

        # Animate angle arc and label
        self.play(Create(theta_arc), Write(theta_label))
        self.wait(2)

        # Highlight components
        x_label = MathTex(r"x_k").scale(0.6).next_to(x_projection, DOWN)
        y_label = MathTex(r"y_k").scale(0.6).next_to(y_projection, LEFT)

        self.play(Write(x_label), Write(y_label))
        self.wait(2)

        # Display equations for x_k, y_k, and v_k
        equations = VGroup(
            MathTex(r"x_k = \cos(\theta_k) \hat{i}\quad\text{and}\quad y_k = \sin(\theta_k) \hat{j}").scale(0.6),
            MathTex(r"\vec{\mathbf{v}}_k = \cos(\theta_k) \hat{i} + \sin(\theta_k) \hat{j}").scale(0.6),
            MathTex(r"\vec{\mathbf{v}}_k = \cos\left(\frac{2k\pi}{n}\right) \hat{i} + \sin\left(\frac{2k\pi}{n}\right) \hat{j}").scale(0.6),
            MathTex(r"\sum_{k=0}^{n-1}\vec{\mathbf{v}}_k = \sum_{k=0}^{n-1} \left[\cos\left(\frac{2k\pi}{n}\right) \hat{i} + \sin\left(\frac{2k\pi}{n}\right) \hat{j}\right]").scale(0.55),
            MathTex(r"\sum_{k=0}^{n-1}\vec{\mathbf{v}}_k = \sum_{k=0}^{n-1} \cos\left(\frac{2k\pi}{n}\right) \hat{i} + \sum_{k=0}^{n-1} \sin\left(\frac{2k\pi}{n}\right) \hat{j}").scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(RIGHT * 3)
        tex = MathTex(r"=\frac{2k\pi}{n}").next_to(theta_label, RIGHT, buff=0.01).scale(0.6)
        # Animate equations appearing on the right
        self.play(Write(equations[0]))
        self.wait(2)
        self.play(Write(equations[1]))
        self.wait(2)
        self.play(FadeOut(VGroup(x_label, y_label, x_projection, y_projection)))
        self.wait()

        # Display arcs and angle labels for first few vectors
        arc_angle_group = VGroup()
        for i in range(4):
            angle = TAU * (i + 1) / n
            arc = Arc(
                radius=0.5,
                start_angle=0,
                angle=angle,
                color=YELLOW,
                stroke_width=2,
            ).move_arc_center_to(center)
            angle_label = MathTex(
                fr"\theta_{i+1} = \frac{{2 \cdot {i+1} \cdot \pi}}{{{n}}} \text{{ rad}}",
                color = YELLOW
            ).scale(0.6).move_to( 2 * RIGHT)
            arc_angle_group.add(VGroup(arc, angle_label))

        self.play(Create(arc_angle_group[0]))
        
        for i in range(3):  # Animate the first few arcs
            if i == 2:  # For the last arc in the range
                self.play(ReplacementTransform(arc_angle_group[i], arc_angle_group[i + 1]))
                self.wait()
                self.play(FadeOut(arc_angle_group[i + 1]))
            else:
                self.play(ReplacementTransform(arc_angle_group[i], arc_angle_group[i + 1]))
                self.wait()
        self.play(Write(tex))
        self.wait(3)
        self.play(FadeOut(VGroup(equations[:2])),Write(equations[2]))
        self.wait()
        self.play(Write(equations[3]))
        self.wait()
        self.play(Write(equations[4]))
        self.wait()
        self.play(FadeOut(VGroup(equations[2],equations[3])))
        self.play(equations[4].animate.shift(2*UP))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

                # Add colorful explanatory text
        explanation_text = Tex(
            "To prove that the vector sum is zero, we need to show that both the sum of ",
            "the x and y components sum to zero simultaneously.", 
            color=BLUE
        )
        explanation_text.arrange(DOWN).move_to(3 * UP).scale(0.7)

        # Add the equations
        equations = MathTex(
            r"\sum_{k=0}^{n-1} \cos\left(\frac{2k\pi}{n}\right) = 0 \quad \text{and} \quad "
            r"\sum_{k=0}^{n-1} \sin\left(\frac{2k\pi}{n}\right) = 0"
        ).scale(0.8)

        # Animate text and equations
        self.play(Write(explanation_text))
        self.play(Write(equations))
        self.wait(3)

class EulerFormula(Scene):
    def construct(self):
        n = 9
        radius = 2  # Radius of the circle
        center = 3 * LEFT  # Center of the circle
        
        # Create axes with grids
        axes = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        ).scale(0.6).shift(center)  # Shift axes to match the new center

        # Add labels for the axes
        x_label0 = MathTex("Re").next_to(axes.x_axis, RIGHT)
        y_label0 = MathTex("Im").next_to(axes.y_axis, UP)

        # Define the angle theta
        theta = PI / 4

        # Create the moving point
        point = Dot(color=YELLOW).move_to(
           center + radius * np.array([np.cos(theta), np.sin(theta), 0])
        )

        # Create the line from the origin to the point
        radius_line = Line(
            axes.c2p(0, 0),
            center + radius * np.array([np.cos(theta), np.sin(theta), 0]),
            color=YELLOW,
        )

        # Add the angle arc and label
        theta_arc = Arc(
            radius=0.4,
            start_angle=0,
            angle=theta,
            arc_center=axes.c2p(0, 0),
            color=GREEN,
        )
        theta_label = MathTex(r"\theta").scale(0.6).next_to(
            theta_arc.point_from_proportion(0.5), RIGHT + UP, buff=0.1
        )

        # Add real and imaginary projections
        imag_line = DashedLine(
           center + radius * np.array([np.cos(theta), 0, 0]),
            center + radius * np.array([np.cos(theta), np.sin(theta), 0]),
            color=RED,
        )
        real_line = DashedLine(
            center + radius * np.array([0, np.sin(theta), 0]),
            center + radius * np.array([np.cos(theta), np.sin(theta), 0]),
            color=GREEN,
        )


        # Add the text for the real and imaginary components
        real_label = MathTex(r"\cos(\theta)").scale(0.6).next_to(
            real_line, UP
        )
        imag_label = MathTex(r"\sin(\theta)").scale(0.6).next_to(
            imag_line, RIGHT
        )

        # Euler's formula text
        euler_title = MarkupText("Euler's Formula", color = BLUE).move_to(3.5 * UP)
        euler_formula = MathTex(
            r"e^{i\theta} = \cos(\theta) + i\sin(\theta)"
        ).move_to(3* RIGHT + UP)

        # Add elements to the scene
        self.play(Write(euler_title),Create(VGroup(axes,x_label0,y_label0)))
        self.play(Create(radius_line), Create(point))
        self.play(Create(theta_arc), Write(theta_label))
        self.wait(3)
        self.play(Create(real_line), Create(imag_line))
        self.play(Write(real_label), Write(imag_label))
        self.play(Write(euler_formula))
        self.wait(2)
        self.play(FadeOut(VGroup(point, radius_line, theta_arc, theta_label,real_label,imag_label,real_line,imag_line,euler_title)))
        self.play(euler_formula.animate.scale(0.6).shift(2*UP + LEFT))
        rec = SurroundingRectangle(euler_formula)
        self.play(Create(rec))
        self.wait()


        # Create vectors and display them
        vectors = VGroup()
        vector_labels = VGroup()
        for i in range(n):
            angle = TAU * i / n  # Angle in radians
            end_point = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
            vector = Arrow(
                start=center,
                end=end_point,
                buff=0,
                color=BLUE,
                stroke_width=2,  # Thin arrows
            )
            # Add labels based on conditions
            if i == 4:
                label = MathTex(r"k").move_to(1.15 * (end_point - center) + center).scale(0.6)
            elif i == n - 2:
                label = MathTex(r"n-2").move_to(1.15 * (end_point - center) + center).scale(0.6)
            elif i == n - 1:
                label = MathTex(r"n-1").move_to(1.15 * (end_point - center) + center).scale(0.6)
            elif 4 < i < n - 2:  # Dots for mid-section
                label = MathTex(r"\cdots").move_to(1.15 * (end_point - center) + center).scale(0.6)
            else:
                label = MathTex(f"{i}").move_to(1.15 * (end_point - center) + center).scale(0.6)

            vectors.add(vector)
            vector_labels.add(label)

        # Animate vectors and labels
        self.play(Create(vectors))
        self.play(Create(vector_labels))
        self.wait(2)
        
        # Display equations for x_k, y_k, and v_k
        equations = VGroup(
            MathTex(r"\vec{\mathbf{v}}_k = \cos\left(\frac{2k\pi}{n}\right) + i\sin\left(\frac{2k\pi}{n}\right)").scale(0.7),
            MathTex(r"e^{i\frac{2k\pi}{n}} = \cos\left(\frac{2k\pi}{n}\right) + i\sin\left(\frac{2k\pi}{n}\right)").scale(0.7),
            MathTex(r"\sum_{k=0}^{n-1} e^{i\frac{2k\pi}{n}} = \sum_{k=0}^{n-1} \cos\left(\frac{2k\pi}{n}\right) + i\sum_{k=0}^{n-1} \sin\left(\frac{2k\pi}{n}\right)").scale(0.6),
        ).arrange(DOWN, aligned_edge=LEFT).move_to(RIGHT * 4)

        # Highlight vector labeled "k"
        k_vector = vectors[4]  # Get the vector at index 4 (labeled "k")
        k_end = k_vector.get_end()  # Get the end point of vector "k"
        k_angle = TAU * 4 / n  # Angle for the "k" vector

        # Projections of "k" vector
        y_projection = DashedLine(center + radius * np.array([np.cos(k_angle), 0, 0]),
                                center + radius * np.array([np.cos(k_angle), np.sin(k_angle), 0]),
                                color=RED,)
        x_projection = DashedLine(center + radius * np.array([np.cos(k_angle), np.sin(k_angle), 0]),
            center + radius * np.array([0, np.sin(k_angle), 0]),
            color=GREEN,)

        # Animate projections
        self.play(Create(x_projection), Create(y_projection))

        # Angle arc and label
        theta_arc = Arc(
            radius=0.5,
            start_angle=0,
            angle=k_angle,
            color=RED,
            stroke_width=2
        ).move_arc_center_to(center)
        theta_label = MathTex(r"\frac{2k\pi}{n}").scale(0.7).next_to(theta_arc, RIGHT)

        # Animate angle arc and label
        self.play(Create(theta_arc), Write(theta_label))
        self.wait(2)

        # Highlight components
        x_label = MathTex(r"Re").scale(0.6).next_to(x_projection, UP)
        y_label = MathTex(r"Im").scale(0.6).next_to(y_projection, LEFT)

        self.play(Write(x_label), Write(y_label))
        self.wait(2)

        self.play(Write(equations[0]))
        self.wait(2)
        self.play(Indicate(euler_formula))
        self.play(Write(equations[1]))
        self.wait(2)
        self.play(Write(equations[2]))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

                        # Add colorful explanatory text
        explanation_text = MathTex(
            r"\text{If we could somehow prove that the sum of these exponents is 0, i.e,}",
           r"\sum_{k=0}^{n-1}e^{i\frac{2k\pi}{n}} = 0",
           r"\text{This would imply: }",
           r"\sum_{k=0}^{n-1} \cos\left(\frac{2k\pi}{n}\right) = 0 \quad \text{and} \quad \sum_{k=0}^{n-1} \sin\left(\frac{2k\pi}{n}\right) = 0"
        ).move_to(UP)
        VGroup(explanation_text[0],explanation_text[2]).set_color(BLUE)
        explanation_text.arrange(DOWN).scale(0.7)
        self.play(Write(explanation_text[:2]))
        self.wait()
        self.play(Write(explanation_text[2:]))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        explanation_text1 = MathTex(r"\text{Let's jump right into our final proof.}",
                                    r"\sum_{k=0}^{n-1} e^{i\frac{2k\pi}{n}}",
                                    r"\text{When we expand this summation, it looks like this:}",
                                    r"\sum_{k=0}^{n-1} e^{i\frac{2k\pi}{n}} = 1 + e^{i \frac{2\pi}{n}} + e^{i \frac{4\pi}{n}} + \ldots + e^{i \frac{2(n-1)\pi}{n}}").move_to(UP)
        VGroup(explanation_text1[0],explanation_text1[2]).set_color(BLUE)
        explanation_text1.arrange(DOWN,buff=0.5).scale(0.7)
        self.play(Write(explanation_text1[0]))
        self.wait()
        self.play(Write(explanation_text1[1]))
        self.wait(2)
        self.play(Write(explanation_text1[2:]))
        self.wait(2)
        self.play(FadeOut(explanation_text1[:3]))
        self.wait()
        self.play(explanation_text1[3].animate.move_to(3*UP).scale(1))
        self.wait(2)

        explanation_text2 = MathTex(
            r"\text{Notice } e^{i\frac{2\pi}{n}} \text{ is common in all terms, so let } e^{i\frac{2\pi}{n}} = x",
            r"1 + x + x^2 + x^3 + \ldots + x^{n-1}",
            r"\text{This should look familiar---it's a geometric series!}",
            r"\frac{1-x^n}{1-x}", 
            r"= \frac{1 - e^{i\frac{2\pi}{n} \cdot n}}{1 - e^{i\frac{2\pi}{n}}}",
            r"= \frac{1 - e^{i2\pi}}{1 - e^{i\frac{2\pi}{n}}}",
            r"= \frac{1 - 1}{1 - e^{i\frac{2\pi}{n}}} = 0",
            )
        explanation_text3 = MathTex(r"e^{i2\pi} = \cos(2\pi) + i\sin(2\pi)",
                                    color = YELLOW
                                    ).scale(0.8).move_to(2 * DOWN)

        VGroup(explanation_text2[0],explanation_text2[2]).set_color(BLUE)
        explanation_text2[0:4].arrange(DOWN,buff=0.5).scale(0.7).next_to(explanation_text1[3], DOWN, buff=0.5)
        explanation_text2[4].next_to(explanation_text2[3], RIGHT, buff=0.1).scale(0.7)
        explanation_text2[5].next_to(explanation_text2[3], RIGHT, buff=0.1).scale(0.7)
        explanation_text2[6].next_to(explanation_text2[3], DOWN, buff=0.5).scale(0.7)
        self.play(Write(explanation_text2[0]))
        self.wait()
        self.play(Write(explanation_text2[1]))
        self.wait(2)
        self.play(Write(explanation_text2[2:4]))
        self.wait(2)
        self.play(Write(explanation_text2[4]))
        self.wait()
        self.play(ReplacementTransform(explanation_text2[4],explanation_text2[5]))
        self.wait()
        self.play(Write(explanation_text3))
        self.wait()
        self.play(FadeOut(explanation_text3))
        self.wait()
        self.play(Write(explanation_text2[6]))
        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.wait()
        
        # Create a brace with label "r"
        brace = Brace(vectors[0], UP)
        brace_label = MathTex(r"r").next_to(brace, DOWN)

        # Animate vectors, brace, and label
        self.play(Create(vectors), Create(VGroup(axes, x_label0, y_label0)))
        self.wait(2)
        self.play(vectors.animate.scale(1.2))
        self.play(Create(brace),Create(brace_label))
        self.wait()
        explanation_text4 = MathTex(r"\text{Euler representation for vectors looks like:}",
                                    r"\sum_{k=0}^{n-1} r \cdot e^{i\frac{2k\pi}{n}}",
                                    r"\text{r is constant, pull out of the summation:}",
                                    r"r \cdot \sum_{k=0}^{n-1} e^{i\frac{2k\pi}{n}}",
                                    r"r \cdot 0 = 0")
        VGroup(explanation_text4[0],explanation_text4[2]).set_color(BLUE)
        explanation_text4.arrange(DOWN,buff=0.5).scale(0.7).move_to(3.5 * RIGHT + UP)
        
        self.play(Write(explanation_text4[0]))
        self.wait()
        self.play(Write(explanation_text4[1]))
        self.wait(2)
        self.play(Write(explanation_text4[2]))
        self.wait(2)
        self.play(Write(explanation_text4[3]))
        self.wait()
        self.play(Write(explanation_text4[4]))
        self.wait(2)

class ContinuousProof(Scene):
    def construct(self):
        mu = MathTex(r"\mu").scale(5).set_color(BLUE).shift(LEFT + DOWN)
        
        # Eyes: Create two small white circles with black pupils
                # Eyes: Create two white ovals for the eyes
        left_eye_white = Ellipse(width=0.3, height=0.4, color=WHITE, fill_opacity=1).shift(UP * 0.6 + LEFT * 1.25 + DOWN)
        right_eye_white = Ellipse(width=0.3, height=0.4, color=WHITE, fill_opacity=1).shift(UP * 0.6 + LEFT * 0.65 + DOWN)
        left_eye_pupil = Dot(point=UP * 0.6 + LEFT * 1.25 + DOWN, radius=0.1, color=BLACK)
        right_eye_pupil = Dot(point=UP * 0.6 + LEFT * 0.65 + DOWN, radius=0.1, color=BLACK)
        
        # Add small circle in the middle of each pupil
        left_eye_glint = Dot(point=UP * 0.6 + LEFT * 1.25 + DOWN, radius=0.03, color=WHITE, fill_opacity=0.8)
        right_eye_glint = Dot(point=UP * 0.6 + LEFT * 0.65 + DOWN, radius=0.03, color=WHITE,fill_opacity=0.8)
        
        # Group the eyes for easy animation
        eyes = VGroup(left_eye_white, right_eye_white, 
                      left_eye_pupil, right_eye_pupil,
                      left_eye_glint,right_eye_glint)

        # Assemble the bot
        mu_bot = VGroup(mu, eyes)


        # Mouth (arc for different moods)
        happy_mouth = Arc(radius=0.2, 
                          start_angle= - 3* PI/4,
                          angle= 2 * PI/4).set_color(WHITE).move_to(DOWN * 0.9 + LEFT)
        sad_mouth = Arc(radius=0.2, start_angle= PI/4,
                        angle= 2 *PI/4).set_color(WHITE).move_to(DOWN * 0.9 + LEFT)
        thinking_mouth = Line(start=LEFT * 0.15 + DOWN * 0.9 + LEFT, 
                              end=RIGHT * 0.15 + DOWN * 0.9 + LEFT).set_color(WHITE)
        mu_bot_happy = VGroup(mu_bot,happy_mouth)
        mu_bot_sad = VGroup(mu_bot,sad_mouth)
        mu_bot_thinking = VGroup(mu_bot,thinking_mouth)
        # Thinking cloud
        cloud = SVGMobject(r"C:/Users/Sumit Sah/Downloads/thinking_cloud.svg").scale(2).set_color(WHITE).next_to(mu, UP + RIGHT)
        cloud_text = Tex("Isn't limited to finite", 
                         "number of vectors!")
        cloud_text.arrange(DOWN).scale(0.6).move_to(cloud.get_center() + 0.5*UR )
        cloud_text1 = Tex("Holds for continuous", 
                          "distribution as well!")
        cloud_text1.arrange(DOWN).scale(0.6).move_to(cloud.get_center() + 0.5*UR)
        cloud_text2 = Tex("Remember the charged", 
                          "ring example?")
        cloud_text2.arrange(DOWN).scale(0.6).move_to(cloud.get_center() + 0.5*UR )

        # Blinking effect using fade-in and fade-out
        def blink():
            return AnimationGroup(
                FadeOut(left_eye_pupil,right_eye_pupil,
                        left_eye_glint,right_eye_glint),
                FadeIn(left_eye_pupil,right_eye_pupil,
                       left_eye_glint,right_eye_glint),
                lag_ratio=0.2,
            )

        
        # Intro Animation
        self.play(FadeIn(mu_bot_thinking), run_time=1.5)
        # Thinking cloud appears
        self.play(FadeIn(cloud), Write(cloud_text), run_time=2)
        # Blinking Animation
        self.play(blink(), run_time=0.5)
        self.wait(0.5)
        self.play(blink(), run_time=0.5)
        self.wait(1)
        
        self.play(ReplacementTransform(cloud_text,cloud_text1))
        # Blinking Animation
        self.play(blink(), run_time=0.5)
        self.wait(0.5)
        self.play(blink(), run_time=0.5)
        self.wait(1)
        
        self.play(ReplacementTransform(cloud_text1,cloud_text2))
        self.play(Transform(mu_bot_thinking, mu_bot_happy), run_time=1)
        # Blinking Animation
        self.play(blink(), run_time=0.5)
        self.wait(0.5)
        self.play(blink(), run_time=0.5)
        self.wait(2)


class ContinuousVectors(Scene):
    def construct(self):
        # Initial setup for the scene
        radius = 2  # Radius of the circle
        center = ORIGIN # Center of the circle

        # Create axes with grids
        axes = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        ).scale(0.6)  # Scale the axes
        self.play(Create(axes))

        # Function to create vectors dynamically based on n
        def create_vectors(n):
            vectors = VGroup()
            for i in range(n):
                angle = TAU * i / n  # Angle in radians
                end_point = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
                vector = Arrow(
                    start=center,
                    end=end_point,
                    buff=0,
                    color=BLUE,
                    stroke_width=2,
                )
                vectors.add(vector)
            return vectors

        # Create a ValueTracker to control the number of vectors
        n_tracker = ValueTracker(10)  # Initial number of vectors

        # Create an initial group of vectors
        vectors = create_vectors(10)

        # Display the number of vectors (n) on the screen
        n_text = MathTex(f"n = {n_tracker.get_value()}").scale(0.7).to_edge(UP)
        self.play(Write(n_text))

        # Add vectors to the scene
        self.add(vectors)

        # Function to update the vectors and text based on n
        def update_scene(n):
            # Update the text
            n_text.become(MathTex(f"n = {n}").scale(0.7).to_edge(UP))
            # Create the new vectors
            new_vectors = create_vectors(n)
            # Transform the current vectors to the new set
            self.play(Transform(vectors, new_vectors), run_time=0.5)

        # Animate transformation from 10 vectors to 1000 vectors
        for n in [20, 40, 60, 80, 100, 200, 500, 1000]:
            self.play(n_tracker.animate.set_value(n), run_time=1)  # Animate the ValueTracker
            update_scene(n)

        # Wait before finishing the scene
        self.wait(2)

class SumToIntegral(Scene):
    def construct(self):
        # Create the introductory text for summation
        intro_text = Tex(r"As $n \to \infty $, the summation", 
                         r"can be transformed into an intgral",
                         color=BLUE).scale(1.5)
        intro_text.arrange(DOWN).to_edge(UP)

        # Create the integral formula
        integral = MathTex(
            r"\lim_{n \to \infty} \sum_{k=0}^{n-1} e^{i\frac{2k\pi}{n}}",
            r" = \frac{n}{2\pi} \int_0^{2\pi} e^{i\theta} \, d\theta",
        ).scale(1.5)
        integral.next_to(intro_text, DOWN, buff=1)

        # Display "The summation" and formula
        self.play(Write(intro_text))
        self.wait(1)

        # Display "transformed into the integral:" and formula
        self.play(Write(integral))
        self.wait(2)