import requests

def send_outreach(enriched_leads, brevo_key, sender_email):
    print("\n--- Starting Stage 4: Preparing Brevo SMTP payload for transmission ---")
    if not brevo_key:
        print("Error: Brevo API key is missing. Exiting.")
        return

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json", 
        "content-type": "application/json", 
        "api-key": brevo_key
    }

    for lead in enriched_leads:
        email_addr = lead.get("email")
        lead_name = lead.get("name", "Prospect")
        company_name = lead.get("company", "Target Company")
        job_title = lead.get("title", "Executive")
        
        if not email_addr:
            print("Skipping record due to missing email field.")
            continue
            
        print(f"Sending outreach message to: {lead_name} ({email_addr})")
        
        # Structuring transactional parameters
        payload = {
            "sender": {"name": "Sathish Kodari", "email": sender_email},
            "to": [{"email": email_addr, "name": lead_name}],
            "subject": f"Synergy Partnership Request - {company_name}",
            "htmlContent": (
                f"<h3>Hi {lead_name},</h3>"
                f"<p>I reached out because of your position as <strong>{job_title}</strong> at {company_name}.</p>"
                f"<p>We are optimizing automated full-stack pipeline engines out of Hyderabad and wanted to "
                f"see if you have 5 minutes for a technical demonstration next week.</p><br/>"
                f"<p>Best Regards,<br/><strong>Sathish Kodari</strong></p>"
            )
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code in [200, 201]:
                msg_id = response.json().get('messageId')
                print(f"Message sent successfully. ID: {msg_id}")
            else:
                print(f"Server rejected message payload with code: {response.status_code}")
                
        except Exception as e:
            print(f"Network error or exception hitting Brevo gateway: {e}")