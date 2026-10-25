from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool

from app.config import BUSINESS, FLOWERS_FOR_SALE, SHOP_BY_SLUG, SHOP_ITEMS
from app.emailer import EmailError, send_order_email
from app.inquiries import validate_inquiry
from app.orders import parse_total, prepare_form, validate_order, venmo_pay_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "static" / "css" / "images"

app = FastAPI(title=BUSINESS["name"])
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def shop_page(
    request: Request,
    item: dict,
    order_status: str | None = None,
    order_error: str | None = None,
    order_total: int | None = None,
    payment_choice: str | None = None,
    submitted: dict[str, str] | None = None,
) -> HTMLResponse:
    available = item.get("available", True)
    form = prepare_form(item["form"]) if item.get("form") and available else None
    if form:
        for field in form["fields"]:
            if submitted:
                field["value"] = (submitted.get(field["name"]) or "").strip()
            controller = field.get("depends_on")
            if controller:
                current = (submitted or {}).get(controller, "")
                field["hidden"] = str(current).strip() != field.get("depends_value")
    venmo = BUSINESS.get("venmo")
    pay_note = f"{item['name']} order"
    pay_url = (
        venmo_pay_url(venmo["username"], order_total, pay_note)
        if venmo and order_total
        else (venmo["url"] if venmo else None)
    )
    if item.get("form", {}).get("payment") == "venmo":
        payment_choice = "venmo"
    elif payment_choice not in {"venmo", "pickup"}:
        payment_choice = None
    return templates.TemplateResponse(
        request,
        "shop_item.html",
        {
            "business": BUSINESS,
            "item": item,
            "form": form,
            "order_status": order_status,
            "order_error": order_error,
            "order_total": order_total,
            "payment_choice": payment_choice,
            "venmo_pay_url": pay_url,
            "venmo_note": pay_note,
            "gallery": gallery_images(item.get("gallery_prefix")),
        },
    )


def gallery_images(prefix: str | None) -> list[str]:
    if not prefix or not IMAGE_DIR.is_dir():
        return []

    def sort_key(name: str) -> tuple[int, str]:
        number = Path(name).stem.rsplit("_", 1)[-1]
        return (int(number) if number.isdigit() else 0, name.lower())

    return sorted(
        (
            path.name
            for path in IMAGE_DIR.iterdir()
            if path.is_file() and path.name.lower().startswith(prefix.lower())
        ),
        key=sort_key,
    )


def carousel_images() -> list[str]:
    if not IMAGE_DIR.is_dir():
        return []
    return sorted(
        path.name
        for path in IMAGE_DIR.iterdir()
        if path.is_file() and path.name.lower().startswith("carousel_")
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "business": BUSINESS,
            "shop": SHOP_ITEMS,
            "flowers": FLOWERS_FOR_SALE,
            "carousel": carousel_images(),
        },
    )


@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "portfolio.html",
        {
            "business": BUSINESS,
            "photos": gallery_images("portfolio_"),
        },
    )


@app.get("/shop/{slug}", response_class=HTMLResponse)
async def shop_item(request: Request, slug: str) -> HTMLResponse:
    item = SHOP_BY_SLUG.get(slug)
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    return shop_page(
        request,
        item,
        order_status=request.query_params.get("order"),
        order_total=parse_total(request.query_params.get("total")),
        payment_choice=request.query_params.get("pay"),
    )


@app.post("/shop/{slug}/order", response_class=HTMLResponse)
async def submit_order(request: Request, slug: str) -> HTMLResponse:
    item = SHOP_BY_SLUG.get(slug)
    if item is None or not item.get("form") or item["form"].get("kind") == "inquiry":
        raise HTTPException(status_code=404, detail="Not found")
    if not item.get("available", True):
        return shop_page(request, item)

    posted = await request.form()
    if str(posted.get("company") or "").strip():
        return RedirectResponse(url=f"/shop/{slug}?order=sent", status_code=303)

    form = prepare_form(item["form"])
    data = {key: str(value) for key, value in posted.items()}
    try:
        subject, body, reply_to, total = validate_order(form, data, item["name"])
        await run_in_threadpool(send_order_email, subject, body, reply_to)
    except ValueError as exc:
        return shop_page(request, item, order_error=str(exc))
    except EmailError as exc:
        return shop_page(request, item, order_error=str(exc))

    payment = data.get("payment_method") or "venmo"
    if form.get("payment") == "venmo" or payment not in {"venmo", "pickup"}:
        payment = "venmo"
    return RedirectResponse(
        url=f"/shop/{slug}?order=sent&total={total}&pay={payment}",
        status_code=303,
    )


@app.post("/shop/{slug}/inquiry", response_class=HTMLResponse)
async def submit_inquiry(request: Request, slug: str) -> HTMLResponse:
    item = SHOP_BY_SLUG.get(slug)
    form = item.get("form") if item else None
    if item is None or not form or form.get("kind") != "inquiry":
        raise HTTPException(status_code=404, detail="Not found")

    posted = await request.form()
    if str(posted.get("company") or "").strip():
        return RedirectResponse(url=f"/shop/{slug}?order=sent", status_code=303)

    data = {key: str(value) for key, value in posted.items()}
    try:
        subject, body, reply_to = validate_inquiry(form, data, item["name"])
        await run_in_threadpool(send_order_email, subject, body, reply_to)
    except ValueError as exc:
        return shop_page(request, item, order_error=str(exc), submitted=data)
    except EmailError as exc:
        return shop_page(request, item, order_error=str(exc), submitted=data)

    return RedirectResponse(url=f"/shop/{slug}?order=sent", status_code=303)
