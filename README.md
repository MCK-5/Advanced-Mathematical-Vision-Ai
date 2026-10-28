# Advanced Mathematical Vision AI

A Python application for recognising handwritten mathematical expressions and calculating basic arithmetic results.

The recognition component uses the public [us4/trocr-mathwriting](https://huggingface.co/us4/trocr-mathwriting) checkpoint. It is separate from the earlier HASYv2 CNN and pix2tex experiments, which are preserved in the development notebook.

## Features

- Draw mathematical expressions in a browser-based canvas.
- Transcribe handwriting with a pretrained TrOCR model.
- Evaluate supported arithmetic without Python `eval()`.
- Show the recognised expression alongside its calculated result.

## Run locally

Python 3.10+ is recommended. A GPU is helpful but not required.

```bash
python -m venv .venv
# Activate your virtual environment, then:
pip install -r requirements.txt
python app.py
```

The first run downloads model weights from Hugging Face (approximately 2.1 GB). Allow time and disk space for the download. Model files are not committed to this repository.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project files

- `app.py`: drawing interface and application flow
- `recognition.py`: pretrained model loading and inference
- `preprocessing.py`: crop and padding for canvas drawings
- `math_solver.py`: restricted arithmetic evaluator
- `tests/`: arithmetic unit tests
- `notebooks/`: original development notebook, including HASYv2 and pix2tex experiments
- `screenshots/`: real demonstration screenshots from Colab

## Current limitations

Recognition is not guaranteed for every writing style or mathematical expression. The solver currently handles **numeric arithmetic only**, not algebraic equations, integrals, fractions written in two dimensions, or full LaTeX. Always check the recognised expression before using the answer.

## Development background

The project began with a 369-class HASYv2 symbol classifier. Subsequent experiments evaluated pix2tex on mathematical expressions and then adopted a MathWriting-trained TrOCR checkpoint for end-to-end handwritten expression recognition. The original Colab notebook documents this progression.

## Model attribution

The pretrained handwriting recognition checkpoint belongs to its original authors. Review its model card and licence before commercial distribution. This repository does not redistribute the checkpoint.
