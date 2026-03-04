"""Pokemon TCG API client for fetching card data."""

import json
import logging
from typing import Optional
import httpx

logger = logging.getLogger(__name__)

POKEMON_TCG_API_BASE = "https://api.pokemontcg.io/v2"


def _safe_float(val) -> Optional[float]:
    try:
        return float(val) if val is not None else None
    except (TypeError, ValueError):
        return None


def _parse_prices(tcgplayer: dict) -> dict:
    prices = {}
    for variant in ("normal", "holofoil", "reverseHolofoil", "1stEditionHolofoil"):
        p = (tcgplayer.get("prices") or {}).get(variant)
        if p:
            prices = p
            break
    return prices


def _card_from_api(data: dict) -> dict:
    """Map raw API card data to our internal schema."""
    attacks = data.get("attacks") or []
    weaknesses = data.get("weaknesses") or []
    resistances = data.get("resistances") or []
    retreat = data.get("convertedRetreatCost") or 0

    tcgplayer = data.get("tcgplayer") or {}
    prices = _parse_prices(tcgplayer)

    images = data.get("images") or {}

    return {
        "api_id": data.get("id"),
        "name": data.get("name", "Unknown"),
        "set_name": (data.get("set") or {}).get("name"),
        "set_id": (data.get("set") or {}).get("id"),
        "number": data.get("number"),
        "rarity": data.get("rarity"),
        "supertype": data.get("supertype"),
        "subtypes": ", ".join(data.get("subtypes") or []),
        "hp": int(data["hp"]) if data.get("hp") and str(data["hp"]).isdigit() else None,
        "types": ", ".join(data.get("types") or []),
        "attacks": json.dumps(attacks),
        "weaknesses": json.dumps(weaknesses),
        "resistances": json.dumps(resistances),
        "retreat_cost": retreat,
        "image_url": images.get("small"),
        "image_url_hires": images.get("large"),
        "market_price_low": _safe_float(prices.get("low")),
        "market_price_mid": _safe_float(prices.get("mid")),
        "market_price_high": _safe_float(prices.get("high")),
        "market_price_market": _safe_float(prices.get("market")),
    }


async def search_cards(query: str, page: int = 1, page_size: int = 20) -> dict:
    """Search for Pokemon cards by name."""
    params = {
        "q": f'name:"{query}*"',
        "page": page,
        "pageSize": page_size,
        "orderBy": "name",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(f"{POKEMON_TCG_API_BASE}/cards", params=params)
            resp.raise_for_status()
            data = resp.json()
            return {
                "cards": [_card_from_api(c) for c in data.get("data", [])],
                "total": data.get("totalCount", 0),
                "page": page,
                "page_size": page_size,
            }
        except Exception as e:
            logger.error("Pokemon TCG API search failed: %s", e)
            return {"cards": [], "total": 0, "page": page, "page_size": page_size}


async def get_card_by_id(card_id: str) -> Optional[dict]:
    """Fetch a single card by its API id."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(f"{POKEMON_TCG_API_BASE}/cards/{card_id}")
            resp.raise_for_status()
            data = resp.json()
            return _card_from_api(data.get("data", {}))
        except Exception as e:
            logger.error("Pokemon TCG API get card failed: %s", e)
            return None


async def get_sets() -> list[dict]:
    """Fetch all available card sets."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(f"{POKEMON_TCG_API_BASE}/sets", params={"orderBy": "-releaseDate"})
            resp.raise_for_status()
            data = resp.json()
            sets = []
            for s in data.get("data", []):
                images = s.get("images") or {}
                sets.append({
                    "id": s.get("id"),
                    "name": s.get("name"),
                    "series": s.get("series"),
                    "total": s.get("total"),
                    "release_date": s.get("releaseDate"),
                    "symbol_url": images.get("symbol"),
                    "logo_url": images.get("logo"),
                })
            return sets
        except Exception as e:
            logger.error("Pokemon TCG API get sets failed: %s", e)
            return []
