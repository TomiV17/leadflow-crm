from flask import Blueprint, jsonify, render_template, request

from app.services.scraper import scrape_google_maps
from app.services.lead_service import (
    save_leads,
    get_all_leads,
    get_ready_leads,
    get_leads_by_status,
    update_lead_status
)

leads_bp = Blueprint("leads", __name__)


# =========================
# API RAW (debug / backend)
# =========================
@leads_bp.route("/", methods=["GET"])
def get_leads():
    return jsonify(get_all_leads())


# =========================
# PANEL PRINCIPAL (CRM)
# =========================
@leads_bp.route("/panel", methods=["GET"])
def panel():

    status = request.args.get("status")
    search = request.args.get("search", "").lower()
    min_score = request.args.get("min_score")

    # 1. base data (pipeline o general)
    if status:
        leads = get_leads_by_status(status)
    else:
        leads = get_all_leads()

    # 2. filtros UI
    if search:
        leads = [l for l in leads if search in (l["nombre"] or "").lower()]

    if min_score:
        leads = [l for l in leads if l["score"] >= int(min_score)]

    return render_template("panel.html", leads=leads)


# =========================
# SCRAPER UI
# =========================
@leads_bp.route("/scrape-ui", methods=["POST"])
def scrape_ui():

    # 🔥 tomar query desde el formulario
    query = request.form.get("query")

    # seguridad
    if not query:
        return "Falta el query (ej: barberías en Córdoba)"

    print("QUERY RECIBIDO:", query)

    # scraping dinámico
    leads = scrape_google_maps(query)

    save_leads(leads)

    return f"""
    <h2>Scraping terminado</h2>
    <p>Query: {query}</p>
    <p>Leads encontrados: {len(leads)}</p>
    <a href="/leads/panel">Volver</a>
    """



# =========================
# HOT LEADS (alta calidad)
# =========================
@leads_bp.route("/hot", methods=["GET"])
def hot_leads():
    leads = get_ready_leads()
    return render_template("panel.html", leads=leads)


# =========================
# PIPELINE ACTIONS
# =========================
@leads_bp.route("/lead/<int:lead_id>/status/<status>", methods=["GET"])
def change_status(lead_id, status):
    update_lead_status(lead_id, status)
    return "OK"
