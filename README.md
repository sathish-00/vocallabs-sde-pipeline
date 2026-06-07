
# SDE Modular Automation Engine 

A robust, full-stack automated cold-outreach pipeline that handles lookalike company discovery, decision-maker extraction, and automated email dispatch with zero human intervention[cite: 1]. Built dynamically with a Python (Flask) backend, a responsive Bootstrap frontend tracker, and relational SQLite3 transaction log tracking.

---

## 🛠️ System Architecture & Workflow

The engine runs seamlessly across a fully decoupled, 4-stage pipeline where every stage's output serves automatically as the next stage's input[cite: 1]:

1. **Stage 1: Lookalike Company Discovery (Ocean.io)** 
   * Takes a single seed domain manual input and expands it into an organized list of target lookalike company domains[cite: 1].
2. **Stage 2: Decision-Maker Hunt (Prospeo)** 
   * Parses extracted domains to isolate C-suite/VP-level target decision-makers alongside their explicit names and LinkedIn URLs[cite: 1].
3. **Stage 3: Data Enrichment & Fallback Processing** 
   * Formatted to handle data handoffs securely[cite: 1]. Per the updated FAQ guidelines regarding EazyReach credit caps, the backend gracefully utilizes Prospeo's comprehensive target extraction data as an operational fallback to route active payloads without crashing on partial API failures[cite: 1].
4. **Stage 4: Personalized Outreach Dispatch (Brevo SMTP)** 
   * Automatically formats and fires custom, personalized email payloads straight to the target contacts using robust SMTP delivery channels[cite: 1].

---

## ✨ Features Added

* **Live Pipeline Tracker Flowchart:** A beautiful, responsive frontend UI grid that visually shifts state styles (`node-active` to `node-success`) in real-time as background API automation tasks process.
* **Historical Transmission Filter Matrix:** Built a dynamic time-range drop-down component (`All Completed`, `Last 24 Hours`, `1 Week`, `1 Month`, `1 Year`) leveraging server-side SQLite query parameters to isolate data log metrics instantly.
* **Resilient Error Tolerances:** Configured with try-except fallback routes ensuring missing contacts or network rate limits do not break the end-to-end processing loop[cite: 1].


## Local Deployment Setup

1. Clone the Project
git clone [https://github.com/sathish-00/vocallabs-sde-pipeline.git](https://github.com/sathish-00/vocallabs-sde-pipeline.git)
cd vocallabs-sde-pipeline

2. Configure Your Virtual Environment
python -m venv venv


3. Install Dependencies
pip install -r requirements.txt

4. Fire Up the Server
python app.py
