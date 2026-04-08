"""
Pokemon Card Tracker - FastAPI Application
Karten erfassen, auswerten und vergleichen
"""

import json
import logging
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import Card, SessionLocal, create_tables, get_db
from schemas import CardCreate, CardUpdate
import pokemon_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Pokemon Karten Tracker", version="1.0.0")

# Mount static files and templates
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

CONDITIONS = ["M", "NM", "LP", "MP", "HP", "D"]
CONDITION_LABELS = {
    "M":  "Mint (Perfekt)",
    "NM": "Near Mint (Fast perfekt)",
    "LP": "Lightly Played (Leicht gespielt)",
    "MP": "Moderately Played (Mäßig gespielt)",
    "HP": "Heavily Played (Stark gespielt)",
    "D":  "Damaged (Beschädigt)",
}
CONDITION_MULTIPLIER = {"M": 1.2, "NM": 1.0, "LP": 0.85, "MP": 0.65, "HP": 0.45, "D": 0.25}


@app.on_event("startup")
async def startup():
    create_tables()
    logger.info("Pokemon Card Tracker gestartet - Datenbank bereit.")


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def _card_value(card: Card) -> Optional[float]:
    """Estimated value based on market price and condition."""
    base = card.market_price_market or card.market_price_mid
    if base is None:
        return None
    mult = CONDITION_MULTIPLIER.get(card.condition, 1.0)
    if card.is_graded and card.grade_score:
        # PSA graded premium
        if card.grade_score >= 10:
            mult *= 3.0
        elif card.grade_score >= 9:
            mult *= 2.0
        elif card.grade_score >= 8:
            mult *= 1.5
    return round(base * mult, 2)


def _parse_json_field(val) -> list:
    if not val:
        return []
    try:
        return json.loads(val)
    except Exception:
        return []


def _collection_stats(cards: list[Card]) -> dict:
    total_cards = sum(c.quantity for c in cards)
    total_value = sum(
        (_card_value(c) or 0) * c.quantity for c in cards
    )
    total_purchase = sum(
        (c.purchase_price or 0) * c.quantity for c in cards
    )
    rarities = {}
    for c in cards:
        r = c.rarity or "Unbekannt"
        rarities[r] = rarities.get(r, 0) + c.quantity
    return {
        "total_cards": total_cards,
        "total_value": round(total_value, 2),
        "total_purchase": round(total_purchase, 2),
        "profit_loss": round(total_value - total_purchase, 2),
        "rarities": rarities,
        "unique_pokemon": len(cards),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Pages
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Session = Depends(get_db)):
    cards = db.query(Card).order_by(Card.added_at.desc()).all()
    stats = _collection_stats(cards)
    for c in cards:
        c.estimated_value = _card_value(c)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "cards": cards,
        "stats": stats,
        "condition_labels": CONDITION_LABELS,
    })


@app.get("/suche", response_class=HTMLResponse)
async def search_page(request: Request, q: str = "", page: int = 1):
    results = []
    total = 0
    if q:
        data = await pokemon_api.search_cards(q, page=page)
        results = data["cards"]
        total = data["total"]
    return templates.TemplateResponse("search.html", {
        "request": request,
        "query": q,
        "results": results,
        "total": total,
        "page": page,
        "page_size": 20,
    })


@app.get("/karte/neu", response_class=HTMLResponse)
async def new_card_form(request: Request, api_id: str = ""):
    prefill = {}
    if api_id:
        prefill = await pokemon_api.get_card_by_id(api_id) or {}
    return templates.TemplateResponse("card_form.html", {
        "request": request,
        "prefill": prefill,
        "conditions": CONDITIONS,
        "condition_labels": CONDITION_LABELS,
        "edit_mode": False,
    })


