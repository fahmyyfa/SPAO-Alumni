import time
import requests
import re
from supabase import create_client

# 1. AMBIL DARI FILE .env ANDA
SUPABASE_URL = "https://ertyoxwnsuxxbzhewurf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVydHlveHduc3V4eGJ6aGV3dXJmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NTA4MDQyNiwiZXhwIjoyMDkwNjU2NDI2fQ.eVVKnT84aZY_OG5MrufU3IrefLp4pe3fqcu3nir6koo"
SERPER_API_KEY = "9cb5433ddb247054aab3aa2ee0bfbb3e4fde340f"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_real_data(nama):
    url = "https://google.serper.dev/search"
    # Robot mencari semua platform sekaligus
    query = f'"{nama}" alumni Universitas Muhammadiyah Malang linkedin instagram facebook tiktok'
    payload = {"q": query, "num": 5} # Ambil 5 hasil teratas untuk akurasi platform
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    
    response = requests.post(url, headers=headers, json=payload).json()
    results = response.get("organic", [])
    
    # Inisialisasi Data ABC=ABC
    data = {
        "linkedin": "-", "instagram": "-", "facebook": "-", "tiktok": "-",
        "email": "-", "no_hp": "-", "tempat_bekerja": "-", "alamat_bekerja": "-",
        "posisi": "-", "status_pekerjaan": "-", "sosmed_kantor": "-"
    }

    if not results:
        return data

    # 1. Identifikasi Link Sosmed Asli
    for res in results:
        link = res.get("link", "").lower()
        if "linkedin.com/in/" in link and data["linkedin"] == "-": data["linkedin"] = res.get("link")
        if "instagram.com/" in link and data["instagram"] == "-": data["instagram"] = res.get("link")
        if "facebook.com/" in link and data["facebook"] == "-": data["facebook"] = res.get("link")
        if "tiktok.com/" in link and data["tiktok"] == "-": data["tiktok"] = res.get("link")

    # 2. Ekstraksi Teks Asli dari Snippet (ABC = ABC)
    top_snippet = results[0].get("snippet", "")
    
    # Mencoba mengambil email jika ada di teks Google
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', top_snippet)
    if email_match: data["email"] = email_match.group(0)
    
    # Mencoba mengambil nomor HP jika ada di teks Google
    phone_match = re.search(r'(\+62|08)[0-9]{8,12}', top_snippet)
    if phone_match: data["no_hp"] = phone_match.group(0)

    # Data Pekerjaan diambil langsung dari potongan teks Google (Raw Text)
    if " at " in top_snippet:
        parts = top_snippet.split(" at ")
        data["posisi"] = parts[0].split("...")[-1].strip()
        data["tempat_bekerja"] = parts[1].split(".")[0].split(",")[0].strip()
        data["status_pekerjaan"] = "Pekerja" # Label umum jika ditemukan data kerja
    
    data["alamat_bekerja"] = top_snippet[:50] # Raw snippet sebagai alamat/lokasi terdeteksi

    return data

def start_pure_enrichment():
    print("--- Memulai Pengumpulan Data Riil (Raw Mapping ABC=ABC) ---")
    
    # Ambil 20 data yang masih kosong
    res = supabase.table("alumni").select("*").is_("linkedin", "null").limit(1000).execute()
    
    for alumni in res.data:
        nama = alumni['nama_lengkap']
        print(f"Crawling riil: {nama}...")
        
        real_data = get_real_data(nama)
        
        supabase.table("alumni").update(real_data).eq("id", alumni['id']).execute()
        print(f"Hasil disimpan untuk: {nama}")
        time.sleep(1)

if __name__ == "__main__":
    start_pure_enrichment()