import gradio as gr
import subprocess
import ollama

def get_installed_models():
    result = subprocess.run(["ollama", "list"], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split('\n')[1:]  # Skip the header
    models = [line.split()[0] for line in lines]
    return models

model_names = get_installed_models()


def test_model_response(model_name, prompt):
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Error calling model: {e}"

with gr.Blocks() as demo:
    gr.Markdown("### 🔍 Test Ollama Model Response via Gradio")

    model_dropdown = gr.Dropdown(choices=model_names, label="Select Model")
    prompt_input = gr.Textbox(label="Prompt", value="What is 2 + 2?")
    output = gr.Textbox(label="Model Output", lines=4)

    run_button = gr.Button("Test Model")

    run_button.click(test_model_response, inputs=[model_dropdown, prompt_input], outputs=output)

demo.launch()