"""Draw a mathematical expression and see its transcription and result."""

import gradio as gr
from PIL import Image

from math_solver import solve_expression
from preprocessing import prepare_image
from recognition import recognize


def recognize_and_solve(drawing):
    if drawing is None:
        return "", "Please draw an expression first."

    # Gradio's sketchpad returns a background and composited drawing.
    image = drawing.get("composite") if isinstance(drawing, dict) else drawing
    if image is None:
        return "", "Please draw an expression first."

    try:
        image = Image.fromarray(image) if not isinstance(image, Image.Image) else image
        if image.mode == "RGBA":
            background = Image.new("RGBA", image.size, "white")
            image = Image.alpha_composite(background, image).convert("RGB")
        prepared = prepare_image(image)
        prediction = recognize(prepared)
    except Exception as exc:
        return "", f"Recognition failed: {exc}"

    try:
        answer = solve_expression(prediction)
        return prediction, answer
    except ValueError:
        return prediction, "Not supported by the arithmetic solver. Check the transcription."


with gr.Blocks(title="Advanced Mathematical Vision AI") as demo:
    gr.Markdown("# Advanced Mathematical Vision AI")
    gr.Markdown("Write an expression, then select **Recognise and solve**. Verify the recognised text before relying on the answer.")

    drawing = gr.Sketchpad(
        label="Handwritten expression",
        type="pil",
        canvas_size=(800, 280),
        brush=gr.Brush(colors=["#000000"], default_color="#000000"),
    )
    run = gr.Button("Recognise and solve", variant="primary")
    with gr.Row():
        transcription = gr.Textbox(label="Recognised expression")
        result = gr.Textbox(label="Calculated answer")
    run.click(recognize_and_solve, inputs=drawing, outputs=[transcription, result])

if __name__ == "__main__":
    demo.launch()
