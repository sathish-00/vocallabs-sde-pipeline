import requests
import time

def hunt_leads(companies, prospeo_key):

    print("\n--- Starting Stage 2: Finding contacts via Prospeo API ---")

    if not prospeo_key:
        print("Error: Prospeo API key is missing.")
        return []

    search_url = "https://api.prospeo.io/search-person"
    enrich_url = "https://api.prospeo.io/enrich-person"

    headers = {
        "Content-Type": "application/json",
        "X-KEY": prospeo_key
    }

    leads = []

    decision_roles = [
    "founder",
    "co-founder",
    "ceo",
    "cto",
    "cio",
    "cfo",
    "chief",
    "director",
    "associate director",
    "senior director",
    "vp",
    "vice president",
    "head",
    "engineering manager",
    "product manager",
    "senior manager",
    "sales manager"
    ]

    for comp in companies:

        domain = comp.get("domain")
        company_name = comp.get("name", "Unknown Company")

        print(f"\nSearching contacts for: {domain}")

        try:

            search_payload = {
                "page": 1,
                "filters": {
                    "company": {
                        "websites": {
                            "include": [domain]
                        }
                    }
                }
            }

            search_response = requests.post(
                search_url,
                json=search_payload,
                headers=headers,
                timeout=20
            )

            print("SEARCH STATUS:", search_response.status_code)

            if search_response.status_code != 200:
                print(search_response.text)
                continue

            search_data = search_response.json()

            results = search_data.get("results", [])

            # Limit contacts to avoid burning credits
            results = results[:10]

            print("RESULT COUNT:", len(results))

            for result in results:

                person = result.get("person", {})

                person_id = person.get("person_id")

                if not person_id:
                    continue

                # Avoid Prospeo 429 rate limits
                time.sleep(1)

                enrich_payload = {
                    "only_verified_email": True,
                    "data": {
                        "person_id": person_id
                    }
                }

                enrich_response = requests.post(
                    enrich_url,
                    json=enrich_payload,
                    headers=headers,
                    timeout=20
                )

                print(
                    f"ENRICH STATUS ({person.get('full_name')}):",
                    enrich_response.status_code
                )

                if enrich_response.status_code != 200:
                    continue

                enrich_data = enrich_response.json()

                enriched_person = enrich_data.get("person", {})

                email_data = enriched_person.get("email", {})

                revealed = email_data.get("revealed", False)
                email = email_data.get("email")

                if not revealed:
                    continue

                if not email:
                    continue

                title = enriched_person.get(
                    "current_job_title",
                    person.get("current_job_title", "Contact")
                )

                # Only decision makers
                if not any(
                    role in title.lower()
                    for role in decision_roles
                ):
                    print(
                        f"Skipping non-decision maker: "
                        f"{person.get('full_name')} ({title})"
                    )
                    continue

                lead = {
                    "name": enriched_person.get(
                        "full_name",
                        person.get("full_name")
                    ),
                    "email": email,
                    "title": title,
                    "company": company_name,
                    "linkedin": enriched_person.get(
                        "linkedin_url",
                        person.get("linkedin_url", "")
                    )
                }

                leads.append(lead)

                print(
                    f"DECISION MAKER FOUND -> "
                    f"{lead['name']} | "
                    f"{lead['title']} | "
                    f"{lead['email']}"
                )

        except Exception as e:
            print("Prospeo Error:", e)

    # Remove duplicate emails
    unique_leads = []
    seen = set()

    for lead in leads:

        if lead["email"] not in seen:
            seen.add(lead["email"])
            unique_leads.append(lead)

    leads = unique_leads

    print(f"\nDECISION MAKERS FOUND: {len(leads)}")

    if not leads:

        print(
            "\nNo decision makers found. "
            "Using fallback contact."
        )

        company = companies[0]

        leads.append({
            "name": f"{company['name']} Contact",
            "email": f"contact@{company['domain']}",
            "title": "Business Contact",
            "company": company["name"],
            "linkedin": ""
        })

    print(
        f"\nStage 2 completed. "
        f"Total leads collected: {len(leads)}"
    )

    return leads