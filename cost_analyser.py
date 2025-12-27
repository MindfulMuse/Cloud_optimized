"""
Cost Analysis and Optimization Recommendations using LLM
Analyzes cloud costs and generates money-saving recommendations
"""
import json
from collections import defaultdict
from profile_extractor import call_llm
from utils import extract_json_from_text

def analyze_costs_and_recommend(profile, billing_data):
    """
    Analyze costs and generate optimization recommendations
    
    Args:
        profile: Project profile dictionary
        billing_data: List of billing records
    
    Returns:
        dict: Complete cost optimization report
    """
    print("\n  📊 Analyzing costs...")
    
    # Calculate cost metrics
    total_cost = sum(record['cost_inr'] for record in billing_data)
    budget = profile['budget_inr_per_month']
    variance = total_cost - budget
    
    # Group costs by service
    service_costs = defaultdict(float)
    for record in billing_data:
        service_costs[record['service']] += record['cost_inr']
    
    # Identify high-cost services (top 3)
    sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
    high_cost_services = dict(sorted_services[:3])
    
    # Prepare analysis summary
    analysis_summary = {
        "total_monthly_cost": round(total_cost, 2),
        "budget": round(budget, 2),
        "budget_variance": round(variance, 2),
        "is_over_budget": total_cost > budget,
        "service_costs": {k: round(v, 2) for k, v in service_costs.items()},
        "high_cost_services": {k: round(v, 2) for k, v in high_cost_services.items()}
    }
    
    print(f"  ✓ Total Cost: ₹{total_cost:,.2f}")
    print(f"  ✓ Budget: ₹{budget:,.2f}")
    print(f"  ✓ Variance: ₹{variance:,.2f} ({'OVER' if variance > 0 else 'UNDER'} budget)")
    
    # Show top services
    print(f"\n  💰 Top Cost Services:")
    for service, cost in list(sorted_services)[:3]:
        percentage = (cost / total_cost * 100) if total_cost > 0 else 0
        print(f"    - {service}: ₹{cost:,.2f} ({percentage:.1f}%)")
    
    # Prepare data for LLM
    tech_stack_str = json.dumps(profile['tech_stack'], indent=2)
    service_costs_str = json.dumps(dict(service_costs), indent=2)
    high_cost_str = json.dumps(high_cost_services, indent=2)
    
    prompt = f"""You are a cloud cost optimization expert. Analyze costs and generate 6-10 actionable recommendations.

PROJECT INFORMATION:
- Name: {profile['name']}
- Budget: ₹{budget}/month
- Actual Cost: ₹{total_cost}/month
- Variance: ₹{variance} ({'OVER BUDGET' if variance > 0 else 'UNDER BUDGET'})

TECH STACK:
{tech_stack_str}

COST BREAKDOWN:
{service_costs_str}

HIGH COST SERVICES:
{high_cost_str}

YOUR TASK:
Generate 6-10 cost optimization recommendations that include:

1. FREE TIER OPTIONS: Services that have free tiers (AWS/Azure/GCP)
2. OPEN SOURCE: Free alternatives to paid services (self-hosted MongoDB, PostgreSQL, etc.)
3. CLOUD ALTERNATIVES: Cheaper providers (DigitalOcean, Linode vs AWS)
4. RIGHT-SIZING: Reduce instance sizes or optimize configurations
5. RESERVED INSTANCES: Long-term commitments for savings
6. ARCHITECTURE: Serverless, caching, CDN optimizations

RECOMMENDATION TYPES TO USE:
- free_tier
- open_source
- alternative_provider
- optimization
- right_sizing
- reserved_instance
- cost_effective_storage
- serverless

Each recommendation must have:
{{
  "title": "Clear, actionable title",
  "service": "Service being optimized (EC2, RDS, S3, etc.)",
  "current_cost": numeric_value,
  "potential_savings": numeric_value,
  "recommendation_type": "one of the types above",
  "description": "2-3 sentence explanation of the optimization",
  "implementation_effort": "low/medium/high",
  "risk_level": "low/medium/high",
  "steps": ["step 1", "step 2", "step 3", "..."],
  "cloud_providers": ["AWS", "Azure", "GCP", "DigitalOcean", "Self-hosted"]
}}

RULES:
1. potential_savings should be realistic (10-70% of current_cost)
2. Include at least 2 open-source alternatives
3. Include at least 2 multi-cloud options
4. Focus on HIGH COST services first
5. Be specific with implementation steps (3-5 steps per recommendation)
6. Total potential savings should be significant (30-80% of total cost)

OUTPUT FORMAT:
Return ONLY a JSON object with this EXACT structure:
{{
  "project_name": "{profile['name']}",
  "analysis": {{
    "total_monthly_cost": {total_cost},
    "budget": {budget},
    "budget_variance": {variance},
    "service_costs": {service_costs_str},
    "high_cost_services": {high_cost_str},
    "is_over_budget": {"true" if variance > 0 else "false"}
  }},
  "recommendations": [
    {{
      "title": "...",
      "service": "...",
      "current_cost": 0,
      "potential_savings": 0,
      "recommendation_type": "...",
      "description": "...",
      "implementation_effort": "...",
      "risk_level": "...",
      "steps": ["...", "...", "..."],
      "cloud_providers": ["..."]
    }}
  ],
  "summary": {{
    "total_potential_savings": 0,
    "savings_percentage": 0,
    "recommendations_count": 0,
    "high_impact_recommendations": 0
  }}
}}

CRITICAL: Return ONLY the JSON object. No markdown, no explanations, no extra text.

JSON:"""

    print("\n  🤖 Generating recommendations with AI...")
    response = call_llm(prompt, max_tokens=4500)
    
    # Extract JSON from response
    json_text = extract_json_from_text(response)
    
    try:
        report = json.loads(json_text)
        
        # Validate structure
        if 'recommendations' not in report:
            raise ValueError("Missing 'recommendations' field")
        
        if not isinstance(report['recommendations'], list):
            raise ValueError("'recommendations' must be an array")
        
        if len(report['recommendations']) < 6:
            print(f"  ⚠️ Only {len(report['recommendations'])} recommendations, expected 6-10")
        
        # Ensure analysis section is complete
        report['analysis'] = analysis_summary
        
        # Calculate summary metrics
        total_savings = sum(r.get('potential_savings', 0) for r in report['recommendations'])
        savings_pct = (total_savings / total_cost * 100) if total_cost > 0 else 0
        
        # Count high impact recommendations (>10% savings of total cost)
        high_impact = sum(1 for r in report['recommendations'] 
                         if r.get('potential_savings', 0) > total_cost * 0.1)
        
        report['summary'] = {
            "total_potential_savings": round(total_savings, 2),
            "savings_percentage": round(savings_pct, 2),
            "recommendations_count": len(report['recommendations']),
            "high_impact_recommendations": high_impact
        }
        
        # Validate each recommendation
        required_fields = ['title', 'service', 'current_cost', 'potential_savings',
                          'recommendation_type', 'description', 'implementation_effort',
                          'risk_level', 'steps', 'cloud_providers']
        
        valid_recommendations = []
        for idx, rec in enumerate(report['recommendations']):
            try:
                # Check all fields
                missing_fields = [f for f in required_fields if f not in rec]
                if missing_fields:
                    print(f"  ⚠️ Recommendation {idx+1} missing fields: {missing_fields}, skipping")
                    continue
                
                # Ensure numeric values
                if not isinstance(rec['current_cost'], (int, float)):
                    rec['current_cost'] = float(rec['current_cost'])
                
                if not isinstance(rec['potential_savings'], (int, float)):
                    rec['potential_savings'] = float(rec['potential_savings'])
                
                # Ensure arrays
                if not isinstance(rec['steps'], list):
                    rec['steps'] = [rec['steps']]
                
                if not isinstance(rec['cloud_providers'], list):
                    rec['cloud_providers'] = [rec['cloud_providers']]
                
                valid_recommendations.append(rec)
                
            except Exception as e:
                print(f"  ⚠️ Error validating recommendation {idx+1}: {str(e)}, skipping")
                continue
        
        report['recommendations'] = valid_recommendations
        report['summary']['recommendations_count'] = len(valid_recommendations)
        
        if len(valid_recommendations) < 6:
            print(f"  ⚠️ Only {len(valid_recommendations)} valid recommendations")
        
        print(f"\n  ✅ Generated {len(valid_recommendations)} recommendations")
        print(f"  ✅ Total Potential Savings: ₹{total_savings:,.2f} ({savings_pct:.1f}%)")
        
        return report
        
    except json.JSONDecodeError as e:
        print(f"\n❌ Failed to parse recommendations as JSON")
        print(f"Error: {str(e)}")
        print(f"\nLLM Response (first 500 chars):\n{response[:500]}")
        print(f"\nExtracted JSON (first 500 chars):\n{json_text[:500]}")
        raise ValueError(f"Failed to parse recommendations as JSON: {str(e)}")
        
    except Exception as e:
        print(f"\n❌ Error processing recommendations")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise ValueError(f"Error processing recommendations: {str(e)}")

