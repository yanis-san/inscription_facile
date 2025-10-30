import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_current_academic_year():
    """Fetch the current active academic year from Supabase"""
    try:
        response = supabase.table("academic_years").select("*").eq("is_current", True).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching academic year: {e}")
        return None


@app.route("/")
def index():
    """Main page - display the registration form"""
    academic_year = get_current_academic_year()

    if not academic_year:
        return render_template("index.html", error="Aucune année académique active trouvée"), 500

    return render_template(
        "index.html",
        academic_year_label=academic_year.get("year_label"),
        academic_year_prefix=academic_year.get("prefix")
    )


@app.route("/api/register", methods=["POST"])
def register_student():
    """Register a new student"""
    try:
        data = request.get_json()

        # Validate mandatory fields
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip()

        if not first_name or not last_name or not email:
            return jsonify({
                "success": False,
                "error": "Les champs Prénom, Nom et Email sont obligatoires"
            }), 400

        # Get current academic year
        academic_year = get_current_academic_year()
        if not academic_year:
            return jsonify({
                "success": False,
                "error": "Aucune année académique active trouvée"
            }), 500

        # Check if email already exists
        existing = supabase.table("students").select("*").eq("email", email).execute()
        if existing.data and len(existing.data) > 0:
            return jsonify({
                "success": False,
                "error": f"L'email '{email}' est déjà enregistré"
            }), 400

        # Prepare student data
        student_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "academic_year_id": academic_year["id"]
        }

        # Add optional fields if provided
        phone_number = data.get("phone_number", "").strip()
        if phone_number:
            student_data["phone_number"] = phone_number

        birth_date = data.get("birth_date", "").strip()
        if birth_date:
            student_data["birth_date"] = birth_date

        # Insert student into database
        response = supabase.table("students").insert(student_data).execute()

        if response.data and len(response.data) > 0:
            student_code = response.data[0].get("student_code", "N/A")
            return jsonify({
                "success": True,
                "message": f"Inscription réussie! Code étudiant: {student_code}",
                "student_code": student_code
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": "Erreur lors de l'inscription"
            }), 500

    except Exception as e:
        print(f"Error registering student: {e}")
        return jsonify({
            "success": False,
            "error": f"Erreur serveur: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Page non trouvée"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Erreur serveur interne"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
