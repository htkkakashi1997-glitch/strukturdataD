import streamlit as st

st.set_page_config(page_title="Searching & Hashing", page_icon="🔍", layout="wide")

st.title("🔍 Searching Algorithm & Hashing")
st.caption("Struktur Data — Informatika UINSSC | Muhammad Iszul Wilsa, S.Si., M.Cs")

tab1, tab2, tab3 = st.tabs(["📋 Linear Search", "🔎 Binary Search", "🗂️ Hash Table"])


# ══════════════════════════════════════════
# HELPER: render array sebagai HTML
# ══════════════════════════════════════════
def render_array(arr, highlight=-1, found=-1, inactive=None):
    if inactive is None:
        inactive = []
    html = "<div style='display:flex;flex-wrap:wrap;gap:6px;margin:10px 0'>"
    for i, v in enumerate(arr):
        if i == found:
            bg = "#d4edda"; border = "#28a745"; tc = "#155724"
        elif i == highlight:
            bg = "#cce5ff"; border = "#004085"; tc = "#004085"
        elif i in inactive:
            bg = "#f8f9fa"; border = "#dee2e6"; tc = "#adb5bd"
        else:
            bg = "#ffffff"; border = "#ced4da"; tc = "#212529"
        html += (
            f"<div style='width:54px;text-align:center;border:2px solid {border};"
            f"border-radius:8px;background:{bg};color:{tc};padding:8px 0;'>"
            f"<b style='font-size:16px'>{v}</b>"
            f"<div style='font-size:10px;color:#888'>{i}</div></div>"
        )
    html += "</div>"
    return html


def render_binary(arr, low, high, mid, found=-1):
    html = "<div style='display:flex;flex-wrap:wrap;gap:6px;margin:10px 0'>"
    for i, v in enumerate(arr):
        if i == found:
            bg = "#d4edda"; border = "#28a745"; tc = "#155724"; label = "✓"
        elif i == mid:
            bg = "#fff3cd"; border = "#ffc107"; tc = "#856404"; label = "M"
        elif low <= i <= high:
            bg = "#e8f4fd"; border = "#004085"; tc = "#004085"
            label = "L" if i == low else ("H" if i == high else "")
        else:
            bg = "#f8f9fa"; border = "#dee2e6"; tc = "#adb5bd"; label = ""
        html += (
            f"<div style='width:54px;text-align:center;border:2px solid {border};"
            f"border-radius:8px;background:{bg};color:{tc};padding:8px 0;'>"
            f"<b style='font-size:16px'>{v}</b>"
            f"<div style='font-size:10px;color:#888'>{i}</div>"
            f"<div style='font-size:10px;font-weight:bold'>{label}</div></div>"
        )
    html += "</div>"
    return html


# ══════════════════════════════════════════
# TAB 1 - LINEAR SEARCH
# ══════════════════════════════════════════
with tab1:
    st.subheader("Sequential / Linear Search")
    st.info("Mencari data secara urut dari indeks pertama sampai ditemukan atau habis.")

    arr_input = st.text_input(
        "Array (pisahkan koma)",
        value="10, 50, 30, 70, 80, 60, 20, 90, 40",
        key="l_arr"
    )
    key_input = st.number_input("Key yang dicari", value=30, key="l_key")

    if st.button("🔍 Cari", key="btn_linear"):
        try:
            arr = [int(x.strip()) for x in arr_input.split(",")]
            key = int(key_input)

            # Simpan semua langkah dulu
            steps = []
            found_idx = -1
            for i in range(len(arr)):
                match = arr[i] == key
                steps.append({"i": i, "match": match})
                if match:
                    found_idx = i
                    break

            # Tampilkan semua langkah
            st.markdown("#### Langkah-langkah Pencarian")
            for s in steps:
                i = s["i"]
                match = s["match"]
                inactive = list(range(0, i))

                if match:
                    st.markdown(
                        render_array(arr, highlight=-1, found=i, inactive=inactive),
                        unsafe_allow_html=True
                    )
                    st.success(f"✅ Langkah {i+1}: arr[{i}] = {arr[i]} == {key} → DITEMUKAN di indeks {i}!")
                else:
                    st.markdown(
                        render_array(arr, highlight=i, found=-1, inactive=inactive),
                        unsafe_allow_html=True
                    )
                    st.write(f"Langkah {i+1}: arr[{i}] = {arr[i]} ≠ {key}, lanjut...")

            if found_idx == -1:
                st.markdown(
                    render_array(arr, inactive=list(range(len(arr)))),
                    unsafe_allow_html=True
                )
                st.error(f"🔴 Key {key} tidak ditemukan dalam array.")

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("#### Kompleksitas Waktu")
    c1, c2, c3 = st.columns(3)
    c1.metric("Best Case", "O(1)", "Key di indeks pertama")
    c2.metric("Worst Case", "O(N)", "Key di indeks terakhir")
    c3.metric("Average Case", "O(N)", "Rata-rata N/2 langkah")


