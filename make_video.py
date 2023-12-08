# manim -pql make_video.py InformationScene
from manim import *

f = open("output.txt", "r")
full_output = f.read()

output_text = full_output.strip().split("\n")

title = output_text[0]
output_text = output_text[1:]


class InformationScene(Scene):
    def construct(self):
        # Create and display text objects

        text = Text(f"10 interesting facts {title}", font_size=30)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))


        text = Text("A video by AI Bhai", font_size=24)
        self.play(Write(text))
        self.wait(2)
        self.play(FadeOut(text))


        for fact in output_text:
            text = Text(fact, font_size=24)
            self.play(Write(text))
            self.wait(2)

            # delete the text object
            self.play(FadeOut(text))
            self.wait(0.5)

        # Wait for a few seconds before ending the scene
        self.wait(5)
