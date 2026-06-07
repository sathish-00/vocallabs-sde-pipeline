import requests

def fetch_companies(keyword, apollo_key, count=3):
    print(f"\n--- Starting Stage 1: Querying Apollo for keyword: '{keyword}' ---")
    if not apollo_key:
        print("Error: Apollo API key is missing. Skipping stage.")
        return []

    url = "https://api.apollo.io/v1/organizations/search"
    headers = {
        "Content-Type": "application/json", 
        "X-Api-Key": apollo_key
    }
    
    payload = {
        "q_organization_keyword_tags": [keyword], 
        "page": 1, 
        "per_page": count
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            orgs = data.get("organizations", [])
            
            # Extract names and valid domains from the search results
            companies = []
            for o in orgs:
                name = o.get("name")
                domain = o.get("primary_domain")
                if domain:
                    companies.append({"name": name, "domain": domain})
            
            print(f"Stage 1 completed successfully. Found {len(companies)} companies.")
            return companies
            
        print(f"Apollo API returned an error status: {response.status_code}")
        
    except Exception as e:
        print(f"Network exception or timeout during Apollo search: {e}")
        
    return []