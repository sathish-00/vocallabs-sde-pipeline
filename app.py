import sqlite3
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from main import run_pipeline

app = Flask(__name__)


@app.route("/")
def home():

    leads = []

    time_range = request.args.get("range", "all")

    try:

        conn = sqlite3.connect("pipeline_records.db")
        cursor = conn.cursor()

        base_query = """
        SELECT
            name,
            email,
            title,
            company,
            delivery_timestamp
        FROM processed_leads
        """

        if time_range == "1hr":

            query = f"""
            {base_query}
            WHERE delivery_timestamp >=
            datetime('now','-1 hour','localtime')
            ORDER BY id DESC
            """

        elif time_range == "24h":

            query = f"""
            {base_query}
            WHERE delivery_timestamp >=
            datetime('now','-1 day','localtime')
            ORDER BY id DESC
            """

        elif time_range == "1w":

            query = f"""
            {base_query}
            WHERE delivery_timestamp >=
            datetime('now','-7 day','localtime')
            ORDER BY id DESC
            """

        elif time_range == "1m":

            query = f"""
            {base_query}
            WHERE delivery_timestamp >=
            datetime('now','-1 month','localtime')
            ORDER BY id DESC
            """

        elif time_range == "1y":

            query = f"""
            {base_query}
            WHERE delivery_timestamp >=
            datetime('now','-1 year','localtime')
            ORDER BY id DESC
            """

        else:

            query = f"""
            {base_query}
            ORDER BY id DESC
            """

        cursor.execute(query)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            timestamp = row[4]

            try:

                formatted_timestamp = datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M:%S"
                ).strftime(
                    "%d %b %Y %I:%M:%S %p"
                )

            except Exception:

                formatted_timestamp = timestamp

            leads.append({
                "name": row[0],
                "email": row[1],
                "title": row[2],
                "company": row[3],
                "timestamp": formatted_timestamp
            })

    except Exception as e:

        print("Database extraction failed:", e)

    return render_template(
        "index.html",
        historical_leads=leads,
        current_filter=time_range
    )


@app.route("/api/run", methods=["POST"])
def trigger_pipeline():

    try:

        request_data = (
            request.get_json()
            if request.is_json
            else {}
        )

        user_input = (
            request_data.get("domain")
            or request.form.get("domain")
        )

        if not user_input:

            return jsonify({
                "status": "error",
                "message": "No domain supplied."
            }), 400

        run_pipeline(user_input)

        conn = sqlite3.connect("pipeline_records.db")

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                name,
                email,
                title,
                company,
                delivery_timestamp
            FROM processed_leads
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        conn.close()

        if row:

            try:

                formatted_timestamp = datetime.strptime(
                    row[4],
                    "%Y-%m-%d %H:%M:%S"
                ).strftime(
                    "%d %b %Y %I:%M:%S %p"
                )

            except Exception:

                formatted_timestamp = row[4]

            return jsonify({
                "status": "success",
                "lead": {
                    "name": row[0],
                    "email": row[1],
                    "title": row[2],
                    "company": row[3],
                    "timestamp": formatted_timestamp
                }
            })

        return jsonify({
            "status": "success",
            "message": "Pipeline completed."
        })

    except Exception as e:

        print("Runtime error:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )