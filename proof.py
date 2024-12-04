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
        x_label = MathTex("Re").next_to(axes.x_axis, RIGHT)
        y_label = MathTex("Im").next_to(axes.y_axis, UP)

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
        euler_title = MarkupText("Euler's Formula", font_size=30, gradient=(BLUE_A,BLUE_E)).move_to(3.5 * UP)
        euler_formula = MathTex(
            r"e^{i\theta} = \cos(\theta) + i\sin(\theta)"
        ).move_to(3* RIGHT + UP)

        # Add elements to the scene
        self.play(Write(euler_title),Create(VGroup(axes,x_label,y_label)))
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


