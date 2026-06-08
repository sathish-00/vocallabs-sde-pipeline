import sqlite3
from datetime import datetime
import requests


def send_outreach(enriched_leads, brevo_key, sender_email):
    # FIXED: This print statement must be indented to be inside the function body
    print(
        "\n--- Starting Stage 4: Preparing Brevo SMTP payload for transmission ---"
    )

    if not brevo_key:
        print("Error: Brevo API key is missing.")
        return

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": brevo_key,
    }

    # Connect to database and create table once before looping
    conn = sqlite3.connect("pipeline_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            title TEXT,
            company TEXT,
            delivery_timestamp TEXT
        )
    """)
    conn.commit()

    for lead in enriched_leads:
        email_addr = lead.get("email")
        lead_name = lead.get("name", "Prospect")
        company_name = lead.get("company", "Unknown Company")
        job_title = lead.get("title", "Executive")

        if not email_addr:
            continue

        print(f"Sending outreach message to: {lead_name} ({email_addr})")

        payload = {
            "sender": {"name": "Sathish Kodari", "email": sender_email},
            "to": [{"email": email_addr, "name": lead_name}],
            "subject": f"Quick Question for {company_name}",
            "htmlContent": f"""
                <h3>Hello {lead_name}</h3>
                <p>
                    I would love to connect regarding
                    potential collaboration opportunities.
                </p>
            """,
        }

        try:
            response = requests.post(
                url, json=payload, headers=headers, timeout=20
            )

            print(f"Status: {response.status_code}")

            if response.status_code in [200, 201]:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute(
                    """
                    INSERT INTO processed_leads 
                    (name, email, title, company, delivery_timestamp)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        lead_name,
                        email_addr,
                        job_title,
                        company_name,
                        timestamp,
                    ),
                )
                # Committing inside the loop keeps the DB up-to-date instantly per lead
                conn.commit()
                print(f"Logged to database: {lead_name}")

        except Exception as e:
            print(f"Brevo Error: {e}")

    # Safely close connection once all leads are processed
    conn.close()