"""Prepare a canvas image for the handwriting recognition model."""

import numpy as np
from PIL import Image, ImageOps


def prepare_image(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    grayscale = np.asarray(image.convert("L"))
    ys, xs = np.where(grayscale < 245)
    if len(xs) == 0:
        raise ValueError("Draw an expression before recognising it.")

    margin = 15
    bounds = (
        max(0, int(xs.min()) - margin),
        max(0, int(ys.min()) - margin),
        min(image.width, int(xs.max()) + margin + 1),
        min(image.height, int(ys.max()) + margin + 1),
    )
    return ImageOps.expand(image.crop(bounds), border=24, fill="white")
