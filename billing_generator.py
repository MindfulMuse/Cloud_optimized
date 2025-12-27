"""
Synthetic Billing Data Generation using LLM
Generates realistic, budget-aware cloud billing records
"""
import json
import random
from profile_extractor import call_llm
from utils import extract_json_from_text

def generate_mock_billing(profile):
    """
    Generate realistic synthetic billing data based on project profile
    
    Args:
        profile: Project profile dictionary
    
    Returns:
        list: Array of 12-20 billing records
    """
    tech_stack_str = json.dumps(profile['tech_stack'], indent=2)
    budget = profile['budget_inr_per_month']
    
    # Determine cloud provider from tech stack
    hosting = profile['tech_stack'].get('hosting', 'aws')
    if hosting and isinstance(hosting, str):
        hosting = hosting.lower()
        if 'aws' in hosting or hosting == 'amazon':
            provider = 'AWS'
        elif 'azure' in hosting or 'microsoft' in hosting:
            provider = 'Azure'
        elif 'gcp' in hosting or 'google' in hosting:
            provider = 'GCP'
        else:
            provider = 'AWS'  # Default
    else:
        provider = 'AWS'
    
    prompt = f"""You are a cloud billing expert. Generate realistic monthly billing records for this project.

Project Details:
- Name: {profile['name']}
- Monthly Budget: ₹{budget}
- Primary Cloud Provider: {provider}
- Tech Stack:
{tech_stack_str}

Your task: Generate 12-20 billing records that represent one month of cloud usage.

Requirements:
1. Total cost should be between {budget * 0.9} and {budget * 1.3} INR (can slightly exceed budget)
2. Include diverse cloud services based on tech stack:
   - COMPUTE: EC2/Virtual Machines (for web servers, API servers, workers)
   - DATABASE: RDS, MongoDB, managed databases
   - STORAGE: S3, Blob Storage, Cloud Storage (for files, backups, static assets)
   - NETWORKING: Load Balancers, CloudFront/CDN, VPC, Data Transfer
   - MONITORING: CloudWatch, Azure Monitor, Stackdriver
   - OTHER: Lambda/Functions, SES/Email, Route53/DNS, WAF, Backup services

3. Each record MUST have these exact fields:
   - month: "2025-01" (current month)
   - service: Service name (EC2, RDS, S3, etc.)
   - resource_id: Unique identifier (e.g., "i-web-server-01", "db-mongo-prod")
   - region: Cloud region (e.g., "ap-south-1" for Mumbai, "us-east-1", "westus2")
   - usage_type: Instance type or usage category
   - usage_quantity: Number (hours for compute, GB for storage, requests for functions)
   - unit: "hours", "GB", "requests", "GB-month", etc.
   - cost_inr: Cost in Indian Rupees (numeric)
   - desc: Brief description of what this resource does

4. Make it realistic:
   - Web/API servers run 24/7 (720 hours/month)
   - Databases run continuously
   - Storage accumulates over time
   - Include load balancer, CDN for production apps
   - Add monitoring and backup services
   - Use appropriate Indian regions when possible

5. Cost distribution (approximate):
   - Compute: 35-45%
   - Database: 20-30%
   - Storage: 10-15%
   - Networking: 10-15%
   - Monitoring/Other: 5-10%

Example format:
[
  {{
    "month": "2025-01",
    "service": "EC2",
    "resource_id": "i-web-server-01",
    "region": "ap-south-1",
    "usage_type": "t3.medium Linux/UNIX",
    "usage_quantity": 720,
    "unit": "hours",
    "cost_inr": 1200,
    "desc": "Primary web server hosting React frontend"
  }},
  {{
    "month": "2025-01",
    "service": "RDS",
    "resource_id": "db-mongodb-prod",
    "region": "ap-south-1",
    "usage_type": "db.t3.small MongoDB",
    "usage_quantity": 720,
    "unit": "hours",
    "cost_inr": 900,
    "desc": "Production MongoDB database"
  }},
  {{
    "month": "2025-01",
    "service": "S3",
    "resource_id": "bucket-static-assets",
    "region": "ap-south-1",
    "usage_type": "Standard Storage",
    "usage_quantity": 50,
    "unit": "GB-month",
    "cost_inr": 150,
    "desc": "Static files and user uploads"
  }}
]

CRITICAL: Return ONLY a valid JSON array. No explanations, no markdown, no extra text.

JSON Array:"""

    print(f"  → Generating billing data for {provider}...")
    response = call_llm(prompt, max_tokens=3500)
    
    # Extract JSON from response
    json_text = extract_json_from_text(response)
    
    try:
        billing_records = json.loads(json_text)
        
        # Validate it's an array
        if not isinstance(billing_records, list):
            raise ValueError("Response is not a JSON array")
        
        # Check minimum records
        if len(billing_records) < 12:
            print(f"  ⚠️ Only generated {len(billing_records)} records, need at least 12")
            raise ValueError(f"Generated only {len(billing_records)} records, need at least 12")
        
        if len(billing_records) > 20:
            print(f"  ⚠️ Generated {len(billing_records)} records, trimming to 20")
            billing_records = billing_records[:20]
        
        # Validate each record
        required_fields = ['month', 'service', 'resource_id', 'region', 
                          'usage_type', 'usage_quantity', 'unit', 'cost_inr', 'desc']
        
        valid_records = []
        for idx, record in enumerate(billing_records):
            try:
                # Check all required fields exist
                for field in required_fields:
                    if field not in record:
                        raise ValueError(f"Record {idx} missing field: {field}")
                
                # Ensure cost is numeric and positive
                if not isinstance(record['cost_inr'], (int, float)):
                    try:
                        record['cost_inr'] = float(str(record['cost_inr']).replace(',', ''))
                    except:
                        raise ValueError(f"Record {idx} has invalid cost: {record['cost_inr']}")
                
                if record['cost_inr'] < 0:
                    raise ValueError(f"Record {idx} has negative cost")
                
                # Ensure usage_quantity is numeric
                if not isinstance(record['usage_quantity'], (int, float)):
                    try:
                        record['usage_quantity'] = float(str(record['usage_quantity']).replace(',', ''))
                    except:
                        raise ValueError(f"Record {idx} has invalid usage_quantity")
                
                valid_records.append(record)
                
            except ValueError as e:
                print(f"  ⚠️ Skipping invalid record {idx}: {str(e)}")
                continue
        
        if len(valid_records) < 12:
            raise ValueError(f"Only {len(valid_records)} valid records after validation")
        
        # Calculate total cost
        total_cost = sum(r['cost_inr'] for r in valid_records)
        
        print(f"  ✓ Generated {len(valid_records)} billing records")
        print(f"  ✓ Total monthly cost: ₹{total_cost:,.2f}")
        print(f"  ✓ Budget: ₹{budget:,.2f}")
        
        if total_cost > budget:
            print(f"  ⚠️ Over budget by ₹{total_cost - budget:,.2f}")
        else:
            print(f"  ✓ Under budget by ₹{budget - total_cost:,.2f}")
        
        # Show service breakdown
        service_costs = {}
        for record in valid_records:
            service = record['service']
            service_costs[service] = service_costs.get(service, 0) + record['cost_inr']
        
        print(f"\n  Service Breakdown:")
        for service, cost in sorted(service_costs.items(), key=lambda x: x[1], reverse=True):
            percentage = (cost / total_cost * 100) if total_cost > 0 else 0
            print(f"    - {service}: ₹{cost:,.2f} ({percentage:.1f}%)")
        
        return valid_records
        
    except json.JSONDecodeError as e:
        print(f"\n❌ Failed to parse billing data as JSON")
        print(f"Error: {str(e)}")
        print(f"\nLLM Response (first 500 chars):\n{response[:500]}")
        print(f"\nExtracted JSON text (first 500 chars):\n{json_text[:500]}")
        raise ValueError(f"Failed to parse billing data as JSON: {str(e)}")
        
    except Exception as e:
        print(f"\n❌ Error processing billing data")
        print(f"Error: {str(e)}")
        raise ValueError(f"Error processing billing data: {str(e)}")