def calculate_cost_metrics(billing_data):
    """
    Calculate detailed cost metrics
    
    Args:
        billing_data: List of billing records
    
    Returns:
        dict: Cost metrics and statistics
    """
    if not billing_data:
        return {
            'total_cost': 0,
            'service_costs': {},
            'region_costs': {},
            'record_count': 0
        }
    
    total_cost = sum(r['cost_inr'] for r in billing_data)
    
    # Group by service
    service_costs = defaultdict(float)
    for record in billing_data:
        service_costs[record['service']] += record['cost_inr']
    
    # Group by region
    region_costs = defaultdict(float)
    for record in billing_data:
        region_costs[record['region']] += record['cost_inr']
    
    # Sort by cost
    sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
    sorted_regions = sorted(region_costs.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'total_cost': round(total_cost, 2),
        'service_costs': dict(service_costs),
        'region_costs': dict(region_costs),
        'top_services': sorted_services[:5],
        'top_regions': sorted_regions[:3],
        'record_count': len(billing_data)
    }

if __name__ == "__main__":
    # Test the module
    print("Testing Cost Analyzer...")
    
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
        "non_functional_requirements": ["high availability"]
    }
    
    test_billing = [
        {"service": "EC2", "cost_inr": 1800},
        {"service": "RDS", "cost_inr": 1200},
        {"service": "S3", "cost_inr": 600},
        {"service": "CloudFront", "cost_inr": 800},
        {"service": "Route53", "cost_inr": 200}
    ]
    
    try:
        report = analyze_costs_and_recommend(test_profile, test_billing)
        print("\n✅ Cost analysis successful!")
        print(f"\nRecommendations: {len(report['recommendations'])}")
        print(f"Total Savings: ₹{report['summary']['total_potential_savings']:,.2f}")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")