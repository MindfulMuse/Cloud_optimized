
"""
Project Profile Extraction using LLM
Extracts structured project profiles from free-form text descriptions
"""
import os
import json
import requests
import time
from groq import Groq
from dotenv import load_dotenv
from utils import extract_json_from_text

# Load environment variables
load_dotenv()

# List of models to try (in order of preference)
# AVAILABLE_MODELS = [
#     "google/flan-t5-small",
#     "google/flan-t5-base"
# ]


def call_llm(prompt, max_tokens=1000, retries=2):
    """
    Call Groq LLM with retry logic
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    client = Groq(api_key=api_key)

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                # model="meta-llama/llama-4-scout-17b-16e-instruct",
                model="llama-3.1-8b-instant" , # faster and supported
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"⚠️ Groq error (attempt {attempt + 1}/{retries}): {str(e)}")
            if attempt == retries - 1:
                raise
            time.sleep(2)

def extract_project_profile(description):
    """
    Extract structured project profile from free-form text using LLM
    
    Args:
        description: Free-form project description text
    
    Returns:
        dict: Structured project profile with name, budget, tech stack, etc.
    """
    prompt = f"""Extract project information and return ONLY a JSON object:

Project Description: {description}

Return this exact JSON structure:
{{
  "name": "project name",
  "budget_inr_per_month": 5000,
  "description": "brief summary",
  "tech_stack": {{
    "frontend": "react or null",
    "backend": "nodejs or null",
    "database": "mongodb or null",
    "proxy": "nginx or null",
    "hosting": "aws or null"
  }},
  "non_functional_requirements": ["scalability", "availability"]
}}

Rules:
- Extract budget in INR (estimate if not specified: small=3000, medium=8000, large=20000)
- List all technologies mentioned
- Include requirements like scalability, high availability, security
- Return ONLY valid JSON, no explanations

JSON:"""

    try:
        response = call_llm(prompt, max_tokens=1500)
        
        # Extract JSON from response
        json_text = extract_json_from_text(response)
        
        profile = json.loads(json_text)
        
        # Validate and fix required fields
        if 'name' not in profile:
            profile['name'] = "Cloud Project"
        
        if 'budget_inr_per_month' not in profile:
            profile['budget_inr_per_month'] = 5000
        else:
            profile['budget_inr_per_month'] = float(str(profile['budget_inr_per_month']).replace(',', ''))
        
        if 'description' not in profile:
            profile['description'] = description[:100]
        
        if 'tech_stack' not in profile or not isinstance(profile['tech_stack'], dict):
            profile['tech_stack'] = {
                "frontend": None,
                "backend": None,
                "database": None,
                "proxy": None,
                "hosting": None
            }
        
        if 'non_functional_requirements' not in profile:
            profile['non_functional_requirements'] = []
        elif not isinstance(profile['non_functional_requirements'], list):
            profile['non_functional_requirements'] = [profile['non_functional_requirements']]
        
        # Normalize tech stack values
        for key, value in profile['tech_stack'].items():
            if isinstance(value, str):
                profile['tech_stack'][key] = value.lower()
        
        print(f"  ✓ Extracted profile for: {profile['name']}")
        print(f"  ✓ Budget: ₹{profile['budget_inr_per_month']:,.2f}/month")
        
        return profile
        
    except json.JSONDecodeError as e:
        print(f"\n⚠️ Could not parse JSON from LLM. Creating profile from description...")
        # Fallback: Create basic profile from description
        return create_fallback_profile(description)
        
    except Exception as e:
        print(f"\n⚠️ Error: {str(e)}")
        print(f"Creating fallback profile from description...")
        return create_fallback_profile(description)

def create_fallback_profile(description):
    """
    Create a basic profile when LLM fails
    
    Args:
        description: Project description text
    
    Returns:
        dict: Basic project profile
    """
    desc_lower = description.lower()
    
    # Extract budget
    budget = 5000  # Default
    if 'budget' in desc_lower:
        import re
        budget_match = re.search(r'(\d+)\s*(?:rupees|inr|rs)', desc_lower)
        if budget_match:
            budget = int(budget_match.group(1))
    
    # Detect technologies
    tech_stack = {
        "frontend": None,
        "backend": None,
        "database": None,
        "proxy": None,
        "hosting": None
    }
    
    if 'react' in desc_lower:
        tech_stack['frontend'] = 'react'
    elif 'angular' in desc_lower:
        tech_stack['frontend'] = 'angular'
    elif 'vue' in desc_lower:
        tech_stack['frontend'] = 'vue'
    
    if 'node' in desc_lower or 'nodejs' in desc_lower:
        tech_stack['backend'] = 'nodejs'
    elif 'python' in desc_lower or 'django' in desc_lower:
        tech_stack['backend'] = 'python'
    elif 'java' in desc_lower:
        tech_stack['backend'] = 'java'
    
    if 'mongodb' in desc_lower or 'mongo' in desc_lower:
        tech_stack['database'] = 'mongodb'
    elif 'postgres' in desc_lower or 'postgresql' in desc_lower:
        tech_stack['database'] = 'postgresql'
    elif 'mysql' in desc_lower:
        tech_stack['database'] = 'mysql'
    
    if 'nginx' in desc_lower:
        tech_stack['proxy'] = 'nginx'
    elif 'apache' in desc_lower:
        tech_stack['proxy'] = 'apache'
    
    if 'aws' in desc_lower:
        tech_stack['hosting'] = 'aws'
    elif 'azure' in desc_lower:
        tech_stack['hosting'] = 'azure'
    elif 'gcp' in desc_lower or 'google cloud' in desc_lower:
        tech_stack['hosting'] = 'gcp'
    
    # Detect requirements
    requirements = []
    if 'scalab' in desc_lower:
        requirements.append('scalability')
    if 'availab' in desc_lower:
        requirements.append('high availability')
    if 'security' in desc_lower:
        requirements.append('security')
    
    profile = {
        "name": "Cloud Application",
        "budget_inr_per_month": budget,
        "description": description[:200],
        "tech_stack": tech_stack,
        "non_functional_requirements": requirements
    }
    
    print(f"  ✓ Created fallback profile")
    print(f"  ✓ Budget: ₹{budget:,.2f}/month")
    
    return profile

if __name__ == "__main__":
    print("Testing Profile Extractor...")
    
    test_description = """
    I want to build an e-commerce platform for selling handmade crafts. 
    The frontend will use React, backend with Node.js and Express, 
    MongoDB for the database, and Nginx as reverse proxy. 
    I plan to host on AWS. My budget is around 8000 rupees per month.
    The system needs to be highly available and scalable.
    """
    
    try:
        profile = extract_project_profile(test_description)
        print("\n✅ Profile extraction successful!")
        print(json.dumps(profile, indent=2))
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")