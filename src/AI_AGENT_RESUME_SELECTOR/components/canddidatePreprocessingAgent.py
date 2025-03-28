from src.AI_AGENT_RESUME_SELECTOR.components.entity import projectEntity
import os
import yaml
from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
import json
import re
import csv

api_key = os.environ["GROQ_API_KEY"]

path = "params.yaml"
params=yaml.safe_load(open(path))['preprocess']
print("loading YAML",path)

def convert_file_json():
    results = []
    with open(params['outputcandidate'], newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            # Keep the values as plain strings
            record = {
                "id":index,
                "skills": row.get("skills", "").strip(),
                "degree_names": row.get("degree_names", "").strip(),
                "professional_company_names": row.get("professional_company_names", "").strip(),
                "start_dates": row.get("start_dates", "").strip(),
                "end_dates": row.get("end_dates", "").strip()
            }
            results.append(record)
    with open(params['jsoncandidate'], 'w') as f:
        json.dump(results, f, indent=4)

convert_file_json()

def read_job_req()-> json:
     """this function returns the job requirment in form of json"""
     with open(params['jsonJobReq'], "r", encoding="utf-8") as f:
        data = json.load(f)
        print("job data---",data)
        return str(data)
def read_candidates()-> json:
    """this function returns list of candiated in json form"""
    with open(params['jsoncandidate'], "r", encoding="utf-8") as f:
        data = json.load(f)
        print("candidate data---",data)
        return str(data)
    
agent = Agent(
    model= Groq(
        id="llama-3.1-8b-instant", 
        api_key = api_key
    ),
  
    instructions=["""
                  very important dont add any fake data, use onlt the data provided.
                  1. load job requirments.
                  2. load all the candidates
                  3. select best candidate
                  """],
    tools=[read_candidates],
    show_tool_calls=True, 
    markdown=True
    )

#response = agent.run("add score to candidates based on skill")
#print(response.content)