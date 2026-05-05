import streamlit as st
from datetime import timedelta


# ════════════════════════════════════════════════════════════
#  CIRCULAR LINKED LIST
# ════════════════════════════════════════════════════════════

class Node:
    def __init__(self, color_name, duration, label, emoji_on, emoji_off):
        self.color_name = color_name
        self.duration = duration
        self.label = label
        self.emoji_on = emoji_on
        self.emoji_off = emoji_off
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.current = None
        self.size = 0

    def append(self, color_name, duration, label, emoji_on, emoji_off):
        baru = Node(color_name, duration, label, emoji_on, emoji_off)
        if self.head is None:
            self.head = baru
            baru.next = baru
            self.current = baru
        else:
            temp = self.head
            while temp.next is not self.head:
                temp = temp.next
            temp.next = baru
            baru.next = self.head
        self.size += 1

    def move_next(self):
        if self.current:
            self.current = self.current.next
            return self.current
        return None

    def get_all_nodes(self):
        hasil = []
        if self.head:
            temp = self.head
            while True:
                hasil.append(temp)
                temp = temp.next
                if temp is self.head:
                    break
        return hasil


# ════════════════════════════════════════════════════════════
#  KONFIGURASI HALAMAN & SESSION STATE
# ════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Simulasi Lampu Lalu Lintas",
    page_icon="🚦",
    layout="wide",
)

if "cll" not in st.session_state:
    cll = CircularLinkedList()
    cll.append("merah", 40, "MERAH", "🔴", "⚫")
    cll.append("kuning", 5, "KUNING", "🟡", "⚫")
    cll.append("hijau", 20, "HIJAU", "🟢", "⚫")
    st.session_state.cll = cll
    st.session_state.remaining = 40
    st.session_state.running = False
    st.session_state.cycle_count = 0
    st.session_state.total_time = 0
    st.session_state.history = []


# ════════════════════════════════════════════════════════════
#  JUDUL
# ════════════════════════════════════════════════════════════

st.title("🚦 Simulasi Lampu Lalu Lintas")
st.caption("Implementasi **Circular Linked List**  ·  Merah 40 detik  ·  Kuning 5 detik  ·  Hijau 20 detik")
st.divider()


# ════════════════════════════════════════════════════════════
#  TOMBOL KONTROL (di luar fragment — tetap interaktif)
# ════════════════════════════════════════════════════════════

kol1, kol2, kol3 = st.columns(3)

with kol1:
    if not st.session_state.running:
        if st.button("▶️  Mulai Simulasi", use_container_width=True, type="primary"):
            st.session_state.running = True
    else:
        if st.button("⏸️  Jeda Simulasi", use_container_width=True):
            st.session_state.running = False

with kol2:
    if st.button("🔄  Reset", use_container_width=True):
        st.session_state.running = False
        st.session_state.remaining = 40
        st.session_state.cycle_count = 0
        st.session_state.total_time = 0
        st.session_state.history = []
        st.session_state.cll.current = st.session_state.cll.head
        st.rerun()

with kol3:
    if st.button("⏭️  Skip ke Lampu Berikutnya", use_container_width=True):
        old = st.session_state.cll.current
        baru = st.session_state.cll.move_next()
        st.session_state.remaining = baru.duration
        if old.color_name == "hijau":
            st.session_state.cycle_count += 1
        mm, ss = divmod(st.session_state.total_time, 60)
        st.session_state.history.append({
            "label": f"{old.label} → {baru.label} (skip)",
            "waktu": f"{mm:02d}:{ss:02d}",
            "siklus": st.session_state.cycle_count,
        })
        st.rerun()

st.divider()


# ════════════════════════════════════════════════════════════
#  FRAGMENT UTAMA — update state + tampilan dinamis
# ════════════════════════════════════════════════════════════

