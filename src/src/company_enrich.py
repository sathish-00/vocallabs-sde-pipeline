import requests


def enrich_company(domain, prospeo_key):

    url = "https://api.prospeo.io/enrich-company"

    headers = {
        "Content-Type": "application/json",
        "X-KEY": prospeo_key
    }

    payload = {
        "data": {
            "company_website": domain
        }
    }

    try:

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=20
        )

        print("\n========== COMPANY ENRICH DATA ==========")

        data = response.json()

        print(data)

        print("=========================================\n")

        return data

    except Exception as e:

        print("Company enrich error:", e)

        return {}