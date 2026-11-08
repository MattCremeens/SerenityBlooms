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
        "serenitybloomsflowerco@gmail.com with any questions or to discuss a special order."
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
    "title": "Order form",
    "payment": "venmo",
    "submit_label": "Continue to Venmo",
    "confirmation": "Thank you! Your order was emailed to us.",
    "fields": [
        {
            "name": "customer_name",
            "label": "Your name",
            "type": "text",
            "required": True,
            "autocomplete": "name",
        },
        {
            "name": "customer_email",
            "label": "Your email",
            "type": "email",
            "required": True,
            "autocomplete": "email",
        },
        {
            "name": "customer_phone",
            "label": "Phone number",
            "type": "tel",
            "required": True,
            "autocomplete": "tel",
        },
        {
            "name": "arrangements",
            "label": "Choice of flowers",
            "hint": "Set a quantity for each arrangement you want. You can order more than one.",
            "type": "products",
            "required": True,
            "max_quantity": 10,
            "options": [
                {
                    "value": "bud-vases-warm",
                    "label": "Trio of bud vases (orange/yellow/burgundy)",
                    "price": 36,
                    "image": "trio_of_bud_vases_orange_yellow_burgandy.jpeg",
                },
                {
                    "value": "bud-vases-blush",
                    "label": "Trio of bud vases (blush/burgundy)",
                    "price": 36,
                    "image": "trio_of_bud_vases_blush_burgandy.jpeg",
                },
                {
                    "value": "bouquet-warm",
                    "label": "Wrapped bouquet (orange/yellow/burgundy)",
                    "price": 40,
                    "image": "wrapped_bouquet_orange_yellow_burgandy.jpeg",
                },
                {
                    "value": "bouquet-blush",
                    "label": "Wrapped bouquet (blush/burgundy)",
                    "price": 40,
                    "image": "wrapped_bouquet_blush_burgandy.jpeg",
                },
                {
                    "value": "vase-warm",
                    "label": "Premium vase arrangement (orange/yellow/burgundy)",
                    "price": 50,
                    "image": "premium_vase_arrangement_orange_yellow_burgandy.jpeg",
                },
                {
                    "value": "vase-blush",
                    "label": "Premium vase arrangement (blush/burgundy)",
                    "price": 50,
                    "image": "premium_vase_arrangement_blush_burgandy.jpeg",
                },
            ],
        },
    ],
}

EVENT_INQUIRY_FORM = {
    "kind": "inquiry",
    "title": "Request a quote",
    "submit_label": "Send request",
    "confirmation": "Thank you! Your request was emailed to us, and we'll be in touch soon.",
    "fields": [
        {
            "name": "customer_name",
            "label": "Name",
            "type": "text",
            "required": True,
            "maxlength": 80,
            "autocomplete": "name",
        },
        {
            "name": "customer_phone",
            "label": "Phone number",
            "type": "tel",
            "required": True,
            "maxlength": 30,
            "autocomplete": "tel",
        },
        {
            "name": "customer_email",
            "label": "Email address",
            "type": "email",
            "required": True,
            "maxlength": 120,
            "autocomplete": "email",
        },
        {
            "name": "event_type",
            "label": "Type of event",
            "type": "text",
            "required": True,
            "maxlength": 80,
        },
        {
            "name": "event_date",
            "label": "Date of event",
            "type": "date",
            "required": True,
            "min": "today",
        },
    ],
}

SHOP_ITEMS = [
    {
        "slug": "in-season",
        "name": "Thanksgiving arrangements",
        "image": "thanksgiving_arrangements.jpeg",
        "gallery": [
            "thanksgiving_1.jpeg",
            "wrapped_bouquet_orange_yellow_burgandy.jpeg",
            "trio_of_bud_vases_orange_yellow_burgandy.jpeg",
            "thanksgiving_2.jpeg",
            "trio_of_bud_vases_blush_burgandy.jpeg",
            "thanksgiving_arrangements_2.jpeg",
            "wrapped_bouquet_blush_burgandy.jpeg",
            "premium_vase_arrangement_orange_yellow_burgandy.jpeg",
            "premium_vase_arrangement_blush_burgandy.jpeg",
        ],
        "alt": "Thanksgiving arrangements",
        "description": [
            "Our fall arrangements are available for preorder just in time to grace your holiday table or be gifted as a special hostess gift! Choose from a trio of bud vases, wrapped bouquets, or premium vase arrangements in either a dreamy color combination of blush, burgundy and cream, OR classic warm fall colors of orange, yellow, burgundy and cream. All arrangements will include a premium mix of roses, hypericum berries, eucalyptus, and other seasonal flowers. (Please note that we always do our best to match orders to what is pictured, but due to flower availability some substitutions may need to be made.)",
            "These flowers will be available for pickup at our home near Rochester, IL on Tuesday, Nov. 24 from 5-7 pm. After you order you will receive a confirmation email with our address. If you are interested in local delivery for just $10, email serenitybloomsflowerco@gmail.com to see if you are within our delivery range. Happy Thanksgiving!",
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
            "This is the perfect gift for someone you love! Beginning in July 2027, we will offer 6 weeks of beautiful, fresh-cut bouquets to be picked up weekly or bi-weekly on Friday evenings at our home near Rochester, IL. The bouquets will be different every week, but some of the flowers you can expect to see are celosia, zinnias, gomphrena, basil, lavender, and so much more!",
            "These bouquets are fuller than our traditional wrapped bouquets and will be full of our most beautiful blooms each week.",
            "We expect this subscription to begin the first week of July, but it is somewhat dependent on the weather. We will notify you the week before the subscription begins and keep in touch throughout the growing season about any changes in pickup dates.",
            "We cannot refund missed pickups, but you may transfer your weekly bouquet to a friend or family member! If we experience crop loss or the weather causes issues with our flowers, we will supplement with our next available crop.",
            "If you live in Springfield or one of the surrounding communities and would like to add on delivery for $10 per bouquet, please email me at serenitybloomsflowerco@gmail.com to see if you live within our range.",
            "* If this is being gifted, we will email you a certificate to present to the recipient."
        ],
        "available": False,
        "closed_note": "Sales open November 27, 2026.",
        "form": SUBSCRIPTION_FORM,
    },
    {
        "slug": "event-flowers",
        "name": "Event flowers",
        "image": "event_flowers.jpeg",
        "alt": "Event flowers",
        "description": [
            "We would love to help make your small event more special with beautiful arrangements from Serenity Blooms. From May-September we can offer our seasonal fresh-cut flowers, and in the colder months, we can source fresh flowers from our wholesaler. We would love to help you bring your vision to life! Tell us a little about your event below, and we'll follow up to gather more details and to discuss a quote.",
        ],
        "form": EVENT_INQUIRY_FORM,
    },
    {
        "slug": "prom-homecoming",
        "name": "Prom/Homecoming flowers",
        "image": "dance_flower_main_image.jpeg",
        "gallery_prefix": "dance_flowers_",
        "alt": "Prom/Homecoming flowers",
        "description": [
            "We offer custom bouquets, corsages, boutonnieres, and pocket squares using a combination of fresh flowers from both the wholesaler and our garden. We feel this approach allows us to design beautiful arrangements that perfectly complement your formal wear.",
        ],
        "notice": "Prom orders will open up in the Spring.",
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
