import cv2;
import textwrap;

def add_text_to_image(img, text, output_path):
    font = cv2.FONT_HERSHEY_DUPLEX
    wrapped_text = textwrap.wrap(text, width=24)
    x, y = 0, 0  # Starting coordinates set to 0
    font_size = 1.5
    font_thickness = 2

    for i, line in enumerate(wrapped_text):
        text_size = cv2.getTextSize(line, font, font_size, font_thickness)[0]

        # Center horizontally
        x = int((img.shape[1] - text_size[0]) / 2) + 20

        gap = text_size[1] + 40

        y = int((img.shape[0] + text_size[1]) / 2) + i * gap - 120

        cv2.putText(img, line, (x, y), font,
                    font_size,
                    (0,0,0),
                    font_thickness,
                    lineType=cv2.LINE_AA)
        
    cv2.imwrite(output_path, img)

# Example usage
sentences = [
    "The sky danced with vivid hues, a mesmerizing canvas of twilight beauty.",
    "Whispering winds embraced the night, secrets carried across moonlit realms.",
    "Neon lights flickered, city streets alive with a pulsating energy.",
    "Enigmatic shadows played hide-and-seek, elusive in the moon's glow.",
    "Time's relentless march echoed in the ticking of an antique clock.",
    "Waves whispered tales, seafoam tales spun under the watchful stars.",
    "Rainbow petals adorned fields, a kaleidoscope blooming in silence.",
    "Gravity's embrace held the world, an invisible force binding all.",
    "Echoes of laughter lingered, a symphony of joy in the air.",
    "Stellar whispers painted constellations, stories etched in celestial ink."
]


for index, sentence in enumerate(sentences):
    add_text_to_image(img = cv2.imread("background.png"), text = sentence, output_path = f"{index}.png")