# ══════════════════════════════════════════
# TAB 2 - BINARY SEARCH
# ══════════════════════════════════════════
with tab2:
    st.subheader("Binary Search")
    st.info("Data harus terurut. Setiap langkah membuang separuh data yang tidak relevan.")

    arr_input2 = st.text_input(
        "Array (pisahkan koma)",
        value="2, 5, 8, 12, 16, 23, 38, 56, 72, 91",
        key="b_arr"
    )
    key_input2 = st.number_input("Key yang dicari", value=23, key="b_key")

    if st.button("🔍 Cari", key="btn_binary"):
        try:
            arr = sorted([int(x.strip()) for x in arr_input2.split(",")])
            key = int(key_input2)

            st.info(f"Array setelah diurutkan: {arr}")
            st.markdown("**Legend:** 🔵 Rentang aktif &nbsp; 🟡 Mid (M) &nbsp; L = Low &nbsp; H = High &nbsp; ⬜ Sudah dibuang")

            # Simpan semua langkah dulu
            steps = []
            low, high = 0, len(arr) - 1
            found_idx = -1

            while low <= high:
                mid = (low + high) // 2
                if arr[mid] == key:
                    steps.append({"low": low, "mid": mid, "high": high, "result": "found"})
                    found_idx = mid
                    break
                elif arr[mid] < key:
                    steps.append({"low": low, "mid": mid, "high": high, "result": "go_right"})
                    low = mid + 1
                else:
                    steps.append({"low": low, "mid": mid, "high": high, "result": "go_left"})
                    high = mid - 1

            if found_idx == -1:
                steps.append({"low": low, "mid": -1, "high": high, "result": "not_found"})

            # Tampilkan semua langkah
            st.markdown("#### Langkah-langkah Pencarian")
            for step_num, s in enumerate(steps):
                lo, mi, hi, res = s["low"], s["mid"], s["high"], s["result"]
                st.markdown(f"**Langkah {step_num + 1}** — Low={lo}, Mid={mi}, High={hi}")

                if res == "found":
                    st.markdown(render_binary(arr, lo, hi, mi, found=mi), unsafe_allow_html=True)
                    st.success(f"✅ arr[{mi}] = {arr[mi]} == {key} → DITEMUKAN di indeks {mi}!")
                elif res == "go_right":
                    st.markdown(render_binary(arr, lo, hi, mi), unsafe_allow_html=True)
                    st.write(f"arr[{mi}] = {arr[mi]} < {key} → geser Low ke {mi + 1}")
                elif res == "go_left":
                    st.markdown(render_binary(arr, lo, hi, mi), unsafe_allow_html=True)
                    st.write(f"arr[{mi}] = {arr[mi]} > {key} → geser High ke {mi - 1}")
                else:
                    st.markdown(render_binary(arr, lo, hi, -1), unsafe_allow_html=True)
                    st.error(f"🔴 Key {key} tidak ditemukan dalam array.")

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("#### Kompleksitas Waktu")
    c1, c2, c3 = st.columns(3)
    c1.metric("Best Case", "O(1)", "Key tepat di tengah")
    c2.metric("Worst Case", "O(log N)", "Key di ujung / tidak ada")
    c3.metric("Average Case", "O(log N)", "Jauh lebih cepat dari linear")


