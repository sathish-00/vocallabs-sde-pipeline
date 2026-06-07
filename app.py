import os
import sqlite3
from flask import Flask, jsonify, render_template, request
from main import run_pipeline

app = Flask(__name__)

@app.route("/")
def home():
    leads = []
    # Grab selected dropdown range filter from request args (defaults to 'all')
    time_range = request.args.get('range', 'all')
    
    try:
        conn = sqlite3.connect("pipeline_records.db")
        cursor = conn.cursor()
        
        base_query = "SELECT name, email, title, company, delivery_timestamp FROM processed_leads"
        
        # Parse filter parameters using standard SQLite date modifiers
        if time_range == "24h":
            query = f"{base_query} WHERE delivery_timestamp >= datetime('now', '-1 day') ORDER BY id DESC"
        elif time_range == "1w":
            query = f"{base_query} WHERE delivery_timestamp >= datetime('now', '-7 days') ORDER BY id DESC"
        elif time_range == "1m":
            query = f"{base_query} WHERE delivery_timestamp >= datetime('now', '-1 month') ORDER BY id DESC"
        elif time_range == "1y":
            query = f"{base_query} WHERE delivery_timestamp >= datetime('now', '-1 year') ORDER BY id DESC"
        else:
            query = f"{base_query} ORDER BY id DESC"
            
        cursor.execute(query)
        rows = cursor.fetchall()
        
        for row in rows:
            leads.append({
                "name": row[0],
                "email": row[1],
                "title": row[2],
                "company": row[3],
                "timestamp": row[4]
            })
        conn.close()
    except Exception as e:
        print(f"Database extraction failed: {e}")
        
    return render_template("index.html", historical_leads=leads, current_filter=time_range)

@app.route("/api/run", methods=["POST"])
def trigger_pipeline():
    try:
        run_pipeline()
        
        conn = sqlite3.connect("pipeline_records.db")
        cursor = conn.cursor()
        
        latest_query = "SELECT name, email, title, company, delivery_timestamp FROM processed_leads ORDER BY id DESC LIMIT 1"
        cursor.execute(latest_query)
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                "status": "success",
                "lead": {
                    "name": row[0],
                    "email": row[1],
                    "title": row[2],
                    "company": row[3],
                    "timestamp": row[4]
                }
            })
            
        return jsonify({"status": "success", "message": "Pipeline completed without errors."})
        
    except Exception as e:
        print(f"Runtime error inside API trigger route: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)