@st.fragment(run_every=timedelta(seconds=1))
def tampilan_utama():

    # ── UPDATE STATE ──
    if st.session_state.running:
        st.session_state.remaining -= 1
        st.session_state.total_time += 1

        if st.session_state.remaining <= 0:
            old = st.session_state.cll.current
            baru = st.session_state.cll.move_next()
            st.session_state.remaining = baru.duration

            if old.color_name == "hijau":
                st.session_state.cycle_count += 1

            mm, ss = divmod(st.session_state.total_time, 60)
            st.session_state.history.append({
                "label": f"{old.label} → {baru.label}",
                "waktu": f"{mm:02d}:{ss:02d}",
                "siklus": st.session_state.cycle_count,
            })

    # ── BACA STATE ──
    node = st.session_state.cll.current
    rem = st.session_state.remaining
    nodes = st.session_state.cll.get_all_nodes()
    cycle = st.session_state.cycle_count
    total = st.session_state.total_time

    pesan = {"merah": "⏹  BERHENTI", "kuning": "⚠️  HATI-HATI", "hijau": "✅  JALAN"}
    status_teks = {"merah": "🔴 MERAH", "kuning": "🟡 KUNING", "hijau": "🟢 HIJAU"}

    # ── LAYOUT 3 KOLOM ──
    kiri, tengah, kanan = st.columns([1, 0.8, 1.3])

    # ════════════════════
    #  KIRI: Informasi
    # ════════════════════
    with kiri:
        st.subheader("📊 Informasi Status")

        st.metric(label="Status Lampu Saat Ini", value=status_teks[node.color_name])

        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Sisa Waktu", value=f"{rem} detik")
        with m2:
            st.metric(label="Siklus Ke-", value=f"#{cycle + 1}")

        m3, m4 = st.columns(2)
        with m3:
            st.metric(label="Total Waktu", value=f"{total} detik")
        with m4:
            st.metric(label="Durasi Siklus", value="65 detik")

        st.metric(label="Jumlah Node CLL", value=st.session_state.cll.size)

        st.divider()
        st.subheader("⏱️ Durasi Setiap Lampu")

        for n in nodes:
            aktif = n is node
            tanda = "▶️ " if aktif else "    "
            teks = f"{tanda}{n.emoji_on}  {n.label}  —  {n.duration} detik"
            if aktif:
                st.markdown(f"**{teks}**")
            else:
                st.markdown(teks)
            st.progress(n.duration / 40)

    # ════════════════════
    #  TENGAH: Lampu Lalu Lintas
    # ════════════════════
    with tengah:
        st.subheader("🚦 Lampu Lalu Lintas")

        st.markdown("")
        for n in nodes:
            if n is node:
                st.markdown(f"# {n.emoji_on}")
            else:
                st.markdown(f"##### {n.emoji_off}")
        st.markdown("")

        st.divider()

        st.markdown(f"## ⏳  {rem:02d}")
        st.markdown(f"**{pesan[node.color_name]}**")

        st.progress(rem / node.duration)
        st.caption(f"{rem} / {node.duration} detik")

        st.divider()

        if st.session_state.running:
            st.success("● Simulasi sedang berjalan")
        else:
            if total == 0:
                st.info("○ Siap dimulai")
            else:
                st.warning("○ Simulasi dijeda")

    # ════════════════════
    #  KANAN: Diagram CLL + Riwayat
    # ════════════════════
    with kanan:
        tab_diagram, tab_riwayat = st.tabs(["🔗 Diagram CLL", "📜 Riwayat"])

        with tab_diagram:
            st.caption("Struktur **Circular Linked List** saat ini:")

            baris = []
            baris.append("┌──────────────────────────────────────────────┐")
            baris.append("│              (kembali ke HEAD)               │")
            baris.append("└──────────────────────┬───────────────────────┘")
            baris.append("                       │")
            baris.append("                       ▼")

            for i, n in enumerate(nodes):
                is_current = (n is node)
                is_head = (n is st.session_state.cll.head)

                tanda_kiri = "▶▶ " if is_current else "   "
                tanda_kanan = " ◀◀" if is_current else ""
                tag_head = " ← HEAD" if is_head else ""

                baris.append(f"{tanda_kiri}┌─────────────────┐{tanda_kanan}")
                baris.append(f"   │  {n.emoji_on}  {n.label:<6}    │{tag_head}")
                baris.append(f"   │  Durasi: {n.duration:>2} detik │")
                baris.append(f"{tanda_kiri}└────────┬────────┘{tanda_kanan}")

                if i < len(nodes) - 1:
                    baris.append("            │")
                    baris.append("           next")
                    baris.append("            ▼")

            baris.append("            │")
            baris.append("           next")
            baris.append("            ▼")
            baris.append("       (kembali ke MERAH)")

            st.code("\n".join(baris), language=None)

            st.divider()
            st.caption("Visualisasi linear:")
            bagian = []
            for n in nodes:
                if n is node:
                    bagian.append(f"**[{n.label}: {n.duration}s]** ◀ CURRENT")
                else:
                    bagian.append(f"[{n.label}: {n.duration}s]")
            st.markdown(" ──next──▶ ".join(bagian) + " ──next──▶ ↩️ HEAD")

        with tab_riwayat:
            st.caption("Log perubahan state lampu:")
            if not st.session_state.history:
                st.info("Belum ada riwayat perubahan.")
            else:
                for entry in reversed(st.session_state.history[-50:]):
                    st.markdown(
                        f"**{entry['waktu']}**  —  {entry['label']}  "
                        f"*(Siklus #{entry['siklus'] + 1})*"
                    )


