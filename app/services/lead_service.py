from app.database import get_connection


# =========================
# 🧠 SCORE DE CALIDAD
# =========================
def calculate_score(lead):
    score = 0

    # peso más realista (valor comercial)
    if lead.get("telefono"):
        score += 35

    if lead.get("email"):
        score += 25

    if lead.get("web"):
        score += 25

    if lead.get("direccion"):
        score += 15

    return score


# =========================
# 🔍 VERIFICAR DUPLICADOS
# =========================
def lead_exists(cursor, telefono=None, email=None):
    if telefono:
        cursor.execute("SELECT id FROM leads WHERE telefono = ?", (telefono,))
        if cursor.fetchone():
            return True

    if email:
        cursor.execute("SELECT id FROM leads WHERE email = ?", (email,))
        if cursor.fetchone():
            return True

    return False


# =========================
# 🚀 GUARDAR LEADS
# =========================
def save_leads(leads):
    conn = get_connection()
    cursor = conn.cursor()

    for lead in leads:

        # seguridad de datos
        nombre = lead.get("nombre") or "Sin nombre"
        empresa = lead.get("empresa") or nombre
        telefono = lead.get("telefono")
        email = lead.get("email")
        web = lead.get("web")
        direccion = lead.get("direccion") or ""

        # duplicados
        if lead_exists(cursor, telefono, email):
            print("DUPLICADO:", nombre)
            continue

        # score
        score = calculate_score(lead)

        # filtro calidad mínima
        if score < 40:
            print("DESCARTADO:", nombre, "score:", score)
            continue

        cursor.execute("""
            INSERT INTO leads (
                nombre, empresa, telefono, email, web, direccion, score, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre,
            empresa,
            telefono,
            email,
            web,
            direccion,
            score,
            "new"
        ))

    conn.commit()
    conn.close()


# =========================
# 📊 OBTENER TODOS LOS LEADS
# =========================
def get_all_leads():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM leads
        ORDER BY score DESC, id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# =========================
# 🔥 LEADS DE ALTA CALIDAD
# =========================
def get_ready_leads():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM leads
        WHERE score >= 70
        ORDER BY score DESC
    """)

    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return leads


# =========================
# 🧭 PIPELINE POR ESTADO
# =========================
def update_lead_status(lead_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE leads
        SET status = ?
        WHERE id = ?
    """, (status, lead_id))

    conn.commit()
    conn.close()


def get_leads_by_status(status=None):
    conn = get_connection()
    cursor = conn.cursor()

    if status and status.strip():
        cursor.execute("""
            SELECT * FROM leads
            WHERE status = ?
            ORDER BY score DESC
        """, (status,))
    else:
        cursor.execute("""
            SELECT * FROM leads
            ORDER BY score DESC
        """)

    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return leads
