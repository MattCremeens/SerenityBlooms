"""Site content — edit this file to update markets, flowers, and contact info."""

BUSINESS = {
    "name": "Serenity Blooms",
    "tagline": "Locally grown, freshly cut, arranged with care",
    "owner": "Heather Cremeens",
    "description": (
        "Hi, I’m Heather, the face behind the flowers here at Serenity Blooms. "
        "I’m so glad you’ve found my page! After several years of hobby gardening, "
        "in 2026 I decided to officially launch Serenity Blooms, a small business "
        "creating custom floral arrangements with the flowers I grow in my very own "
        "backyard here in Springfield, IL. My growing space is limited, but my vision is big!\n\n"
        "Serenity Blooms specializes in using organic gardening practices to create fresh "
        "market bouquets and one-of-a-kind vase arrangements. We deliver locally and can "
        "create something to match just about any budget. We also use a combination of our "
        "locally grown stems and fresh flowers from the wholesaler to create bouquets and "
        "boutonnieres for dances and arrangements for small special events. Email me at "
        "serenitybloomsflowerco@gmail.com if you want to order something pretty today!"
    ),
    "phone": "(217) 259-3692",
    "phone_href": "tel:+12172593692",
    "email": "serenitybloomsflowerco@gmail.com",
    "email_href": "mailto:serenitybloomsflowerco@gmail.com",
    "venmo": {
        "username": "SerenityBloomsFlowerCo",
        "url": "https://venmo.com/u/SerenityBloomsFlowerCo",
    },
    "social": {
        "instagram": {
            "label": "Instagram",
            "url": "https://www.instagram.com/serenitybloomsflowerco/",
        },
        "facebook": {
            "label": "Facebook",
            "url": "https://www.facebook.com/serenitybloomsflowerco",
        },
    },
}

SUBSCRIPTION_FORM = {
    "title": "Subscribe",
    "payment": "venmo",
    "submit_label": "Continue to Venmo",
    "confirmation": "Thank you! Your subscription was emailed to us.",
    "fields": [
        {
            "name": "customer_name",
            "label": "Your name",
            "type": "text",
            "required": True,
        },
        {
            "name": "customer_email",
            "label": "Your email",
            "type": "email",
            "required": True,
        },
        {
            "name": "customer_phone",
            "label": "Phone number",
            "type": "tel",
            "required": True,
        },
        {
            "name": "plan",
            "label": "Plan",
            "hint": "Select one",
            "type": "select",
            "required": True,
            "options": [
                {"value": "weekly", "label": "Weekly for 6 weeks: $150", "price": 150},
                {"value": "biweekly", "label": "Bi-weekly for 6 weeks: $75", "price": 75},
            ],
        },
        {
            "name": "recipient_name",
            "label": "Recipient's name",
            "hint": "If this is a gift",
            "type": "text",
            "required": False,
        },
        {
            "name": "recipient_phone",
            "label": "Recipient's phone number",
            "type": "tel",
            "required": False,
        },
    ],
}

IN_SEASON_FORM = {
    "title": "In-season locally grown flowers order form",
    "fields": [
        {
            "name": "customer_name",
            "label": "Your name",
            "type": "text",
            "required": True,
        },
        {
            "name": "customer_email",
            "label": "Your email",
            "type": "email",
            "required": True,
        },
        {
            "name": "customer_phone",
            "label": "Phone number",
            "type": "tel",
            "required": True,
        },
        {
            "name": "style",
            "label": "Style",
            "hint": "Select one",
            "type": "select",
            "required": True,
            "options": [
                {"value": "wrapped-bouquet", "label": "Wrapped bouquet: $25", "price": 25},
                {"value": "premium-vase", "label": "Premium vase arrangement: $35", "price": 35},
            ],
        },
        {
            "name": "color_palette",
            "label": "Color palette",
            "hint": "Select one",
            "type": "select",
            "required": True,
            "options": [
                {"value": "bright", "label": "Bright and colorful"},
                {"value": "pastel", "label": "Pastel"},
            ],
        },
        {
            "name": "needed_date",
            "label": "Date needed",
            "hint": "Please allow at least 24 hours",
            "type": "date",
            "required": True,
        },
        {
            "name": "needed_time",
            "label": "Time needed",
            "type": "time_select",
            "required": True,
        },
        {
            "name": "fulfillment",
            "label": "Pick up or delivery",
            "hint": "Select one",
            "type": "select",
            "required": True,
            "options": [
                {"value": "pickup", "label": "Pickup: no additional charge", "price": 0},
                {"value": "delivery", "label": "Delivery within 15 miles: $10", "price": 10},
            ],
        },
        {
            "name": "recipient_name",
            "label": "Recipient name",
            "type": "text",
            "required": False,
        },
        {
            "name": "delivery_address",
            "label": "Delivery address",
            "hint": "Required if you choose delivery",
            "type": "text",
            "required": False,
        },
        {
            "name": "message",
            "label": "Custom message",
            "hint": "Up to 100 characters",
            "type": "textarea",
            "required": False,
            "maxlength": 100,
        },
        {
            "name": "quantity",
            "label": "Quantity",
            "type": "select",
            "required": True,
            "options": [
                {"value": str(n), "label": str(n)} for n in range(1, 6)
            ],
        },
    ],
}

