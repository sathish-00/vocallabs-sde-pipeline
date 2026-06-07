import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Clean package imports from our src folder
from src.stage1_apollo import fetch_companies
from src.stage2_prospeo import hunt_leads
from src.stage3_eazyreach import enrich_leads
from src.stage4_brevo import send_outreach

def init_database():
    """Initializes a local SQLite database to store pipeline metrics and leads."""
    conn = sqlite3.connect("pipeline_records.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            title TEXT,
            company TEXT,
            mobile_status TEXT,
            delivery_timestamp TEXT
        )
    """)
    conn.commit()
    return conn

def log_leads_to_db(leads):
    """Saves successfully processed leads into the database with a timestamp."""
    conn = init_database()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for lead in leads:
        # Check instance type to safely extract attributes
        if isinstance(lead, dict):
            name = lead.get("name", "Unknown")
            email = lead.get("email", "Unknown")
            title = lead.get("title", "Unknown")
            company = lead.get("company", "Unknown")
        else:
            name = getattr(lead, "name", "Unknown")
            email = getattr(lead, "email", "Unknown")
            title = getattr(lead, "title", "Unknown")
            company = getattr(lead, "company", "Unknown")
        
        cursor.execute("""
            INSERT INTO processed_leads (name, email, title, company, mobile_status, delivery_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, title, company, "Enriched/Verified", timestamp))
        
    conn.commit()
    conn.close()
    print(f"Database sync: Successfully cached {len(leads)} execution records.")

def run_pipeline():
    print("------------------------------------------------------------------")
    print("Initializing VocalLabs SDE Modular Automation Pipeline")
    print("------------------------------------------------------------------")
    
    # Load environment configuration variables
    load_dotenv()
    
    apollo_key = os.getenv("APOLLO_API_KEY")
    prospeo_key = os.getenv("PROSPEO_API_KEY")
    eazy_id = os.getenv("EAZYREACH_CLIENT_ID")
    eazy_secret = os.getenv("EAZYREACH_CLIENT_SECRET")
    brevo_key = os.getenv("BREVO_API_KEY")
    sender = os.getenv("SENDER_EMAIL", "outreach@sathishkodari00.space")

    # Step 1: Query targeted enterprise entities via Apollo
    companies = fetch_companies(keyword="Hyderabad Tech", apollo_key=apollo_key, count=2)
    if not companies:
        print("Pipeline stopped: No companies retrieved in Stage 1.")
        return

    # Step 2: Extract decision maker profiles via Prospeo
    leads = hunt_leads(companies, prospeo_key=prospeo_key)
    if not leads:
        print("Pipeline stopped: No target contacts isolated in Stage 2.")
        return

    # Step 3: Run data structure enrichment via EazyReach
    enriched_leads = enrich_leads(leads, client_id=eazy_id, client_secret=eazy_secret)

    # Step 4: Dispatch transactional outbound email layouts via Brevo
    send_outreach(enriched_leads, brevo_key=brevo_key, sender_email=sender)

    # Step 5: Save execution rows to the relational database cache
    try:
        log_leads_to_db(enriched_leads)
    except Exception as e:
        print(f"Database logging exception encountered: {e}")

    print("------------------------------------------------------------------")
    print("All modular automation pipeline stages completed successfully.")
    print("------------------------------------------------------------------")

if __name__ == "__main__":
    run_pipeline()