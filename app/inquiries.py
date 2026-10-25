"""Validate event flower quote requests."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from app.orders import business_today

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_inquiry(
    form: dict[str, Any],
    data: dict[str, str],
    item_name: str,
) -> tuple[str, str, str]:
    """Return (subject, body, customer_email) or raise ValueError."""
    lines = [f"New event request: {item_name}", ""]
    today = business_today()
    customer_email = ""

    for field in form["fields"]:
        name = field["name"]
        raw = (data.get(name) or "").strip()
        maxlength = field.get("maxlength")
        if maxlength and len(raw) > int(maxlength):
            raise ValueError(f"{field['label']} must be {maxlength} characters or fewer.")
        if field.get("required") and not raw:
            raise ValueError(f"Please fill in {field['label'].lower()}.")
        if raw and field["type"] == "email":
            if not _EMAIL.match(raw):
                raise ValueError("Please enter a valid email address.")
            customer_email = raw
            lines.append(f"{field['label']}: {raw}")
            continue
        if raw and field["type"] == "tel":
            digits = re.sub(r"\D", "", raw)
            if len(digits) < 10 or len(digits) > 15:
                raise ValueError("Please enter a valid phone number.")
        if raw and field["type"] == "date":
            try:
                chosen = datetime.strptime(raw, "%Y-%m-%d").date()
            except ValueError as exc:
                raise ValueError("Please choose a valid date of event.") from exc
            if chosen < today:
                raise ValueError("Please choose today or a later date.")
            lines.append(
                f"{field['label']}: {chosen.strftime('%A, %B')} {chosen.day}, {chosen.year}"
            )
            continue
        if raw:
            lines.append(f"{field['label']}: {raw}")

    subject = f"New event request: {item_name}"
    return subject, "\n".join(lines), customer_email
