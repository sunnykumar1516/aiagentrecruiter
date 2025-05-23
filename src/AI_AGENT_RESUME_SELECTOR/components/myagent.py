from src.AI_AGENT_RESUME_SELECTOR.components import canddidatePreprocessingAgent as ca
import gradio as gr
from src.AI_AGENT_RESUME_SELECTOR.components import jobpreprocessingAgent as ja
import os

#--- setting api key----
api_key = ""
def set_api_key(api_key):
    os.environ["GROQ_API_KEY"] = api_key 
    return "API Key saved successfully!"

# Function to process the uploaded text file
def read_txt_file(file):
    if file is None:
        return "No file uploaded."
    with open(file.name, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def agent_response(text,selection,file):
    print(">>>>>>>>>updated key:--",os.environ.get("GROQ_API_KEY"))
    try:
        req = ""
        print(">>>>>>>selected option:",selection)
        if selection == "use default job requirments":
            req = ca.read_job_req()
            req = str(req)
        elif selection == "upload my custom job requirments" :
            req = extract_requirment(file)
        else:
            return "no file uploaed","no file uploaded"

        ca.convert_file_json()
        response = ca.agent.run(f"here is job requirments{req}.Here is what i want : {text}")
        resp = f"here is reponse:-------- {str(response.content)}"
        return resp,selection + req
    except Exception:
        return "error occured","error occured"

def extract_requirment(file):
    text = read_txt_file(file)
    text = str(text)
    response = ja.agent.run(text)
    return response.content


''''
# Gradio interface
face = gr.Interface(
    fn=agent_response,
    inputs=[gr.Textbox(lines=2, placeholder="enter text here"),
            gr.Radio(choices=["use default job requirments","upload my custom job requirments"], label="Pick one", value="use default job requirments"),
            gr.File(file_types=[".txt"])
            ],
    outputs=[gr.Textbox(label="selected candidate"),gr.Textbox(label="skills extracted")] ,
    examples=[
        ["select the best candidate for my job requirment based on skills"],
        ["list only the id of candidates who are suitable for job"]
    ],
    title="AI Recruiter Agent",

)
'''
with gr.Blocks(title="AI Recruiter Agent") as face:

    gr.Markdown("## AI Recruiter Agent")
    gr.Markdown("### Created by [Sunny Kumar](https://www.linkedin.com/in/sunny-kumar-b232417a/)")
    with gr.Tabs():
        with gr.Tab("Main App"):
            with gr.Row():
                textbox_input = gr.Textbox(lines=2, placeholder="enter text here", label="Your Query")
                file_input = gr.File(file_types=[".txt"], label="Upload Job Requirements.")

            with gr.Row():
                radio_input = gr.Radio(
                    choices=["use default job requirments", "upload my custom job requirments"],
                    label="Pick one",
                    value="use default job requirments"
                )

            with gr.Row():
                output_candidate = gr.Textbox(label="Selected Candidate")
                output_skills = gr.Textbox(label="Skills Extracted")

            submit_button = gr.Button("Submit")

            examples = gr.Examples(
                examples=[
                    ["select the best candidate for my job requirment based on skills"],
                    ["list only the id of candidates who are suitable for job"]
                ],
                inputs=[textbox_input]
            )

            submit_button.click(
                fn=agent_response,
                inputs=[textbox_input, radio_input, file_input],
                outputs=[output_candidate, output_skills]
            )
        with gr.Tab("API"):
            gr.Markdown("## Manage groq API Keys")
            api_key_input = gr.Textbox(label="Enter API Key", type="password")
            save_btn = gr.Button("Save API Key")
            api_status = gr.Textbox(label="Status", interactive=False)
            save_btn.click(set_api_key, inputs=api_key_input, outputs=api_status)

        with gr.Tab("Image"):
            gr.Markdown("## Architecture")
            image = gr.Image(value="data/image/arch.png", label="© sunny kumar", type="filepath")

