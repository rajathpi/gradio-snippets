import gradio as gr
import PyPDF2
import subprocess
from io import BytesIO

# Placeholder for actual model inference logic
import subprocess

def query_model(model_name, context, question):
    prompt = f"Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr}"


# Extract text from PDF using a file-like object
def extract_text_from_pdf(pdf_bytes):
    pdf_stream = BytesIO(pdf_bytes)
    reader = PyPDF2.PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Main QA function
def ask_question(pdf_file, question, model_name):
    if pdf_file is None or question.strip() == "":
        return "Please upload a PDF and enter a question."
    
    text = extract_text_from_pdf(pdf_file)
    if not text.strip():
        return "Could not extract text from the PDF."

    # Run model inference
    answer = query_model(model_name, text, question)
    return answer

# Fetch available models using Ollama
def get_installed_models():
    try:
        result = subprocess.run(["ollama", "list"], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        models = [line.split()[0] for line in lines]
        return models if models else ["No models found"]
    except Exception as e:
        return [f"Error fetching models: {str(e)}"]

model_names = get_installed_models()

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📄 Ask Questions About Your PDF")
    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", type="binary")
        model_choice = gr.Dropdown(choices=model_names, label="Choose Model")
    question_input = gr.Textbox(label="Enter your question")
    output = gr.Textbox(label="Answer", lines=4)

    submit_btn = gr.Button("Get Answer")
    submit_btn.click(ask_question, inputs=[pdf_input, question_input, model_choice], outputs=output)

demo.launch()
