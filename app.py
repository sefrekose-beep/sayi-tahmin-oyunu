import streamlit as st
import random

st.set_page_config(page_title="Sayı Tahmin Arenası", page_icon="🎯", layout="centered")

st.title("🎯 Sayı Tahmin Arenası")

# --- 1. Yan Menü (Sidebar): Seviye Seçimi ---
st.sidebar.header("⚙️ Oyun Ayarları")

seviye = st.sidebar.selectbox(
    "Zorluk Seviyesi Seç:",
    ["Kolay (1-10, 3 Can)", "Orta (1-20, 5 Can)", "Zor (1-50, 7 Can)"]
)

# Seviyeye göre kuralları belirleyelim
if "Kolay" in seviye:
    maks_sayi = 10
    toplam_can = 3
elif "Orta" in seviye:
    maks_sayi = 20
    toplam_can = 5
else:
    maks_sayi = 50
    toplam_can = 7

# --- 2. Oyun Hafızası (Session State) ---
def oyunu_sifirla():
    st.session_state.gizli_sayi = random.randint(1, maks_sayi)
    st.session_state.kalan_hak = toplam_can
    st.session_state.toplam_hak = toplam_can
    st.session_state.tahminler = []
    st.session_state.oyun_bitti = False

# İlk açılışta veya seviye değiştiğinde hafızayı hazırla
if "gizli_sayi" not in st.session_state or st.session_state.get("aktif_seviye") != seviye:
    st.session_state.aktif_seviye = seviye
    oyunu_sifirla()

if "en_iyi_skor" not in st.session_state:
    st.session_state.en_iyi_skor = "-"

# Rekoru yan menüde göster
st.sidebar.divider()
st.sidebar.metric(label="🏆 En İyi Rekor", value=f"{st.session_state.en_iyi_skor} deneme")

# --- 3. Üst Bilgi ve İlerleme Çubuğu ---
st.write(f"**1 ile {maks_sayi}** arasında bir sayı tuttum. Tahminini yap!")

oran = max(0.0, st.session_state.kalan_hak / st.session_state.toplam_hak)
st.progress(oran, text=f"Kalan Can: {st.session_state.kalan_hak} / {st.session_state.toplam_hak}")

# --- 4. Oyun Alanı ---
if not st.session_state.oyun_bitti:
    tahmin = st.number_input(f"Tahminin kaç? (1-{maks_sayi})", min_value=1, max_value=maks_sayi, step=1)

    if st.button("Tahmin Et 🚀"):
        if tahmin in st.session_state.tahminler:
            st.info(f"⚠️ {tahmin} sayısını zaten girdin, hakkın gitmedi!")
        else:
            st.session_state.kalan_hak -= 1
            st.session_state.tahminler.append(tahmin)

            if tahmin == st.session_state.gizli_sayi:
                deneme_sayisi = len(st.session_state.tahminler)
                st.balloons()
                st.success(f"🎉 Bildin! Doğru sayı: {st.session_state.gizli_sayi} ({deneme_sayisi} denemede buldun)")
                
                # Rekor güncelleme
                if st.session_state.en_iyi_skor == "-" or deneme_sayisi < st.session_state.en_iyi_skor:
                    st.session_state.en_iyi_skor = deneme_sayisi
                    st.info("🔥 Tebrikler, yeni bir rekor kırdın!")
                    
                st.session_state.oyun_bitti = True
            elif st.session_state.kalan_hak == 0:
                st.error(f"💥 Hakkın tükendi! Tuttuğum sayı: {st.session_state.gizli_sayi} idi.")
                st.session_state.oyun_bitti = True
            elif tahmin < st.session_state.gizli_sayi:
                st.warning("⬆️ Daha BÜYÜK bir sayı söyle!")
            else:
                st.warning("⬇️ Daha KÜÇÜK bir sayı söyle!")

# --- 5. Geçmiş ve Yeniden Başlatma ---
if st.session_state.tahminler:
    st.divider()
    st.write("📋 **Denenen Sayılar:**", ", ".join(map(str, st.session_state.tahminler)))

if st.session_state.oyun_bitti:
    if st.button("Tekrar Oyna 🔄"):
        oyunu_sifirla()
        st.rerun()