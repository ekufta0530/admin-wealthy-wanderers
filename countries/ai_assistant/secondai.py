import openai
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# List of countries to update
countries = [
    "Estonia", "Croatia", "Germany", "Portugal", "Spain"
]

# Template for the JSON document
template = {
    "country_name": "",
    "country_code": "",
    "capital": "",
    "display": True,
    "currency": "",
    "anchor_country": False,
    "has_nomad_visa": False,
    "schengen_zone": False,
    "in_european_union": False,
    "cost_of_living_index": 0.0,
    "cost_of_living_lvl": "$$",
    "practical_tips": {
        "financial_benefits": [],
        "lifestyle_benefits": [],
        "additional_benefits": []
    },
    "key_consideration": "",
    "best_for": [],
    "action_comment": "",
    "tagline": "",
    "image": "",
    "tax_residency_trigger": 183,
    "tax_residency_trigger_details": "",
    "country_standard_taxes": {
        "tax_currency": "",
        "employees": {
            "income_tax": [
                {
                    "min_income_range": 0,
                    "max_income_range": 100000,
                    "rate_pct": 5
                },
                {
                    "min_income_range": 100001,
                    "max_income_range": 200000,
                    "rate_pct": 10
                }
            ],
            "social_security": [
                {
                    "min_income_range": 0,
                    "max_income_range": 100000,
                    "rate_pct": 5
                },
                {
                    "min_income_range": 100001,
                    "max_income_range": 200000,
                    "rate_pct": 10
                }
            ]
        },
        "contractors": {
            "income_tax": [],
            "social_security": []
        },
        "retirees": {
            "income_tax": [],
            "social_security": []
        }
    },
    "visas": []
}

# Function to get tax information for a country using OpenAI API
def get_tax_information(country):
    prompt = f"""
    Provide detailed tax information for {country}, including income tax and social security rates for employees, contractors, and retirees. 
    Format it as a JSON document with the following structure paying special attention to how the tax brackets are structured with min_income_range, max_income_range, and rate_pct. I provided an example in income tax and social security tax for guidance. 
    {json.dumps(template, indent=4)}
    """
    
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": prompt}
      ],
      max_tokens=1500,
      temperature=0
    )
    
    return response.choices[0].message['content'].strip()

# Dictionary to hold the JSON documents for all countries
country_data = {}

# Loop through the list of countries and get the tax information
for country in countries:
    print(f"Processing {country}...")
    country_info = get_tax_information(country)
    try:
        country_data[country] = json.loads(country_info)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON for {country}")
        continue

# Save the JSON documents to a file locally
with open('country_tax_information.json', 'w') as outfile:
    json.dump(country_data, outfile, indent=4)

print("Country tax information has been saved to 'country_tax_information.json'")