# ══════════════════════════════════════════
# TAB 3 - HASH TABLE
# ══════════════════════════════════════════
with tab3:
    st.subheader("Hash Table")
    st.info("Fungsi hash: h(k) = k mod M")

    col1, col2 = st.columns(2)
    with col1:
        M = st.number_input("Ukuran tabel (M)", min_value=3, max_value=20, value=7, key="hm")
    with col2:
        method = st.selectbox("Metode Collision", ["Chaining", "Linear Probing"])

    val_in = st.number_input("Nilai yang akan diinsert", value=0, key="hv")

    # Inisialisasi session state
    if ("ht" not in st.session_state or
            st.session_state.get("ht_M") != int(M) or
            st.session_state.get("ht_method") != method):
        st.session_state.ht_M = int(M)
        st.session_state.ht_method = method
        st.session_state.ht_log = []
        if method == "Chaining":
            st.session_state.ht = [[] for _ in range(int(M))]
        else:
            st.session_state.ht = [None] * int(M)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("➕ Insert", key="btn_insert"):
            v = int(val_in)
            m = int(M)
            idx = v % m
            ht = st.session_state.ht

            if method == "Chaining":
                collision = len(ht[idx]) > 0
                ht[idx].append(v)
                if collision:
                    msg = f"⚠️ Insert {v}: h({v}) = {v} mod {m} = {idx} → Collision! Chaining di indeks {idx}"
                else:
                    msg = f"✅ Insert {v}: h({v}) = {v} mod {m} = {idx} → Disimpan di indeks {idx}"
            else:
                pos = idx
                probes = 0
                placed = False
                msg = ""
                while probes < m:
                    if ht[pos] is None:
                        ht[pos] = v
                        if probes == 0:
                            msg = f"✅ Insert {v}: h({v}) = {v} mod {m} = {idx} → Disimpan di indeks {idx}"
                        else:
                            msg = f"⚠️ Insert {v}: h({v}) = {v} mod {m} = {idx} → Collision! Probe {probes}x, disimpan di indeks {pos}"
                        placed = True
                        break
                    pos = (pos + 1) % m
                    probes += 1
                if not placed:
                    msg = f"❌ Insert {v}: Tabel penuh!"

            st.session_state.ht = ht
            st.session_state.ht_log.append(msg)

    with col_b:
        if st.button("🔄 Reset Tabel", key="btn_reset"):
            st.session_state.ht_log = []
            if method == "Chaining":
                st.session_state.ht = [[] for _ in range(int(M))]
            else:
                st.session_state.ht = [None] * int(M)

    # Render tabel hash
    st.markdown("#### Tabel Hash")
    ht = st.session_state.ht
    m = int(M)

    html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin:10px 0'>"
    for i in range(m):
        if method == "Chaining":
            if ht[i]:
                bg = "#d4edda" if len(ht[i]) == 1 else "#fff3cd"
                border = "#28a745" if len(ht[i]) == 1 else "#ffc107"
                tc = "#155724" if len(ht[i]) == 1 else "#856404"
                isi = "<br>".join([f"<b>{x}</b>" for x in ht[i]])
            else:
                bg = "#f8f9fa"; border = "#dee2e6"; tc = "#adb5bd"; isi = "—"
        else:
            if ht[i] is not None:
                bg = "#cce5ff"; border = "#004085"; tc = "#004085"
                isi = f"<b style='font-size:18px'>{ht[i]}</b>"
            else:
                bg = "#f8f9fa"; border = "#dee2e6"; tc = "#adb5bd"; isi = "—"

        html += (
            f"<div style='width:70px;min-height:80px;border:2px solid {border};"
            f"border-radius:8px;background:{bg};color:{tc};"
            f"text-align:center;padding:8px 4px;'>"
            f"<div style='font-size:11px;color:#888;margin-bottom:4px'>idx {i}</div>"
            f"{isi}</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    # Log insert
    if st.session_state.get("ht_log"):
        st.markdown("#### Log Insert")
        for i, log in enumerate(st.session_state.ht_log, 1):
            st.markdown(f"{i}. {log}")

    st.markdown("---")
    st.markdown("#### Contoh: Insert 14, 5, 9, 1, 24 dengan M = 7")
    st.table({
        "Nilai (k)":      [14, 5, 9, 1, 24],
        "h(k) = k mod 7": [14%7, 5%7, 9%7, 1%7, 24%7]
    })