# ════════════════════════════════════════════════════════════
#  PANGGIL FRAGMENT
# ════════════════════════════════════════════════════════════

tampilan_utama()


# ════════════════════════════════════════════════════════════
#  PENJELASAN (Expander)
# ════════════════════════════════════════════════════════════

with st.expander("💡 Penjelasan Struktur Data — Circular Linked List"):
    st.markdown(
        "**Circular Linked List** adalah struktur data linear di mana "
        "node terakhir menunjuk kembali ke node pertama (`head`), "
        "membentuk siklus tanpa akhir."
    )
    st.markdown("")
    st.markdown("Pada simulasi ini:")
    st.markdown("")
    st.markdown("| Elemen | Penjelasan |")
    st.markdown("|--------|------------|")
    st.markdown("| **Node** | Menyimpan data lampu (warna, durasi) dan pointer `next` |")
    st.markdown("| **head** | Menunjuk ke node MERAH sebagai titik awal |")
    st.markdown("| **current** | Menunjuk ke lampu yang sedang aktif saat ini |")
    st.markdown("| **next** | Pointer dari setiap node ke node berikutnya |")
    st.markdown("| **Circular** | Node HIJAU.next → MERAH (bukan NULL) |")
    st.markdown("")
    st.markdown("**Alur Traversal:**")
    st.code(
        "MERAH (40s) ──next──▶ KUNING (5s) ──next──▶ HIJAU (20s)\n"
        "     ▲                                         │\n"
        "     └──────────────── next ───────────────────┘",
        language=None,
    )
    st.markdown("")
    st.markdown(
        "Setiap kali countdown mencapai **0**, pointer `current` berpindah ke "
        "`current.next`. Karena sifat *circular*, perpindahan ini terjadi "
        "secara otomatis tanpa pernah berhenti."
    )
    st.markdown("")
    st.markdown("**Implementasi dalam kode:**")
    st.code(
        "class Node:\n"
        "    def __init__(self, ...):\n"
        "        self.next = None        # pointer ke node berikutnya\n"
        "\n"
        "class CircularLinkedList:\n"
        "    def append(self, ...):\n"
        "        baru.next = self.head   # node baru menunjuk ke head\n"
        "        # ini yang membuat list menjadi CIRCULAR\n"
        "\n"
        "    def move_next(self):\n"
        "        self.current = self.current.next  # traversal maju",
        language="python",
    )