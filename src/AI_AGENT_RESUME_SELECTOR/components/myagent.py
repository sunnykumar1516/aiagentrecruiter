from src.AI_AGENT_RESUME_SELECTOR.components import canddidatePreprocessingAgent as ca
import gradio as gr
from src.AI_AGENT_RESUME_SELECTOR.components import jobpreprocessingAgent as ja

# Function to process the uploaded text file
def read_txt_file(file):
    if file is None:
        return "No file uploaded."
    with open(file.name, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def agent_response(text,file):
    req = extract_requirment(file)
    ca.convert_file_json()
    response = ca.agent.run(f"here is job requirments{req}. use this to select candidate. explain also why you are selecting the candidate.")
    
    return response.content,req

def extract_requirment(file):
    text = read_txt_file(file)
    response = ja.agent.run(text)
    return response.content



# Gradio interface
face = gr.Interface(
    fn=agent_response,
    inputs=[gr.Textbox(lines=2, placeholder="enter text here"),
            gr.File(file_types=[".txt"])
            ],
    outputs=["text","text"],
    title="Simple Agent",
   
)
