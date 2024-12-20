from manim import *

class BlockOnSurface(Scene):
    def construct(self):

        # Add the colorful title at the top
        title = MarkupText(
            "Imagine a block on a frictionless surface being pulled by force",
            gradient=(BLUE, GREEN)
        ).scale(0.7).to_edge(UP)
        
        # Setting up the surface
        surface = Line(LEFT * 5, RIGHT * 5, color=GREY)
        surface_label = Text("Frictionless Surface").scale(0.5).next_to(surface, DOWN)

        # Setting up the block
        block = Square(side_length=1, color=BLUE, fill_opacity=1).move_to(LEFT * 4 + UP * 0.5)
        block_label = Text("Block", font_size=24).next_to(block, UP)

        # Setting up the force vector
        force_arrow = always_redraw(lambda:
                                    Arrow(start=block.get_center(), end=block.get_right() + RIGHT, 
                                          color=RED))
        force_label = always_redraw(lambda:
                                    Text("F", color=RED).scale(0.8).next_to(force_arrow, UP))

        # Add the title
        self.play(Write(title))

        # Animations for the scene
        self.play(Create(surface), Write(surface_label))
        self.play(FadeIn(block), Write(block_label))
        self.wait(1)

        self.play(GrowArrow(force_arrow), Write(force_label))
        self.wait(1)

        # Animate block moving to the right
        self.play(block.animate.shift(RIGHT * 8), rate_func=lambda x: x**2)
        self.wait()

        # Fade out the block and force
        self.play(FadeOut(VGroup(force_arrow, force_label, block_label, surface_label)))

        # Move block to origin with animation
        self.play(block.animate.move_to(ORIGIN + UP * 0.5))
        radius = 2  # Radius of the circle
        center = block.get_center()

        # Create and animate circles of arrows with angle labels
        first_arrows = VGroup()  # The first set of arrows to render
        num_arrows = 2  # Initial number of arrows
        for i in range(num_arrows):
            angle = TAU * i / num_arrows  # Angle in radians
            start_point = center
            end_point = center + np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
            arrow = Arrow(start=start_point, end=end_point, color=RED, stroke_width=2)
            first_arrows.add(arrow)
        
            # Angle Label Setup
            angle_arc = Arc(
                radius=radius / 3,  # Arc radius
                start_angle=0, 
                angle=TAU / 2,
                color=YELLOW,
            ).move_arc_center_to(center)
            
            angle_label = MathTex(r"\frac{2\pi}{" + str(2) + r"}").scale(0.7)
            angle_label.next_to(angle_arc, UR)

        # Show the first group of arrows
        self.play(Create(first_arrows))
        self.wait()
        self.play(Create(angle_label),Create(angle_arc))
        self.wait(2)
        self.play(FadeOut(angle_arc), FadeOut(angle_label))  # Fade out the arc and label

        # Create successive arrow groups and animate
        previous_arrows = first_arrows
        for j in range(3, 8):  # Increasing number of arrows
            current_arrows = VGroup()
            for i in range(j):
                angle = TAU * i / j
                start_point = center
                end_point = center + np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
                arrow = Arrow(start=start_point, end=end_point, color=RED, stroke_width=2)
                current_arrows.add(arrow)

            # Angle Label Setup
            angle_arc = Arc(
                radius=radius / 3,  # Arc radius
                start_angle=0, 
                angle=TAU / j,
                color=YELLOW,
            ).move_arc_center_to(center)
            
            angle_label = MathTex(r"\frac{2\pi}{" + str(j) + r"}").scale(0.7)
            angle_label.next_to(angle_arc, UR)

            # Animate replacement and angle labels
            self.play(ReplacementTransform(previous_arrows, current_arrows), Create(angle_arc), Write(angle_label))
            self.wait(2)
            self.play(FadeOut(angle_arc), FadeOut(angle_label))  # Fade out the arc and label

            # For j = 3, illustrate the parallelogram law
            if j == 3:
                # The first two arrows (current_arrows[0] and current_arrows[1]) will be added using the parallelogram law
                vec_1 = current_arrows[0]
                vec_2 = current_arrows[1]

                # The resultant vector formed by adding vec_1 and vec_2
                res_angle = PI/3
                resultant_vec = Arrow(start=center, end=center + np.array([radius * np.cos(res_angle), radius * np.sin(res_angle), 0]), color=PURPLE, stroke_width=3)
        
                # Create dashed lines showing the parallelogram sides
                dashed1 = DashedLine(vec_1.get_end(), resultant_vec.get_end())
                dashed2 = DashedLine(vec_2.get_end(), resultant_vec.get_end())

                # Animate the parallelogram visualization
                self.play(Create(dashed1), Create(dashed2), Create(resultant_vec))
                self.wait(2)
                self.play(FadeOut(dashed1), FadeOut(dashed2), FadeOut(resultant_vec))

            previous_arrows = current_arrows

        # Fade out the last group of arrows
        self.play(FadeOut(previous_arrows))
        self.wait(1)

        single_force_arrow = Arrow(start=ORIGIN + 0.5*UP, end = RIGHT*2 + 0.5*UP, color=RED, stroke_width=2)
        self.play(FadeIn(single_force_arrow))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))


