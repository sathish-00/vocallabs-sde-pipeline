import os
from dotenv import load_dotenv

# Stage Imports
from src.stage1_apollo import fetch_companies
from src.stage1_similar_companies import get_similar_companies
from src.stage2_prospeo import hunt_leads
from src.stage3_eazyreach import enrich_leads
from src.stage4_brevo import send_outreach


def run_pipeline(target_input):

    print("------------------------------------------------------------------")
    print(
        f"Initializing VocalLabs SDE Automation Pipeline for: "
        f"{target_input}"
    )
    print("------------------------------------------------------------------")

    # Load Environment Variables
    load_dotenv()

    apollo_key = os.getenv("APOLLO_API_KEY")
    prospeo_key = os.getenv("PROSPEO_API_KEY")
    eazy_id = os.getenv("EAZYREACH_CLIENT_ID")
    eazy_secret = os.getenv("EAZYREACH_CLIENT_SECRET")
    brevo_key = os.getenv("BREVO_API_KEY")

    sender = os.getenv(
        "SENDER_EMAIL",
        "outreach@sathishkodari00.space"
    )

    # ==========================================================
    # STAGE 1 - INITIAL COMPANY
    # ==========================================================

    companies = fetch_companies(
        domain=target_input,
        apollo_key=apollo_key,
        count=1
    )

    if not companies:

        print(
            f"⚠ No company found for "
            f"{target_input}"
        )

        companies = [{
            "name": target_input.split(".")[0].capitalize(),
            "domain": target_input
        }]

    # ==========================================================
    # STAGE 1.5 - DYNAMIC SIMILAR COMPANY DISCOVERY
    # ==========================================================

    try:

        print(
            "\n--- Starting Similar Company Discovery ---"
        )

        similar_companies = get_similar_companies(
            target_input,
            apollo_key
        )

        if similar_companies:

            print(
                f"Found {len(similar_companies)} "
                f"similar companies."
            )

            existing_domains = {
                company["domain"]
                for company in companies
            }

            for company in similar_companies:

                if (
                    company["domain"]
                    not in existing_domains
                ):

                    companies.append(company)

        else:

            print(
                "No similar companies returned."
            )

    except Exception as e:

        print(
            f"Similar company discovery failed: {e}"
        )

    print("\nFINAL COMPANY LIST:")

    for company in companies:

        print(
            f"- {company['name']} "
            f"({company['domain']})"
        )

    # ==========================================================
    # STAGE 2 - DECISION MAKER DISCOVERY
    # ==========================================================

    leads = hunt_leads(
        companies,
        prospeo_key=prospeo_key
    )

    if not leads:

        print(
            "\nPipeline stopped:"
            " No contacts discovered."
        )

        return []

    # ==========================================================
    # STAGE 3 - CONTACT ENRICHMENT
    # ==========================================================

    enriched_leads = enrich_leads(
        leads,
        client_id=eazy_id,
        client_secret=eazy_secret
    )

    # ==========================================================
    # STAGE 4 - OUTREACH
    # ==========================================================

    send_outreach(
        enriched_leads,
        brevo_key=brevo_key,
        sender_email=sender
    )

    print("------------------------------------------------------------------")
    print(
        f"All modular automation pipeline stages "
        f"completed for: {target_input}"
    )
    print("------------------------------------------------------------------")

    return enriched_leads


if __name__ == "__main__":

    run_pipeline("razorpay.com")