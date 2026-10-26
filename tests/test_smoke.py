"""Basic HTTP and deployment checks (run with `python -m unittest discover -s tests`)."""

import unittest
from pathlib import Path
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient

from app.config import SHOP_BY_SLUG
from app.main import app
from app.orders import business_today, earliest_order_date


class SiteSmokeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_home_and_portfolio(self):
        for path in ("/", "/portfolio", "/shop/event-flowers", "/shop/summer-subscription"):
            with self.subTest(path=path):
                response = await self.client.get(path)
                self.assertEqual(response.status_code, 200)

    def test_static_image_exists(self):
        self.assertTrue((Path(__file__).resolve().parents[1] / "app/static/css/images/logo.jpg").is_file())

    async def test_unknown_shop_item(self):
        self.assertEqual((await self.client.get("/shop/not-an-item")).status_code, 404)

    async def test_invalid_inquiry_does_not_send_email(self):
        with patch("app.main.send_order_email") as send:
            response = await self.client.post("/shop/event-flowers/inquiry", data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Please fill in", response.text)
        send.assert_not_called()

    def test_business_dates_are_local(self):
        self.assertEqual((earliest_order_date() - business_today()).days, 1)

    async def test_subscription_form_is_hidden_until_sales_open(self):
        item = SHOP_BY_SLUG["summer-subscription"]
        self.assertFalse(item["available"])
        self.assertEqual(item["form"]["submit_label"], "Continue to Venmo")

        page = (await self.client.get("/shop/summer-subscription")).text
        self.assertIn("Sales open November 27, 2026.", page)
        self.assertIn("perfect gift", page)
        self.assertNotIn("Continue to Venmo", page)
        self.assertNotIn('class="order-form"', page)

        with patch("app.main.send_order_email") as send:
            response = await self.client.post(
                "/shop/summer-subscription/order",
                data={"customer_name": "Ada", "plan": "weekly"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Sales open November 27, 2026.", response.text)
        send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