class NEqualVectors(Scene):
    def construct(self):
        
        # Set the number of vectors
        n = 9  # Change this value to the desired number of vectors

        tex_lines = [
            "If n equal vectors are lined up",
            "making an angle of $\\frac{2\pi}{n}$ to each",
            "other, then the resultant is 0.",
        ]
        
        # Create text objects
        text_group = VGroup(*[Tex(line) for line in tex_lines if line])
        text_group.arrange(DOWN, aligned_edge=LEFT)
        text_group.move_to(3*RIGHT + UP)  # Move text group to desired position

        formula = MathTex(r"\sum_{n=0}^{k-1}\vec{v}_k = 0").next_to(text_group, DOWN, buff=0.8)
        
        # Create the central object
        obj = Dot(ORIGIN, color=WHITE).scale(2)
        
        # Angle between the vectors
        angle = 2 * PI / n
        
        # Create and display the vectors
        vectors = [
            Arrow(
                start=obj.get_center(), 
                end=obj.get_center() + np.array([np.cos(k * angle), np.sin(k * angle), 0]) * 2.5, 
                buff=0, 
                color=BLUE,
                stroke_width=2
            ) for k in range(n)
        ]
        forces = VGroup(*vectors)

        # Create arcs and angle labels between vectors, but only show one at a time
        arc = Arc(
            radius=1, 
            start_angle=0, 
            angle=angle, 
            color=YELLOW,
            stroke_width=2
        ).move_arc_center_to(obj.get_center())
        angle_label = MathTex(r"\frac{2\pi}{n}").scale(0.6)
        angle_label.move_to(arc.point_from_proportion(0.5) + 0.5 * UP)

        # Group for initial arc and label
        arc_angle_group = VGroup(arc, angle_label)

        self.play(Create(obj))
        self.play(Create(forces))
        self.wait(1)

        # Animate each arc and label one by one
        for k in range(n):
            new_arc = Arc(
                radius=1,
                start_angle=k * angle,
                angle=angle,
                color=YELLOW,
                stroke_width=2
            ).move_arc_center_to(obj.get_center())

            new_angle_label = MathTex(r"\frac{2\pi}{n}").scale(0.6)
            new_angle_label.move_to(new_arc.point_from_proportion(0.5) + 0.5 * UP)

            new_arc_angle_group = VGroup(new_arc, new_angle_label)
        
            self.play(Transform(arc_angle_group, new_arc_angle_group))
        
        self.wait(1)
        self.play(FadeOut(arc_angle_group))
        self.play(VGroup(obj,forces).animate.shift(LEFT*3.5))
        self.wait(1)
        self.play(Write(text_group))
        self.wait(1)
        self.play(Write(formula))
        self.wait(1)

        # Shift the vectors to form a closed polygon
        closed_polygon_vectors = VGroup()
        for i in range(n):
            if i == 0:
                start = obj.get_center() + np.array([np.cos(i * angle), np.sin(i * angle), 0]) * 2.5
            else:
                start = end
            end = obj.get_center() + np.array([np.cos((i + 1) * angle), np.sin((i + 1) * angle), 0]) * 2.5
            closed_polygon_vectors.add(Arrow(start=start, end=end, buff=0, color=BLUE, stroke_width=2))

        self.play(Transform(forces, closed_polygon_vectors))
        self.wait(2)

        # Fade out text and elements
        self.play(FadeOut(text_group), FadeOut(formula))
        self.wait(1)
        self.play(FadeOut(forces), FadeOut(obj))
        self.wait(1)

