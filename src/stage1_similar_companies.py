import requests


def get_similar_companies(domain, apollo_key):

    print("\n--- Starting Similar Company Discovery ---")

    # ==================================================
    # STEP 1 - ENRICH ORIGINAL COMPANY
    # ==================================================

    enrich_url = (
        "https://api.apollo.io/api/v1/organizations/enrich"
    )

    headers = {
        "X-Api-Key": apollo_key,
        "Content-Type": "application/json"
    }

    try:

        enrich_response = requests.get(
            enrich_url,
            headers=headers,
            params={
                "domain": domain
            },
            timeout=20
        )

        print(
            "ORGANIZATION ENRICH STATUS:",
            enrich_response.status_code
        )

        if enrich_response.status_code != 200:

            print(
                "Failed to enrich company."
            )

            return []

        enrich_data = enrich_response.json()

        company = enrich_data.get(
            "organization",
            {}
        )

        country = company.get(
            "country",
            ""
        )

        keywords = company.get(
            "keywords",
            []
        )

        employee_count = company.get(
            "estimated_num_employees",
            0
        )

        print("\nTARGET COMPANY PROFILE")

        print(
            "Country:",
            country
        )

        print(
            "Employees:",
            employee_count
        )

        print(
            "Keywords:",
            keywords[:5]
        )

    except Exception as e:

        print(
            f"Company enrichment error: {e}"
        )

        return []

    # ==================================================
    # STEP 2 - BUILD EMPLOYEE RANGE
    # ==================================================

    min_emp = max(
        1,
        int(employee_count * 0.5)
    )

    max_emp = max(
        50,
        int(employee_count * 1.5)
    )

    employee_range = (
        f"{min_emp},{max_emp}"
    )

    # ==================================================
    # STEP 3 - ORGANIZATION SEARCH
    # ==================================================

    search_url = (
        "https://api.apollo.io/api/v1/mixed_companies/search"
    )

    payload = {
        "organization_locations": [
            country
        ],
        "organization_num_employees_ranges": [
            employee_range
        ],
        "q_organization_keyword_tags":
            keywords[:3],
        "page": 1,
        "per_page": 10
    }

    print("\nAPOLLO SEARCH PAYLOAD:")
    print(payload)

    try:

        search_response = requests.post(
            search_url,
            json=payload,
            headers=headers,
            timeout=30
        )

        print(
            "ORGANIZATION SEARCH STATUS:",
            search_response.status_code
        )

        # ------------------------------------------
        # FREE PLAN BLOCK
        # ------------------------------------------

        if search_response.status_code == 403:

            print(
                "\nApollo Organization Search "
                "is not available on the current plan."
            )

            print(
                "Continuing pipeline with "
                "seed company only."
            )

            return []

        if search_response.status_code != 200:

            print(
                "Apollo company search failed."
            )

            try:

                print(
                    search_response.json()
                )

            except Exception:

                print(
                    search_response.text
                )

            return []

        search_data = search_response.json()

        print(
            "\nAPOLLO SEARCH RESPONSE RECEIVED"
        )

        organizations = search_data.get(
            "organizations",
            []
        )

        similar_companies = []

        for org in organizations:

            org_domain = org.get(
                "primary_domain"
            )

            if (
                not org_domain
                or org_domain == domain
            ):
                continue

            similar_companies.append({
                "name": org.get(
                    "name",
                    "Unknown"
                ),
                "domain": org_domain
            })

        print(
            f"\nSIMILAR COMPANIES FOUND: "
            f"{len(similar_companies)}"
        )

        for comp in similar_companies:

            print(
                f"- {comp['name']} "
                f"({comp['domain']})"
            )

        return similar_companies[:5]

    except Exception as e:

        print(
            f"Apollo search exception: {e}"
        )

        return []