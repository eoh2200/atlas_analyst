from enum import Enum
from typing import Optional
import csv
import argparse
import os
from dotenv import load_dotenv

from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Specialization(str, Enum):
    decks = 'decks'
    sheds = 'sheds'
    fencing = 'fencing'
    greenhouses = 'greenhouses'
    formwork = 'formwork'
    general = 'general'

class Contractor(BaseModel):
    name: str
    website: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    city: Optional[str]
    state: Optional[str]
    specialization: Optional[list[Specialization]]

class ContractorList(BaseModel):
    contractors: list[Contractor]

instructions = """
You are a helpful assistant that finds contractors for a given project.
You will be given a specific county in the United States and a specific project type.
You will need to find the top 10-20 contractors operating in the county that could potentially be interested in the project.
Results may include contractors that specialize in the given project type, or general contractors that may be interested in the project.
Prioritize finding local contractors vs nationwide firms.

The results should be returned in a list of objects with the following fields:
- name: the name of the contractor / company name
- website: the website of the contractor (if available)
- phone: the phone number of the contractor (if available)
- email: the email address of the contractor (if available)
- city: the city of the contractor
- state: the state of the contractor
- specialization: list of specific project types the contractor specializes in from the following list:
    - decks
    - sheds
    - fencing
    - greenhouses
    - formwork
    - general (general contractor)

All information should be found through web search.
All information should come directly from the contractor's website or other reputable sources.
"""

def find_contractors(county: str, project_type: Specialization):
    input = f"Find the top 10-20 contractors operating in {county} that could potentially be interested in {project_type} projects."
    response = client.responses.parse(
        model="gpt-5-mini",
        tools=[{"type": "web_search"}],
        instructions=instructions,
        input=input,
        text_format=ContractorList,
    )
    return response.output_parsed

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--county", type=str, required=True)
    parser.add_argument("--project_type", type=Specialization, required=True)
    args = parser.parse_args()
    contractors = find_contractors(args.county, args.project_type)
    
    # Create CSV filename
    csv_filename = f"output/contractors_{args.county.replace(', ','_')}_{args.project_type}.csv"
    
    # Write to CSV
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["County", "State", "Company", "Phone", "Email", "Website", "Specialization"])
        # Write data rows
        for contractor in contractors.contractors:
            # Join specialization list with comma and space, or empty string if None/empty
            specialization = ", ".join(contractor.specialization) if contractor.specialization else ""
            writer.writerow([
                args.county,  # County
                contractor.state or "",  # State
                contractor.name,  # Company
                contractor.phone or "",  # Phone
                contractor.email or "",  # Email
                contractor.website or "",  # Website
                specialization  # Specialization
            ])