class MuBot(Scene):
    def construct(self):
        # Mu symbol as the body of the bot
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
        cloud_text = Tex("Imagine n equal vectors", 
                         "acting at a point")
        cloud_text.arrange(DOWN).scale(0.6).move_to(cloud.get_center() + 0.5*UR )
        cloud_text1 = Tex("What is the sum of", 
                          "all these vectors ?")
        cloud_text1.arrange(DOWN).scale(0.6).move_to(cloud.get_center() + 0.5*UR)
        cloud_text2 = Tex("Symmetrical Arrangement !").scale(0.6).move_to(cloud.get_center() + 0.5*UR)
        cloud_text3 = Tex("Euler's Formula").scale(0.6).move_to(cloud.get_center() + 0.5*UR)
        cloud_text4 = Tex("Connection between",
                          "maths and physics").arrange(DOWN).scale(0.6).move_to(cloud.get_center() + 0.5*UR)


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

        self.play(ReplacementTransform(cloud_text2,cloud_text3))
        self.play(Transform(mu_bot_thinking, mu_bot_happy), run_time=1)
        # Blinking Animation
        self.play(blink(), run_time=0.5)
        self.wait(0.5)
        self.play(blink(), run_time=0.5)
        self.wait(2)

        self.play(ReplacementTransform(cloud_text3,cloud_text4))
        self.play(Transform(mu_bot_thinking, mu_bot_happy), run_time=1)
        # Blinking Animation
        self.play(blink(), run_time=0.5)
        self.wait(0.5)
        self.play(blink(), run_time=0.5)
        self.wait(2)

       

