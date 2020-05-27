import moviepy.editor as mpy
import gizeh as gz
from math import pi



BLUE = (59/255, 89/255, 152/255)

def render_text(t):
    surface = gz.Surface(640, 60, bg_color=(1, 1, 1))
    text = gz.text("Let's build together", fontfamily="Charter",
                fontsize=30, fontweight='bold', fill=BLUE, xy=(320, 40))
    text.draw(surface)
    return surface.get_npimage()

text = mpy.VideoClip(render_text, duration=10)


def draw_stars(t):
    surface = gz.Surface(640, 120, bg_color=(1, 1, 1))
    for i in range(5):
        star = gz.star(nbranches=5, radius=120*0.2,
                xy=[100*(i+1), 50], fill=(0, 1, 0),
                angle=t*pi)
        star.draw(surface)
    return surface.get_npimage()

stars = mpy.VideoClip(draw_stars, duration=10)


WHITE = (255, 255, 255)
VIDEO_SIZE = (640, 480)

video = mpy.CompositeVideoClip(
    [
        stars.set_position(
            ('center', sb_logo.size[1] + text.size[1])
        )
    ],
    size=VIDEO_SIZE).\
    on_color(
        color=WHITE,
        col_opacity=1).set_duration(10)

video.write_videofile('video_with_python.mp4', fps=10)

