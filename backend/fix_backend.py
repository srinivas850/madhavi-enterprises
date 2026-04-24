import re

with open('backend.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Print statements at top and safe omni_client
content = content.replace("app = Flask(__name__)", "print('App starting...')\napp = Flask(__name__)")
content = content.replace("DATABASE_URL        = os.environ.get(\"DATABASE_URL\")", "DATABASE_URL        = os.environ.get(\"DATABASE_URL\")\nprint(\"DB status:\", DATABASE_URL is not None)")

omni_replace = """omni_client = Client(OMNI_API_KEY)"""
new_omni = """try:
    omni_client = Client(OMNI_API_KEY)
except Exception as e:
    print(f"Omnidimension Init Error: {e}")
    omni_client = None"""
content = content.replace(omni_replace, new_omni)

# 2. get_pg_db rewrite
old_get_db = """def get_pg_db():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not set")
    return psycopg2.connect(DATABASE_URL)"""

new_get_db = """def get_pg_db():
    try:
        url = os.getenv("DATABASE_URL")
        if not url: return None
        if "?sslmode=" in url:
            return psycopg2.connect(url)
        return psycopg2.connect(url, sslmode="require")
    except Exception as e:
        print("DB Error:", e)
        return None

@app.route("/")
def home():
    return "Backend is running"
"""
content = content.replace(old_get_db, new_get_db)

# 3. Fix all conn = get_pg_db() usages to handle None
lines = content.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    if "conn = get_pg_db()" in line and "def get_pg_db" not in line and "def init_pg_db" not in line:
        indent = line.split("conn")[0]
        # Peek at next line to see if it's already fixed
        if i + 1 < len(lines) and "if not conn:" in lines[i+1]:
            pass
        else:
            if "login" in new_lines[-2] or "login" in new_lines[-3]:
                # Special return for login
                new_lines.append(indent + "if not conn:")
                new_lines.append(indent + "    return jsonify({'status': 'error', 'message': 'DB connection failed'}), 500")
            elif "def " in new_lines[-2] or "def " in new_lines[-3]:
                # Inside route
                new_lines.append(indent + "if not conn:")
                new_lines.append(indent + "    return jsonify([])")
    
    # Wrap in try/except is harder line by line, but if we just handle the conn == None, it prevents 
    # the TypeError: 'NoneType' object has no attribute 'cursor'.
    # And Waitress catches normal exceptions with a 500. So we just need to make sure conn is closed.
    if "c = conn.cursor" in line:
        indent = line.split("c =")[0]
        # we can't easily wrap the whole block. 
        # But wait, python's garbage collector closes PG connections when they go out of scope in CPython.
        # But `conn.close()` is present in all routes.
    i += 1

with open('backend.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))