class ChargedRing(Scene):
    def construct(self):
        title = Text("What's the electric field at the center ?", gradient=[BLUE,GREEN]).scale(0.7).to_edge(UP)
        # Create a ring
        ring_radius = 2
        ring_center = LEFT * 3
        ring = Circle(radius=ring_radius, color=BLUE, stroke_width=12).shift(ring_center)
        
        # Add uniformly distributed "+" signs for the positive charge
        num_charges = 30  # Number of charges
        charges = VGroup()
        for i in range(num_charges):
            angle = i * 2 * PI / num_charges
            charge = MathTex(r"\boldsymbol{+}", color=RED,
                             stroke_width = 3).scale(0.6)
            charge.move_to(ring_center + np.array([np.cos(angle), np.sin(angle), 0]) * ring_radius)
            charges.add(charge)

        # Add segments to represent infinitesimal charge elements dQ
        num_segments = 20  # Number of segments
        gap_factor = 0.6  # This will make each segment occupy 60% of its allocated angle
        segments = VGroup()
        e_field_vectors = VGroup()  # Group for electric field vectors
        highlighted_segments = VGroup()  # Group for highlighted segments
        
        # Create center point
        center_dot = Dot(ring_center, color=WHITE)
        
        # Create all segments first
        for i in range(num_segments):
            segment_angle = 2 * PI / num_segments  # Total angle allocated for each segment
            actual_segment_angle = segment_angle * gap_factor  # Actual angle of the segment
            
            # Calculate the start and mid angles correctly
            start_angle = i * segment_angle + (segment_angle - actual_segment_angle) / 2
            mid_angle = start_angle + actual_segment_angle / 2  # This is the actual center of the segment
            
            # Create regular segment
            segment = Arc(
                radius=ring_radius,
                start_angle=start_angle,
                angle=actual_segment_angle,
                color=YELLOW,
                stroke_width=10,
            ).shift(ring_center)
            segments.add(segment)
            
            # Create highlighted version of the segment
            highlighted_segment = Arc(
                radius=ring_radius,
                start_angle=start_angle,
                angle=actual_segment_angle,
                color=RED,
                stroke_width=12,
            ).shift(ring_center)
            highlighted_segments.add(highlighted_segment)
            
            # Create electric field vector for each segment using the corrected mid_angle
            vector_end = ring_center + np.array([-0.7*ring_radius * np.cos(mid_angle), -0.7*ring_radius * np.sin(mid_angle), 0])
            

            e_field = Arrow(
                ring_center,  # Start from center
                vector_end,  # Point towards the middle of the actual segment
                buff=0,
                color=RED,
                max_tip_length_to_length_ratio=0.15
            )
            e_field_vectors.add(e_field)

        # Create dQ label for the first segment
        first_segment_angle = 2 * PI / num_segments
        first_actual_angle = first_segment_angle * gap_factor
        first_start_angle = (first_segment_angle - first_actual_angle) / 2
        first_mid_angle = first_start_angle + first_actual_angle / 2
        
        dq_label = MathTex("dQ", color=YELLOW).scale(0.7)
        dq_label.move_to(ring_center + np.array([1.2 * ring_radius * np.cos(first_mid_angle), 1.2 * ring_radius * np.sin(first_mid_angle), 0]))

        # Display the ring and charges
        self.play(Create(ring))
        self.play(FadeIn(charges))
        self.wait(1)
        self.play(Write(title),Create(center_dot))
        self.wait(2)
        # Show all segments
        self.play(Create(segments), run_time=2)
        self.wait(1)
        
        self.play(Write(dq_label))
        
        self.play(
            Transform(segments[0], highlighted_segments[0]),
            Write(e_field_vectors[0]),
            run_time=0.5
        )
       
        # Formula for dE
        formula = MathTex(r"|d\vec{E}| = \frac{k_e \cdot dQ}{r^2}").scale(0.8)
        formula.move_to(2 * RIGHT + UP)
        
        # Add explanation text
        explanation = Tex(
            r"where, $k_e$ = Coulomb's constant\\",
            r"$dQ$ = magnitude of charge element\\",
            r"$r$ = distance of center from the charge element"
        ).scale(0.6)
        explanation.arrange(DOWN, aligned_edge=LEFT)
        explanation.move_to(0.5 * DOWN + 3 * RIGHT)
        
        self.play(Write(formula))
        self.play(Write(explanation))

        # Show electric field contributions one by one
        for i in range(1, 5):
            self.play(
                Transform(segments[i], highlighted_segments[i]),
                Write(e_field_vectors[i]),
                run_time=0.5
            )
            self.wait(1)
        
        self.play(
            Transform(segments[5:], highlighted_segments[5:]),
            Write(e_field_vectors[5:]),
            run_time=0.5
        )
        self.wait(2)

                # Now illustrate diametrically opposite dQ and their electric fields
        # Indicate pairs of opposite electric field vectors
        for i in range(num_segments // 2):  # Loop through pairs of opposite segments
            self.play(
                Indicate(VGroup(e_field_vectors[i], e_field_vectors[i + num_segments // 2])),
                run_time=1
            )
        self.wait(2)
            
class DChargedRing(Scene):
    def construct(self):
        
        # Ring parameters
        ring_radius = 1.2
        gap_between_rings = 4  # Distance between rings
        ring_center_top = LEFT * 3.5 + UP * 1.5  # Center of the top row of rings
        ring_center_bottom = LEFT * 3.5 + DOWN * 2.5  # Center of the bottom row of rings
        
        # Number of charges on the rings (odd top, even bottom)
        num_charges_top = [3, 5, 7]  # Odd number of charges on top rings
        num_charges_bottom = [4, 6, 8]  # Even number of charges on bottom rings
        
        # Groups for charges, electric field vectors, and rings
        charges_top = VGroup()
        charges_bottom = VGroup()
        e_field_vectors_top = VGroup()
        e_field_vectors_bottom = VGroup()
        rings = VGroup()
        charge_labels_top = VGroup()  # To display the number of charges on top of each ring
        charge_labels_bottom = VGroup()  # To display the number of charges on top of each ring

        # Create rings and charges for the top row
        for j, num_charges in enumerate(num_charges_top):
            ring = Circle(radius=ring_radius, color=BLUE).shift(ring_center_top + RIGHT * j * gap_between_rings)
            rings.add(ring)

            # Label the number of charges
            charge_label = MathTex(f"n = {num_charges}", color=WHITE).scale(0.6)
            charge_label.next_to(ring,UP)
            charge_labels_top.add(charge_label)

            for i in range(num_charges):
                angle = i * 2 * PI / num_charges
                charge = MathTex(r"\boldsymbol{+}", color=RED, stroke_width=2).scale(0.6)
                charge.move_to(ring_center_top + np.array([np.cos(angle), np.sin(angle), 0]) * ring_radius + RIGHT * j * gap_between_rings)
                charges_top.add(charge)
                
                # Electric field vector for each charge
                vector_end = ring_center_top + np.array([0.7 * ring_radius * np.cos(angle), 0.7 * ring_radius * np.sin(angle), 0]) + RIGHT * j * gap_between_rings
                e_field = Arrow(ring_center_top + RIGHT * j * gap_between_rings, vector_end, buff=0, color=RED, max_tip_length_to_length_ratio=0.15)
                e_field_vectors_top.add(e_field)

        # Create rings and charges for the bottom row
        for j, num_charges in enumerate(num_charges_bottom):
            ring = Circle(radius=ring_radius, color=BLUE).shift(ring_center_bottom + RIGHT * j * gap_between_rings)
            rings.add(ring)

            # Label the number of charges
            charge_label = MathTex(f"n = {num_charges}", color=WHITE).scale(0.6)
            charge_label.next_to(ring,UP)
            charge_labels_bottom.add(charge_label)

            for i in range(num_charges):
                angle = i * 2 * PI / num_charges
                charge = MathTex(r"\boldsymbol{+}", color=RED, stroke_width=2).scale(0.6)
                charge.move_to(ring_center_bottom + np.array([np.cos(angle), np.sin(angle), 0]) * ring_radius + RIGHT * j * gap_between_rings)
                charges_bottom.add(charge)
                
                # Electric field vector for each charge
                vector_end = ring_center_bottom + np.array([0.7 * ring_radius * np.cos(angle), 0.7 * ring_radius * np.sin(angle), 0]) + RIGHT * j * gap_between_rings
                e_field = Arrow(ring_center_bottom + RIGHT * j * gap_between_rings, vector_end, buff=0, color=RED, max_tip_length_to_length_ratio=0.15)
                e_field_vectors_bottom.add(e_field)

        # Display the rings, charges, and labels
        self.play(Create(rings))
        self.play(FadeIn(charges_top), FadeIn(charges_bottom))
        self.play(Write(charge_labels_top), Write(charge_labels_bottom))
        self.wait(1)
        
        # Show electric field vectors for the top charges (odd charges)
        self.play(Create(e_field_vectors_bottom), run_time=3)
        self.wait(1)

        # Show electric field vectors for the bottom charges (even charges)
        self.play(Create(e_field_vectors_top), run_time=3)
        self.wait(1)