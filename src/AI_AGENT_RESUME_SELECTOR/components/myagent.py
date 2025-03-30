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

def agent_response(text,selection,file):
    try:
        req = ""
        print(">>>>>>>selected option:",selection)
        if selection == "use default job requirments":
            req = ca.read_job_req()
            req = str(req)
        else:
            req = extract_requirment(file)

        ca.convert_file_json()
        response = ca.agent.run(f"here is job requirments{req}.Here is what i want : {text}")
        
        return response.content,selection + req
    except Exception:
        return "error occured","error occured"

def extract_requirment(file):
    text = read_txt_file(file)
    response = ja.agent.run(text)
    return response.content



# Gradio interface
face = gr.Interface(
    fn=agent_response,
    inputs=[gr.Textbox(lines=2, placeholder="enter text here"),
            gr.Radio(choices=["use default job requirments","upload my custom job requirments"], label="Pick one", value="use default job requirments"),
            gr.File(file_types=[".txt"])
            ],
    outputs=["text","text"],
    examples=[
        ["select the best candidate for my job requirment based on skills"],
        ["list only the id of candidates who are suitable for job"]
    ],
    title="Simple Agent",
   
)