def validate_billing_record(record):
    """
    Validate a single billing record
    
    Args:
        record: Billing record dictionary
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = {
        'month': str,
        'service': str,
        'resource_id': str,
        'region': str,
        'usage_type': str,
        'usage_quantity': (int, float),
        'unit': str,
        'cost_inr': (int, float),
        'desc': str
    }
    
    for field, expected_type in required_fields.items():
        if field not in record:
            return False, f"Missing required field: {field}"
        if not isinstance(record[field], expected_type):
            return False, f"Field '{field}' must be of type {expected_type}"
    
    # Validate numeric values
    if record['cost_inr'] < 0:
        return False, "cost_inr must be non-negative"
    
    if record['usage_quantity'] <= 0:
        return False, "usage_quantity must be positive"
    
    return True, None

def calculate_billing_summary(billing_records):
    """
    Calculate summary statistics from billing records
    
    Args:
        billing_records: List of billing records
    
    Returns:
        dict: Summary statistics
    """
    total_cost = sum(r['cost_inr'] for r in billing_records)
    
    # Group by service
    service_costs = {}
    for record in billing_records:
        service = record['service']
        service_costs[service] = service_costs.get(service, 0) + record['cost_inr']
    
    # Group by region
    region_costs = {}
    for record in billing_records:
        region = record['region']
        region_costs[region] = region_costs.get(region, 0) + record['cost_inr']
    
    return {
        'total_cost': total_cost,
        'record_count': len(billing_records),
        'service_costs': service_costs,
        'region_costs': region_costs,
        'top_service': max(service_costs.items(), key=lambda x: x[1])[0] if service_costs else None,
        'top_region': max(region_costs.items(), key=lambda x: x[1])[0] if region_costs else None
    }

if __name__ == "__main__":
    # Test the module
    print("Testing Billing Generator...")
    
    test_profile = {
        "name": "E-commerce Platform",
        "budget_inr_per_month": 5000,
        "description": "Online store for handmade crafts",
        "tech_stack": {
            "frontend": "react",
            "backend": "nodejs",
            "database": "mongodb",
            "proxy": "nginx",
            "hosting": "aws"
        },
        "non_functional_requirements": ["high availability", "scalability"]
    }
    
    try:
        billing = generate_mock_billing(test_profile)
        print("\n✅ Billing generation successful!")
        print(f"\nSample records (first 3):")
        for record in billing[:3]:
            print(json.dumps(record, indent=2))
        
        summary = calculate_billing_summary(billing)
        print(f"\n📊 Summary:")
        print(json.dumps(summary, indent=2))
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")