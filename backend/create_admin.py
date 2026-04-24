import os
import getpass
import bcrypt
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def create_admin():
    if not DATABASE_URL:
        print("[!] ERROR: DATABASE_URL not set in environment.")
        return

    print("=== Create Madhavi Enterprises Admin ===")
    email = input("Admin Email: ").strip()
    if not email:
        print("[!] Email cannot be empty.")
        return
        
    password = getpass.getpass("Admin Password: ")
    if not password:
        print("[!] Password cannot be empty.")
        return

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        # Connect to Neon PostgreSQL DB
        conn = psycopg2.connect(DATABASE_URL)
        c = conn.cursor()
        
        # Insert admin credentials
        c.execute(
            "INSERT INTO admins (email, password_hash) VALUES (%s, %s)",
            (email, hashed_password)
        )
        conn.commit()
        
        print(f"\n[+] Success! Admin account created for: {email}")
        print("[*] You can now log in via the /admin.html dashboard.")
        
    except psycopg2.IntegrityError:
        print(f"\n[!] ERROR: An admin with the email '{email}' already exists.")
    except Exception as e:
        print(f"\n[!] ERROR: Failed to create admin: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    create_admin()
