"""Cut course pictures out of the felt 'Psych and Otic' film.

    .venv/bin/python scripts/make_images.py [path/to/psych-and-otic]
"""
import pathlib, subprocess, sys, tempfile
from PIL import Image, ImageDraw

FILM = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "~/Documents/felt/films/psych-and-otic").expanduser()
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
MAX = 640

# Character turnaround stills on flat beige: key out the background.
CUTOUTS = {
    "psych": "stills/c-psych.png",
    "psych-up": "stills/c-psych-up.png",
    "psych-smash": "stills/c-psych-smash.png",
    "otic": "stills/c-otic.png",
    "propellor-boy": "stills/c-pb2.png",
    "unicorn-boy": "stills/c-ub.png",
}
# Comic stickers: already transparent.
STICKERS = {k: f"assets/{k}.png" for k in ["whudonk", "mooo", "ohno", "poof", "shloop", "whoosh", "clink"]}
STICKERS["huh"] = "assets/huh1.png"
# Scene frames from the film: (time s, crop box in the 960x720 frame).
FRAMES = {
    "mender": (22.0, (600, 160, 900, 620)),
    "scribble": (38.0, (480, 0, 960, 600)),
    "jar": (57.5, (160, 140, 760, 720)),
    "woods": (61.8, (60, 40, 940, 610)),
}


def shrink(im):
    im.thumbnail((MAX, MAX))
    return im


def cutout(path):
    im = Image.open(path).convert("RGBA")
    bg = im.getpixel((2, 2))
    # Flood-fill from each corner with a magenta marker, then make it transparent.
    key = (255, 0, 255, 255)
    for xy in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]:
        if im.getpixel(xy)[:3] == bg[:3]:
            ImageDraw.floodfill(im, xy, key, thresh=18)
    px = [(0, 0, 0, 0) if p == key else p for p in im.getdata()]
    im.putdata(px)
    box = im.getbbox()
    pad = 12
    im = im.crop((max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, im.width), min(box[3] + pad, im.height)))
    return shrink(im)


def frame(t, box):
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "f.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(FILM / "psych-and-otic.mp4"),
                        "-frames:v", "1", str(p)], check=True)
        return shrink(Image.open(p).convert("RGB").crop(box))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rel in CUTOUTS.items():
        cutout(FILM / rel).save(OUT / f"{name}.png", optimize=True)
    for name, rel in STICKERS.items():
        shrink(Image.open(FILM / rel).convert("RGBA")).save(OUT / f"{name}.png", optimize=True)
    for name, (t, box) in FRAMES.items():
        frame(t, box).save(OUT / f"{name}.png", optimize=True)
    print("wrote", len(list(OUT.glob("*.png"))), "images to", OUT)


if __name__ == "__main__":
    main()
