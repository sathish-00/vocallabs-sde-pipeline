import requests

def fetch_companies(domain, apollo_key, count=3):
    """
    Stage 1:
    Accept a company domain and create a clean company record.

    The assignment only requires the pipeline to start from a
    single company domain and pass data automatically to the
    next stages.
    """

    print(f"\n--- Starting Stage 1: Processing company domain: '{domain}' ---")

    company_name = domain.split('.')[0].capitalize() if '.' in domain else domain

    companies = [{
        "name": company_name,
        "domain": domain
    }]

    print("DEBUG STAGE1 OUTPUT:", companies)
    print(f"Stage 1 completed successfully. Found {len(companies)} company record(s).")

    return companies 