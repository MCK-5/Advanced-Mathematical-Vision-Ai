"""Load the MathWriting TrOCR checkpoint and recognise an image."""

from functools import lru_cache

import torch
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

MODEL_ID = "us4/trocr-mathwriting"


@lru_cache(maxsize=1)
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = TrOCRProcessor.from_pretrained(MODEL_ID)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_ID)
    model.to(device)
    model.eval()
    return processor, model, device


def recognize(image: Image.Image) -> str:
    processor, model, device = load_model()
    dtype = next(model.parameters()).dtype
    pixels = processor(images=image, return_tensors="pt").pixel_values
    pixels = pixels.to(device=device, dtype=dtype)
    with torch.inference_mode():
        tokens = model.generate(pixels, max_new_tokens=128, num_beams=4)
    return processor.batch_decode(tokens, skip_special_tokens=True)[0].strip()
