from src.AI_AGENT_RESUME_SELECTOR.components import canddidatePreprocessingAgent as ca
import gradio as gr
from src.AI_AGENT_RESUME_SELECTOR.components import jobpreprocessingAgent as ja



def agent_response(text,file):
    req = ja.agent.run(text)
    req = str(req.content)
    ca.convert_file_json()
    response = ca.agent.run(f"here is job requirments{req}. use this to select candidate. explain also why you are selecting the candidate.")
    return response.content,req



# Gradio interface
face = gr.Interface(
    fn=agent_response,
    inputs=[gr.Textbox(lines=2, placeholder="job requirments..."),
            gr.File(file_types=[".txt"])
            ],
    outputs=["text","text"],
    title="Simple Agent",
   
)

#face.launch()