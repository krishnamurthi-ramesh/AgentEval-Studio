"""
Community Eval Pack Library for AgentEval Studio.
Handles discovery, loading, forking, and saving of reusable evaluation packs.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from agenteval.models import EvalPack

PACKS_DIR = Path(__file__).parent / "packs"


def list_packs() -> List[Dict[str, Any]]:
    """List all available Eval Packs in the library."""
    packs_metadata = []
    if not PACKS_DIR.exists():
        return packs_metadata

    for file_path in PACKS_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                packs_metadata.append({
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "version": data.get("version", "1.0.0"),
                    "category": data.get("category", "general"),
                    "description": data.get("description", ""),
                    "author": data.get("author", "community"),
                    "cases_count": len(data.get("cases", [])),
                    "tags": data.get("tags", []),
                    "file_name": file_path.name
                })
        except Exception:
            continue
    return packs_metadata


def load_pack(pack_identifier: str) -> EvalPack:
    """
    Load an EvalPack by ID, filename, or slug.
    Example: load_pack("customer_support_banking") or load_pack("pack_banking_001")
    """
    if not PACKS_DIR.exists():
        raise FileNotFoundError(f"Packs directory not found: {PACKS_DIR}")

    # Check direct filename
    target_file = PACKS_DIR / f"{pack_identifier}.json"
    if target_file.exists():
        with open(target_file, "r", encoding="utf-8") as f:
            return EvalPack.model_validate(json.load(f))

    # Search through all pack files
    for file_path in PACKS_DIR.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data.get("id") == pack_identifier or file_path.stem == pack_identifier:
                return EvalPack.model_validate(data)

    raise ValueError(f"EvalPack '{pack_identifier}' not found in library.")


def save_pack(pack: EvalPack, custom_dir: Optional[Path] = None) -> Path:
    """Save an EvalPack to the library or a custom directory."""
    target_dir = custom_dir or PACKS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{pack.category}_{pack.id}.json"
    file_path = target_dir / filename

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(pack.model_dump(), f, indent=2)

    return file_path
