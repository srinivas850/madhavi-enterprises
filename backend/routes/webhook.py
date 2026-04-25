import os
import jwt
from flask import Blueprint, request, jsonify, Response
from functools import wraps
import psycopg2
from psycopg2.extras import RealDictCursor
import json

from services.groq_service import extract_lead_data
from services.whatsapp_service import send_hot_lead_whatsapp
from utils.excel_export import generate_ai_leads_excel

webhook_bp = Blueprint('webhook', __name__)

JWT_SECRET = os.environ.get("JWT_SECRET", "madhavi_enterprises_secret_key_2025")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth.split(" ")[1]
        if not token:
            return jsonify({"message": "Authentication required"}), 401
        try:
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Session expired, please log in again"}), 401
        except Exception as e:
            return jsonify({"message": f"Invalid token: {e}"}), 401
        return f(*args, **kwargs)
    return decorated

def get_pg_db():
    try:
        url = os.getenv("DATABASE_URL")
        if not url: return None
        if "?sslmode=" in url:
            return psycopg2.connect(url)
        return psycopg2.connect(url, sslmode="require")
    except Exception as e:
        print("DB Error:", e)
        return None

@webhook_bp.route('/webhook/call-completed', methods=['POST'])
def call_completed_webhook():
    try:
        data = request.get_json() or {}
        transcript = data.get('transcript', '')
        
        if not transcript:
            return jsonify({"status": "ignored", "message": "No transcript provided"}), 200

        # Extract data using Groq
        extracted_data = extract_lead_data(transcript)
        
        if not extracted_data:
            return jsonify({"status": "error", "message": "Failed to extract lead data"}), 500

        # Store in DB
        conn = get_pg_db()
        if not conn:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500
            
        c = conn.cursor()
        c.execute('''
            INSERT INTO ai_extracted_leads (
                name, phone, budget, location_preference, property_type, 
                buying_timeline, interest_level, key_requirements, 
                conversation_summary, raw_json
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        ''', (
            extracted_data.get('name'),
            extracted_data.get('phone'),
            extracted_data.get('budget'),
            extracted_data.get('location_preference'),
            extracted_data.get('property_type'),
            extracted_data.get('buying_timeline'),
            extracted_data.get('interest_level'),
            extracted_data.get('key_requirements'),
            extracted_data.get('conversation_summary'),
            json.dumps(extracted_data)
        ))
        
        lead_id = c.fetchone()[0]
        conn.commit()
        conn.close()

        # Trigger WhatsApp if Hot
        interest_level = str(extracted_data.get('interest_level', '')).strip().lower()
        if interest_level == 'hot':
            send_hot_lead_whatsapp(
                name=extracted_data.get('name'),
                phone=extracted_data.get('phone'),
                property_type=extracted_data.get('property_type'),
                location_preference=extracted_data.get('location_preference'),
                budget=extracted_data.get('budget')
            )

        return jsonify({
            "status": "success",
            "message": "Lead processed and saved",
            "id": lead_id,
            "data": extracted_data
        }), 200

    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@webhook_bp.route('/api/admin/ai-leads', methods=['GET'])
@token_required
def get_ai_leads():
    try:
        conn = get_pg_db()
        if not conn:
            return jsonify([])
        c = conn.cursor(cursor_factory=RealDictCursor)
        c.execute("SELECT * FROM ai_extracted_leads ORDER BY created_at DESC")
        rows = c.fetchall()
        conn.close()
        
        for r in rows:
            if 'created_at' in r and r['created_at']:
                r['created_at'] = r['created_at'].isoformat()
                
        return jsonify({"leads": rows})
    except Exception as e:
        print(f"Get AI leads error: {e}")
        return jsonify({"error": str(e)}), 500


@webhook_bp.route('/api/admin/ai-leads/export', methods=['GET'])
@token_required
def export_ai_leads():
    try:
        conn = get_pg_db()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        c = conn.cursor(cursor_factory=RealDictCursor)
        c.execute("SELECT * FROM ai_extracted_leads ORDER BY created_at DESC")
        rows = c.fetchall()
        conn.close()
        
        for r in rows:
            if 'created_at' in r and r['created_at']:
                r['created_at'] = r['created_at'].strftime("%Y-%m-%d %H:%M:%S")

        buf = generate_ai_leads_excel(rows)
        
        return Response(
            buf.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=AIExtractedLeads.xlsx"}
        )
    except Exception as e:
        print(f"Export AI leads error: {e}")
        return jsonify({"error": str(e)}), 500
