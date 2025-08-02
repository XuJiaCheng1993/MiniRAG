import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv(os.path.join(os.getcwd(), ".env"))
api_key = os.getenv("SILICONFLOW_API_KEY")

db_password = os.getenv("PG_PASSWORD")
db_user = os.getenv("PG_USER")
db_host = os.getenv("PG_HOST")
db_port = os.getenv("PG_PORT")
db_database = "dash"


vector_db_connection_string = f"postgresql://{db_user}:{quote(db_password)}@{db_host}:{db_port}/{db_database}"
vector_db_collection_name = "minirag"
