import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def add_violation(data):
    supabase.table("violations").insert(data).execute()

def get_violations():
    return supabase.table("violations").select("*").execute().data

def mark_fine_paid(plate):
    supabase.table("violations").update({"paid": True}).eq("plate", plate).execute()

def get_owner(plate):
    owners = {
        "ABC-1234": {"email": "owner1@example.com", "name": "John Doe"},
        "XYZ-5678": {"email": "owner2@example.com", "name": "Jane Smith"},
    }
    return owners.get(plate, {"email": "unknown@example.com", "name": "Unknown"})
