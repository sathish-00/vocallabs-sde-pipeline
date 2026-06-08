# SDE Modular Automation Engine

A robust, full-stack automated cold-outreach pipeline that handles target company processing, decision-maker discovery, contact enrichment, and automated email dispatch with minimal human intervention.

Built using:

* Python (Flask)
* SQLite3
* Bootstrap
* Apollo API
* Prospeo API
* EazyReach API
* Brevo SMTP

---

# System Architecture & Workflow

The engine executes a fully modular pipeline where each stage automatically feeds data into the next stage.

## Stage 1: Company Discovery

Accepts a single company domain as input and generates a normalized company profile.

Example:

```text
freshworks.com
```

Output:

```json
{
  "name": "Freshworks",
  "domain": "freshworks.com"
}
```

---

## Stage 1.5: Similar Company Discovery

Uses Apollo Organization Enrichment to retrieve:

* Industry
* Employee Count
* Keywords
* Technologies
* Location

The project includes dynamic Apollo Organization Search integration.

Current Limitation:

Apollo's free plan restricts access to the Organization Search endpoint and returns:

```text
403 API_INACCESSIBLE
```

The implementation is included and can be activated with a supported Apollo subscription.

---

## Stage 2: Decision-Maker Hunt (Prospeo)

Parses target companies and isolates senior decision-makers.

Examples:

* CTO
* VP Technology
* VP Engineering
* Senior Vice President
* Director
* Founder

The system filters non-decision-makers automatically.

---

## Stage 3: Contact Enrichment (EazyReach)

Handles:

* Session generation
* Contact enrichment
* Additional profile data retrieval

The pipeline includes fallback processing to ensure API failures do not terminate execution.

---

## Stage 4: Personalized Outreach Dispatch (Brevo SMTP)

Automatically builds personalized outreach emails and sends them through Brevo.

Features:

* Dynamic recipient personalization
* Custom email templates
* Delivery status tracking
* Error handling

---

# Features Added

## Live Pipeline Tracker

Responsive frontend dashboard displaying:

* Pipeline execution state
* Processing status
* Historical activity

---

## Historical Transmission Tracking

SQLite-backed logging system supporting:

* All Records
* Last Hour
* Last 24 Hours
* Last Week
* Last Month
* Last Year

Filtering occurs server-side for efficient querying.

---

## SQLite Audit Logging

Each successful outreach stores:

* Name
* Email
* Job Title
* Company
* Delivery Timestamp

inside:

```text
pipeline_records.db
```

---

## Resilient Error Handling

Implemented using:

```python
try:
    ...
except Exception:
    ...
```

The pipeline continues execution even when:

* Contacts are unavailable
* APIs return rate limits
* Partial enrichment failures occur

---

# Example Execution

Input:

```text
freshworks.com
```

Discovered Decision Makers:

```text
Andrew Wharton
VP of Technology

Prasad Athawale
Vice President

Karthick Subramanian
Senior Engineering Manager

Alex Glanz
Senior Vice President
```

Pipeline:

```text
Company Discovery
        ↓
Decision Maker Discovery
        ↓
Contact Enrichment
        ↓
Email Outreach
        ↓
SQLite Logging
        ↓
Dashboard Tracking
```

---

# Local Deployment Setup

## Clone Repository

```bash
git clone https://github.com/sathish-00/vocallabs-sde-pipeline.git
cd vocallabs-sde-pipeline
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file:

```env
APOLLO_API_KEY=your_key
PROSPEO_API_KEY=your_key
EAZYREACH_CLIENT_ID=your_id
EAZYREACH_CLIENT_SECRET=your_secret
BREVO_API_KEY=your_key
SENDER_EMAIL=your_email
```

## Start Server

```bash
python app.py
```

Application URL:

```text
http://127.0.0.1:5000
```

---

# Future Enhancements

* Apollo Organization Search (Paid Plan)
* Dynamic Similar Company Discovery
* CRM Integrations
* Email Open Tracking
* Reply Tracking
* Campaign Analytics
* AI-Based Outreach Personalization

---

# Assignment Objective

The project demonstrates a complete automated outreach workflow capable of:

1. Processing target companies.
2. Discovering relevant decision makers.
3. Enriching contact information.
4. Sending personalized outreach automatically.
5. Persisting execution history in SQLite.
6. Visualizing execution history through a dashboard.
