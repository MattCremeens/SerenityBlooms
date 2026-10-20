"""Build and validate shop order forms."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any
from urllib.parse import urlencode

from app.config import BUSINESS


def earliest_order_date():
    return datetime.now().date() + timedelta(days=1)


def time_options() -> list[dict[str, str]]:
    options = []
    for hour in range(8, 19):
        for minute in (0, 30):
            if hour == 18 and minute == 30:
                break
            value = f"{hour:02d}:{minute:02d}"
            suffix = "AM" if hour < 12 else "PM"
            display_hour = hour % 12 or 12
            label = f"{display_hour}:{minute:02d} {suffix}"
            options.append({"value": value, "label": label})
    return options


def prepare_form(form: dict[str, Any]) -> dict[str, Any]:
    prepared = deepcopy(form)
    for field in prepared["fields"]:
        if field["type"] == "date":
            field["min"] = earliest_order_date().isoformat()
        elif field["type"] == "time_select":
            field["type"] = "select"
            field["options"] = time_options()
    return prepared


def venmo_pay_url(username: str, amount: int, note: str) -> str:
    query = urlencode(
        {
            "txn": "pay",
            "amount": f"{amount:.2f}",
            "note": note,
        }
    )
    return f"https://venmo.com/{username}?{query}"


def parse_total(value: str | None) -> int | None:
    if not value:
        return None
    try:
        amount = int(value)
    except ValueError:
        return None
    if 1 <= amount <= 1000:
        return amount
    return None


def _option_map(field: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(option["value"]): option for option in field.get("options", [])}


def validate_order(
    form: dict[str, Any],
    data: dict[str, str],
    item_name: str,
) -> tuple[str, str, str | None, int]:
    """Return (subject, body, customer_email, estimated_total) or raise ValueError."""
    lines = [f"New order: {item_name}", ""]
    style_price = 0
    delivery_price = 0
    quantity = 1
    customer_email: str | None = None
    fulfillment = ""

    for field in form["fields"]:
        name = field["name"]
        raw = (data.get(name) or "").strip()
        if field.get("required") and not raw:
            raise ValueError(f"Please fill in {field['label'].lower()}.")

        maxlength = field.get("maxlength")
        if maxlength and len(raw) > maxlength:
            raise ValueError(f"{field['label']} must be {maxlength} characters or fewer.")

        if field["type"] == "select":
            options = _option_map(field)
            if raw not in options:
                raise ValueError(f"Please choose a valid option for {field['label'].lower()}.")
            option = options[raw]
            label = option["label"]
            if name == "fulfillment":
                delivery_price = int(option.get("price") or 0)
                fulfillment = raw
            elif name == "quantity":
                quantity = int(raw)
            elif "price" in option:
                style_price = int(option.get("price") or 0)
            lines.append(f"{field['label']}: {label}")
        elif field["type"] == "email":
            if "@" not in raw or "." not in raw:
                raise ValueError("Please enter a valid email address.")
            customer_email = raw
            lines.append(f"{field['label']}: {raw}")
        elif field["type"] == "date":
            try:
                chosen = datetime.strptime(raw, "%Y-%m-%d").date()
            except ValueError as exc:
                raise ValueError("Please choose a valid date.") from exc
            if chosen < earliest_order_date():
                raise ValueError("Please allow at least 24 hours.")
            lines.append(
                f"{field['label']}: {chosen.strftime('%A, %B')} {chosen.day}, {chosen.year}"
            )
        else:
            if name == "delivery_address" and fulfillment == "delivery" and not raw:
                raise ValueError("Please enter a delivery address.")
            if name == "delivery_address" and fulfillment != "delivery":
                continue
            if raw:
                lines.append(f"{field['label']}: {raw}")

    estimated = style_price * quantity + delivery_price
    lines.append("")
    if form.get("payment") == "venmo":
        if estimated < 1:
            raise ValueError("Please choose a plan.")
        lines.append(f"Total: ${estimated}")
        lines.append(f"Payment: Venmo to @{BUSINESS['venmo']['username']}")
    else:
        lines.append(f"Estimated total: ${estimated}")
        lines.append(
            "This total is an estimate based on the selected style, quantity, and pickup or delivery."
        )
        payment = (data.get("payment_method") or "").strip()
        if payment == "pickup":
            lines.append("Payment: Pay at pickup")
        else:
            lines.append(
                f"Payment: Venmo to @{BUSINESS['venmo']['username']}"
            )

    subject = f"New order: {item_name}"
    return subject, "\n".join(lines), customer_email, estimated
