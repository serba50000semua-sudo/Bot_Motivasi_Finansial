import streamlit as st
import requests
import datetime

# --- SISTEM KEAMANAN (PASSWORD DARI SOCIABUZZ) ---
PASSWORD_RAHASIA = "Semogasukes140926"

def check_password():
    if "password_benar" not in st.session_state:
        st.session_state["password_benar"] = False

    if not st.session_state["password_benar"]:
        st.title("🔒 Portal Inspirasi Finansial")
        masukan = st.text_input("Masukkan Password Akses:", type="password")
        if st.button("Masuk"):
            if masukan == PASSWORD_RAHASIA:
                st.session_state["password_benar"] = True
                st.rerun()
            else:
                st.error("Password salah! Silakan periksa kembali.")
        return False
    return True

def generate_motivasi_filosofis(api_key):
    nama_mesin = "models/gemini-3.5-flash"
    tanggal_hari_ini = datetime.date.today().strftime("%d %B %Y")
    
    prompt = f"""
    Bertindaklah sebagai seorang filsuf finansial yang bijaksana, berwibawa, dan mengayomi. 
    Hari ini adalah tanggal {tanggal_hari_ini}. 
    
    Tugasmu adalah menyajikan 3 hingga 5 kutipan (quote) motivasi finansial paling terkenal dan bermakna filosofis yang sangat relevan untuk direnungkan hari ini. 
    Kutipan bisa berasal dari tokoh ekonomi, investor legendaris, filsuf, atau pemikir besar dunia.
    
    ATURAN PENULISAN:
    1. Pilih 3 sampai 5 kutipan terbaik yang memberikan efek 'mind-blowing' (pencerahan mendalam bagi pembaca).
    2. Sebutkan secara jelas kutipannya dan siapa pencetusnya.
    3. Jelaskan makna filosofis di balik kutipan tersebut dengan bahasa yang sangat mudah dipahami oleh orang awam, hangat, menenangkan, namun penuh wawasan mendalam.
    4. Karakter bahasa: Bijaksana, membimbing, mengayomi, dan mencerahkan.
    5. Jangan gunakan tanda bintang (*) atau format markdown berlebihan agar teks bersih saat dibaca.
    
    FORMAT PENYAJIAN PER KUTIPAN:
    
    KUTIPAN [Nomor]:
    "Isi kutipan yang menginspirasi..."
    Pencetus: [Nama Tokoh]
    
    MAKNA & FILOSOFI MENDALAM:
    [Penjelasan yang mencerahkan, mudah dicerna, dan aplikatif untuk kehidupan finansial sehari-hari dengan gaya bahasa seorang bijak yang mengayomi]
    
    ---
    """

    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/{nama_mesin}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url_gemini, json=payload, headers={'Content-Type': 'application/json'}, timeout=90)
        data = response.json()
        
        if 'error' in data:
            return None, f"Error API: {data['error']['message']}"
            
        hasil_ai = data['candidates'][0]['content']['parts'][0]['text']
        return hasil_ai.replace('*', ''), None
        
    except Exception as e:
        return None, f"Gagal menghubungi server AI. Pastikan internet aktif. Error: {e}"

# --- JALANKAN APLIKASI WEB JIKA PASSWORD BENAR ---
if check_password():
    # 1. TAMPILAN SIDEBAR
    st.sidebar.title("⚙️ Pengaturan Akses")
    
    st.sidebar.markdown("**Langkah 1:** Dapatkan Kunci API (Gratis)")
    st.sidebar.markdown("[Klik di sini untuk buat API Key (Google AI Studio)](https://aistudio.google.com/app/apikey)")
    
    st.sidebar.markdown("**Langkah 2:** Masukkan Kunci API Anda di bawah ini:")
    api_key_pelanggan = st.sidebar.text_input(
        "API Key Gemini:", 
        type="password", 
        help="Paste API Key Anda di sini"
    )
    
    if api_key_pelanggan:
        st.session_state["API_KEY"] = api_key_pelanggan

    st.sidebar.markdown("---")
    st.sidebar.info("Privasi terjamin. Kunci API Anda tidak pernah disimpan di server kami.")

    # 2. TAMPILAN UTAMA
    if "API_KEY" not in st.session_state or st.session_state["API_KEY"] == "":
        st.warning("⚠️ Silakan masukkan API Key Gemini Anda di menu samping (sidebar) terlebih dahulu.")
        
    else:
        st.title("🌟 Renungan & Filosofi Finansial Harian")
        st.write("Temukan pencerahan, kutipan abadi, dan kebijaksanaan finansial yang mengubah cara pandang Anda terhadap kekayaan dan kehidupan.")
        
        tanggal_tampil = datetime.date.today().strftime("%A, %d %B %Y")
        st.info(f"📅 Waktu Refleksi Hari Ini: {tanggal_tampil}")
        
        if st.button("✨ Singkap Kutipan & Filosofi Hari Ini"):
            with st.spinner("Menyelami kebijaksanaan dan menyusun pencerahan untuk Anda..."):
                hasil_renungan, error = generate_motivasi_filosofis(st.session_state["API_KEY"])
                
                if error:
                    st.error(f"[GAGAL] {error}")
                else:
                    st.success("Renungan Hari Ini Berhasil Dimuat")
                    st.markdown("---")
                    
                    # Tampilkan hasil di kotak teks yang rapi atau markdown
                    st.markdown(hasil_renungan)
                    
                    st.markdown("---")
                    st.caption("Semoga kutipan hari ini membawa ketenangan pikiran dan kelimpahan bagi langkah Anda.")