@app.post("/karte/neu")
async def add_card(
    request: Request,
    db: Session = Depends(get_db),
    api_id: str = Form(""),
    name: str = Form(...),
    set_name: str = Form(""),
    number: str = Form(""),
    rarity: str = Form(""),
    hp: str = Form(""),
    types: str = Form(""),
    image_url: str = Form(""),
    image_url_hires: str = Form(""),
    market_price_market: str = Form(""),
    condition: str = Form("NM"),
    quantity: int = Form(1),
    purchase_price: str = Form(""),
    is_foil: str = Form(""),
    is_graded: str = Form(""),
    grade_score: str = Form(""),
    grading_company: str = Form(""),
    notes: str = Form(""),
):
    def to_float(v):
        try:
            return float(v) if v.strip() else None
        except Exception:
            return None

    def to_int(v):
        try:
            return int(v) if v.strip() else None
        except Exception:
            return None

    # If API id provided and card already in collection – just bump quantity
    if api_id:
        existing = db.query(Card).filter(Card.api_id == api_id).first()
        if existing:
            existing.quantity += quantity
            db.commit()
            return RedirectResponse(f"/karte/{existing.id}", status_code=303)

    card = Card(
        api_id=api_id or None,
        name=name,
        set_name=set_name or None,
        number=number or None,
        rarity=rarity or None,
        hp=to_int(hp),
        types=types or None,
        image_url=image_url or None,
        image_url_hires=image_url_hires or None,
        market_price_market=to_float(market_price_market),
        condition=condition,
        quantity=quantity,
        purchase_price=to_float(purchase_price),
        is_foil=bool(is_foil),
        is_graded=bool(is_graded),
        grade_score=to_float(grade_score),
        grading_company=grading_company or None,
        notes=notes or None,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return RedirectResponse(f"/karte/{card.id}", status_code=303)


@app.get("/karte/{card_id}", response_class=HTMLResponse)
async def card_detail(card_id: int, request: Request, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(404, "Karte nicht gefunden")
    card.estimated_value = _card_value(card)
    attacks = _parse_json_field(card.attacks)
    weaknesses = _parse_json_field(card.weaknesses)
    resistances = _parse_json_field(card.resistances)
    return templates.TemplateResponse("card_detail.html", {
        "request": request,
        "card": card,
        "attacks": attacks,
        "weaknesses": weaknesses,
        "resistances": resistances,
        "condition_labels": CONDITION_LABELS,
        "condition_mult": CONDITION_MULTIPLIER,
    })


@app.get("/karte/{card_id}/bearbeiten", response_class=HTMLResponse)
async def edit_card_form(card_id: int, request: Request, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(404, "Karte nicht gefunden")
    return templates.TemplateResponse("card_form.html", {
        "request": request,
        "prefill": card.__dict__,
        "card_id": card_id,
        "conditions": CONDITIONS,
        "condition_labels": CONDITION_LABELS,
        "edit_mode": True,
    })


@app.post("/karte/{card_id}/bearbeiten")
async def edit_card(
    card_id: int,
    db: Session = Depends(get_db),
    condition: str = Form("NM"),
    quantity: int = Form(1),
    purchase_price: str = Form(""),
    is_foil: str = Form(""),
    is_graded: str = Form(""),
    grade_score: str = Form(""),
    grading_company: str = Form(""),
    notes: str = Form(""),
):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(404, "Karte nicht gefunden")

    def to_float(v):
        try:
            return float(v) if v.strip() else None
        except Exception:
            return None

    card.condition = condition
    card.quantity = quantity
    card.purchase_price = to_float(purchase_price)
    card.is_foil = bool(is_foil)
    card.is_graded = bool(is_graded)
    card.grade_score = to_float(grade_score)
    card.grading_company = grading_company or None
    card.notes = notes or None
    db.commit()
    return RedirectResponse(f"/karte/{card_id}", status_code=303)


@app.post("/karte/{card_id}/loeschen")
async def delete_card(card_id: int, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        db.delete(card)
        db.commit()
    return RedirectResponse("/", status_code=303)


@app.get("/vergleich", response_class=HTMLResponse)
async def compare_page(
    request: Request,
    ids: str = "",
    db: Session = Depends(get_db),
):
    all_cards = db.query(Card).order_by(Card.name).all()
    selected_cards = []
    if ids:
        id_list = [int(i) for i in ids.split(",") if i.strip().isdigit()]
        for cid in id_list:
            c = db.query(Card).filter(Card.id == cid).first()
            if c:
                c.estimated_value = _card_value(c)
                c.attacks_parsed = _parse_json_field(c.attacks)
                selected_cards.append(c)
    return templates.TemplateResponse("compare.html", {
        "request": request,
        "all_cards": all_cards,
        "selected_cards": selected_cards,
        "selected_ids": ids,
        "condition_labels": CONDITION_LABELS,
    })


@app.get("/statistiken", response_class=HTMLResponse)
async def statistics_page(request: Request, db: Session = Depends(get_db)):
    cards = db.query(Card).all()
    stats = _collection_stats(cards)
    for c in cards:
        c.estimated_value = _card_value(c)

    # Top 10 most valuable
    sorted_by_value = sorted(
        [c for c in cards if c.estimated_value],
        key=lambda c: c.estimated_value,
        reverse=True
    )[:10]

    # By type
    types_count: dict[str, int] = {}
    for c in cards:
        for t in (c.types or "").split(","):
            t = t.strip()
            if t:
                types_count[t] = types_count.get(t, 0) + c.quantity

    return templates.TemplateResponse("statistics.html", {
        "request": request,
        "stats": stats,
        "top_cards": sorted_by_value,
        "types_count": types_count,
        "condition_labels": CONDITION_LABELS,
    })


# ─────────────────────────────────────────────────────────────────────────────
# JSON API endpoints (for JS fetch)
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/api/karten")
async def api_list_cards(db: Session = Depends(get_db)):
    cards = db.query(Card).all()
    result = []
    for c in cards:
        d = {col.name: getattr(c, col.name) for col in c.__table__.columns}
        d["estimated_value"] = _card_value(c)
        result.append(d)
    return result


@app.get("/api/suche")
async def api_search(q: str = "", page: int = 1):
    if not q:
        return {"cards": [], "total": 0}
    return await pokemon_api.search_cards(q, page=page)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
