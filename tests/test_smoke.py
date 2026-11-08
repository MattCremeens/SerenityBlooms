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

    async def test_thanksgiving_page_lists_each_arrangement(self):
        page = (await self.client.get("/shop/in-season")).text
        self.assertIn("Thanksgiving arrangements", page)
        self.assertIn("Tuesday, Nov. 24", page)
        self.assertIn('class="shop-detail-gallery"', page)
        self.assertIn('class="zoomable"', page)
        self.assertIn('id="photo-lightbox"', page)
        self.assertIn("thanksgiving_1.jpeg", page)
        self.assertIn("thanksgiving_2.jpeg", page)
        self.assertIn("thanksgiving_arrangements_2.jpeg", page)
        self.assertIn("trio_of_bud_vases_orange_yellow_burgandy.jpeg", page)
        self.assertIn("premium_vase_arrangement_blush_burgandy.jpeg", page)
        self.assertNotIn("Photo coming soon", page)
        self.assertIn("Continue to Venmo", page)
        self.assertNotIn("not available at this time", page)
        for label in (
            "Trio of bud vases (orange/yellow/burgundy)",
            "Trio of bud vases (blush/burgundy)",
            "Wrapped bouquet (orange/yellow/burgundy)",
            "Wrapped bouquet (blush/burgundy)",
            "Premium vase arrangement (orange/yellow/burgundy)",
            "Premium vase arrangement (blush/burgundy)",
        ):
            self.assertIn(label, page)

    async def test_portfolio_photos_can_be_enlarged(self):
        page = (await self.client.get("/portfolio")).text
        self.assertIn("portfolio_1.jpeg", page)
        self.assertIn('class="zoomable"', page)
        self.assertIn('id="photo-lightbox"', page)

    async def test_prom_gallery_photos_can_be_enlarged(self):
        page = (await self.client.get("/shop/prom-homecoming")).text
        self.assertIn("dance_flowers_1.jpeg", page)
        self.assertIn('class="zoomable"', page)
        self.assertIn('id="photo-lightbox"', page)

    async def test_thanksgiving_order_can_include_more_than_one_arrangement(self):
        with patch("app.main.send_order_email") as send:
            response = await self.client.post(
                "/shop/in-season/order",
                data={
                    "customer_name": "Ada Lovelace",
                    "customer_email": "ada@example.com",
                    "customer_phone": "2175550100",
                    "arrangements__bud-vases-warm": "1",
                    "arrangements__bouquet-blush": "2",
                },
                follow_redirects=False,
            )
        self.assertEqual(response.status_code, 303)
        self.assertIn("total=116", response.headers["location"])
        self.assertIn("pay=venmo", response.headers["location"])
        body = send.call_args.args[1]
        self.assertIn("Trio of bud vases (orange/yellow/burgundy): 1 × $36", body)
        self.assertIn("Wrapped bouquet (blush/burgundy): 2 × $40", body)
        self.assertIn("Total: $116", body)
        self.assertIn("Payment: Venmo", body)

    async def test_thanksgiving_order_requires_an_arrangement(self):
        with patch("app.main.send_order_email") as send:
            response = await self.client.post(
                "/shop/in-season/order",
                data={
                    "customer_name": "Ada Lovelace",
                    "customer_email": "ada@example.com",
                    "customer_phone": "2175550100",
                    "arrangements__bud-vases-warm": "0",
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Please choose at least one arrangement.", response.text)
        send.assert_not_called()


if __name__ == "__main__":
    unittest.main()
