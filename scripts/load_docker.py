import subprocess
import sys
import time
import os

compose_files = [
    "docker-compose-mysql.yml",
    "docker-compose-chromadb.yml",
    "docker-compose-ollama.yml",
    "docker-compose-app.yml"
]

# def validate_compose_files(files):
#     for f in files:
#         print(f"🔍 Validating {f}...")
#         try:
#             subprocess.run(["docker-compose", "-f", f, "config"], check=True, capture_output=True)
#         except subprocess.CalledProcessError as e:
#             print(f"❌ Error in {f}:\n{e.stderr.decode()}")
#             sys.exit(1)

def wait_for_mysql(container_name="flask-mysql-db", retries=10, delay=2):
    print("\n⏳ Waiting for MySQL to be ready...")
    root_pw = os.getenv('DB_ROOT_PASSWORD', 'supersecurepassword')

    for attempt in range(retries):
        result = subprocess.run([
            "docker", "exec", container_name, "mysqladmin",
            "-uroot", f"-p{root_pw}", "ping"
        ], capture_output=True, text=True)

        if "mysqld is alive" in result.stdout:
            print("✅ MySQL is ready.")
            return
        else:
            print(f"🔄 MySQL not ready yet ({attempt + 1}/{retries}). Retrying in {delay}s...")
            time.sleep(delay)

    raise RuntimeError("❌ MySQL did not become ready in time.")

def import_sql_file(sql_file="mysql-init/insert_data.sql", db_name="ai_chatbot_db", container_name="flask-mysql-db"):
    print(f"\n📥 Importing data from {sql_file} into {db_name}...")
    root_pw = os.getenv('DB_ROOT_PASSWORD', 'supersecurepassword')

    try:
        subprocess.run([
            "docker", "exec", "-i", container_name, "mysql",
            "-uroot", f"-p{root_pw}", db_name
        ], input=open(sql_file, "rb").read(), check=True)
        print("✅ Sample data imported successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to import sample data:\n{e}")
        sys.exit(1)

# Step 1: Validate each compose file
# validate_compose_files(compose_files) #replacing with combined validation block below. helper function commented out
# Step 1: Validate combined docker-compose configuration
print("\n🔍 Validating full docker-compose stack...")
validate_cmd = ["docker-compose"]
for f in compose_files:
    validate_cmd.extend(["-f", f])
try:
    subprocess.run(validate_cmd + ["config"], check=True, capture_output=True)
    print("✅ Compose files validated successfully.")
except subprocess.CalledProcessError as e:
    print(f"❌ Compose validation failed:\n{e.stderr.decode()}")
    sys.exit(1)

# Step 2: Compose build command
cmd = ["docker-compose"]
for f in compose_files:
    cmd.extend(["-f", f])

# Step 3: Tear down existing containers
print("\n🧹 Stopping and removing any existing containers...")
try:
    subprocess.run(cmd + ["down"], check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    print(f"⚠️ Warning: 'down' failed (possibly nothing was running): {e.stderr.decode() if e.stderr else str(e)}")

# Step 4: Bring everything up
print("\n🚀 Rebuilding and starting all services...")
try:
    subprocess.run(cmd + ["up", "--build"], check=True)
    print("\n✅ All services started successfully.")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Failed to bring up services:\n{e.stderr.decode() if e.stderr else str(e)}")
    sys.exit(1)

# Step 5: Wait for MySQL, then import data
wait_for_mysql()
import_sql_file(
    sql_file="mysql-init/insert_data.sql",
    db_name="ai_chatbot_db",
    container_name="ai_chatbot_db"
)

def run_schema_ingestion():
    print("\n📥 Loading schema into ChromaDB...")
    try:
        subprocess.run(["python", "scripts/load_schema_to_chroma.py"], check=True)
        print("✅ Schema loaded into ChromaDB.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to load schema into ChromaDB:\n{e}")
        sys.exit(1)

# And call:
run_schema_ingestion()