SHOP_ITEMS = [
    {
        "slug": "in-season",
        "name": "In-season locally grown flowers",
        "image": "in_season.jpeg",
        "alt": "In-season locally grown flowers",
        "description": [
            "During late spring through early fall, we offer market bouquets and specialty arrangements. Reach out to request something created just for you!",
        ],
        "form": IN_SEASON_FORM,
    },
    {
        "slug": "summer-subscription",
        "name": "Summer flower subscription",
        "image": "summer_flowers.jpeg",
        "alt": "Summer flower subscription",
        "prices": [
            {"label": "Weekly for 6 weeks", "amount": "$150"},
            {"label": "Bi-weekly for 6 weeks", "amount": "$75"},
        ],
        "description": [
            "This is the perfect gift for someone you love! Beginning in July 2027, we will offer 6 weeks of beautiful, fresh-cut bouquets to be picked up weekly or bi-weekly on Friday evenings at our home near Rochester, IL. The bouquets will be different every week, but some of the flowers you can expect to see are celosia, zinnias, gomphrena, echinacea, lavender, and so much more!",
            "These bouquets are fuller than our traditional wrapped bouquets and will be full of our most beautiful blooms each week.",
            "We expect this subscription to begin the second week of July, but it is somewhat dependent on the weather. We will notify you the week before the subscription begins and keep in touch throughout the growing season about any changes in pickup dates.",
            "We cannot refund missed pickups, but you may transfer your weekly bouquet to a friend or family member! If we experience crop loss or weather causes issues with our flowers, we will supplement with our next available crop.",
            "* If this is being gifted, we will email you a certificate to present to the recipient."
        ],
        "form": SUBSCRIPTION_FORM,
    },
    {
        "slug": "event-flowers",
        "name": "Event Flowers",
        "image": "event_flowers.jpeg",
        "alt": "Event flowers",
        "description": [
            "We would love to help make your small event more special with beautiful arrangements from Serenity Blooms. From May-September we can offer our seasonal fresh-cut flowers, and in the colder months, we can source fresh flowers from our wholesaler. We would love to help you bring your vision to life! Reach out to us at serenitybloomsflowerco@gmail.com to receive a quote.",
        ],
        "cta": "Email for a quote",
    },
    {
        "slug": "prom-homecoming",
        "name": "Prom/Homecoming flowers",
        "image": "dance_flower_main_image.jpeg",
        "alt": "Prom/Homecoming flowers",
        "description": [
            "We offer custom hand-tied bouquets and boutonnieres using a combination of fresh flowers from both the wholesaler and our garden. We feel this approach allows us to design beautiful arrangements that perfectly complement your formal wear.",
        ],
        "cta": "Email to order",
    },
]

SHOP_BY_SLUG = {item["slug"]: item for item in SHOP_ITEMS}

FLOWERS_FOR_SALE = [
    {
        "name": "Seasonal Market Bouquets",
        "description": "Hand-tied mixed bouquets featuring whatever is freshest from the garden.",
        "season": "Year-round",
    },
    {
        "name": "Sunflowers",
        "description": "Cheerful, long-stemmed sunflowers — a market favorite every summer.",
        "season": "June – September",
    },
    {
        "name": "Zinnias",
        "description": "Vibrant, long-lasting blooms in a rainbow of colors.",
        "season": "July – October",
    },
    {
        "name": "Dahlias",
        "description": "Lush, layered blooms in rich tones — perfect for statement arrangements.",
        "season": "August – October",
    },
    {
        "name": "Snapdragons & Stock",
        "description": "Fragrant, vertical stems that add height and texture to any bouquet.",
        "season": "Spring – Fall",
    },
    {
        "name": "Specialty Bundles",
        "description": "Limited bundles of focal flowers, greenery, and seasonal accents.",
        "season": "Varies — follow us on Instagram for updates",
    },
]
