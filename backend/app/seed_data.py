"""Seed catalog and reviews for VIKINGS storefront."""

PRODUCTS_SEED = [
    {"name": "Valhalla Performance Trunk", "cat": "Trunks", "price": 1299, "old_price": None, "badge": "Bestseller", "rating": 4.9, "review_count": 312, "img": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=700&q=90&fit=crop&crop=top", "fabric": "95% Modal, 5% Elastane", "fabric_type": "Modal", "color": "Charcoal", "tags": ["Moisture Wicking", "4-Way Stretch", "Anti-Chafe"], "desc": "The trunk that started it all. Micro-modal fabric that feels like a second skin — engineered for warriors who refuse to compromise on comfort, from boardroom to battlefield."},
    {"name": "Odin Classic Brief — 3 Pack", "cat": "Briefs", "price": 1999, "old_price": None, "badge": "New", "rating": 4.8, "review_count": 189, "img": "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1512484776495-a09d92e87c3b?w=700&q=90&fit=crop&crop=top", "fabric": "100% Pima Cotton", "fabric_type": "Pima Cotton", "color": "White", "tags": ["Tagless", "Breathable", "Value Pack"], "desc": "Three briefs. Infinite comfort. 100% Pima cotton that gets softer with every wash — because excellence should compound over time, just like your ambition."},
    {"name": "Thor Boxer Shorts", "cat": "Boxers", "price": 824, "old_price": 1099, "badge": "25% OFF", "rating": 4.6, "review_count": 97, "img": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=700&q=90&fit=crop&crop=top", "fabric": "100% Combed Cotton", "fabric_type": "Combed Cotton", "color": "Navy", "tags": ["Relaxed Fit", "Breathable", "Odor Control"], "desc": "Relaxed enough for rest days. Resilient enough for everything else. Combed cotton so fine it rivals silk, at a price that respects your intelligence."},
    {"name": "Fenrir V-Neck Undershirt", "cat": "Undershirts", "price": 799, "old_price": None, "badge": None, "rating": 4.9, "review_count": 224, "img": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1618354691792-d1d42acfd860?w=700&q=90&fit=crop&crop=top", "fabric": "92% Micro-Modal, 8% Spandex", "fabric_type": "Modal", "color": "White", "tags": ["Invisible Layer", "Stay-Fresh", "Ultra Soft"], "desc": "Invisible confidence. The undershirt that disappears beneath dress shirts while delivering all-day freshness. Your secret weapon for commanding every room you enter."},
    {"name": "Ragnarok Thermal Set", "cat": "Thermal", "price": 2499, "old_price": None, "badge": "Winter Pick", "rating": 4.9, "review_count": 78, "img": "https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=700&q=90&fit=crop&crop=top", "fabric": "Double-Layer Merino Blend", "fabric_type": "Merino", "color": "Slate", "tags": ["Insulating", "Moisture Control", "Full Set"], "desc": "Face winter like a legend. Double-layer merino wool construction that traps warmth without the bulk — engineered for men who conquer mountains in boardrooms and beyond."},
    {"name": "Skald Boxer Brief", "cat": "Trunks", "price": 899, "old_price": 1199, "badge": "Popular", "rating": 4.7, "review_count": 445, "img": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1520975916090-3105956dac38?w=700&q=90&fit=crop&crop=top", "fabric": "88% Modal, 12% Elastane", "fabric_type": "Modal", "color": "Black", "tags": ["Hybrid Fit", "Anti-Ride", "Compression Support"], "desc": "The hybrid warrior. Between a trunk and a brief lies perfection — supportive compression meets relaxed luxury in our most-loved silhouette."},
    {"name": "Mjolnir Sport Boxer", "cat": "Boxers", "price": 999, "old_price": 1299, "badge": "Sale", "rating": 4.5, "review_count": 143, "img": "https://images.unsplash.com/photo-1593702288056-7cc9c9c93e39?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=700&q=90&fit=crop&crop=top", "fabric": "Performance Polyester Blend", "fabric_type": "Performance", "color": "Grey", "tags": ["Sport Fit", "Quick Dry", "Anti-Chafe"], "desc": "Built for the relentless. Performance polyester that wicks, stretches, and endures alongside you — because your underwear should work as hard as you do."},
    {"name": "Freya Ultra-Comfort Brief", "cat": "Briefs", "price": 549, "old_price": None, "badge": None, "rating": 4.8, "review_count": 201, "img": "https://images.unsplash.com/photo-1520975916090-3105956dac38?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1593702288056-7cc9c9c93e39?w=700&q=90&fit=crop&crop=top", "fabric": "100% Supima Cotton", "fabric_type": "Supima Cotton", "color": "White", "tags": ["Cloud Soft", "Stretch Waistband", "Everyday"], "desc": "Pure luxury at its most essential. Supima cotton — the rarest, softest cotton on earth — shaped into the perfect everyday brief. Wear it once, wear nothing else."},
    {"name": "Asgard Long Boxer", "cat": "Boxers", "price": 1149, "old_price": None, "badge": "New", "rating": 4.7, "review_count": 89, "img": "https://images.unsplash.com/photo-1618354691792-d1d42acfd860?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=700&q=90&fit=crop&crop=top", "fabric": "96% Bamboo, 4% Spandex", "fabric_type": "Bamboo", "color": "Charcoal", "tags": ["Extended Length", "Anti-Bacterial", "Eco-Certified"], "desc": "Sustainability meets supremacy. Bamboo-derived fabric that's naturally antibacterial, temperature-regulating, and impeccably soft — for the warrior who cares about the earth as fiercely as his craft."},
    {"name": "Loki Seamless Trunk", "cat": "Trunks", "price": 1099, "old_price": 1399, "badge": "21% OFF", "rating": 4.6, "review_count": 167, "img": "https://images.unsplash.com/photo-1512484776495-a09d92e87c3b?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=700&q=90&fit=crop&crop=top", "fabric": "Seamless Nylon-Spandex", "fabric_type": "Performance", "color": "Black", "tags": ["Zero Seams", "Compression", "No-Show"], "desc": "The invisible advantage. Seamless construction eliminates all friction points — no lines, no ride-up, no distractions. Just clean confidence from the inside out."},
    {"name": "Bifrost Thermal Brief", "cat": "Thermal", "price": 1349, "old_price": None, "badge": None, "rating": 4.8, "review_count": 54, "img": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=700&q=90&fit=crop&crop=top", "fabric": "Merino Wool Blend", "fabric_type": "Merino", "color": "Slate", "tags": ["Heat-Lock", "Odor Resistant", "All-Day Comfort"], "desc": "Arctic warmth, desert breathability. Our merino brief traps heat when you need it, releases it when you don't — nature's most sophisticated thermoregulation, engineered for the modern man."},
    {"name": "Dreki Compression Brief", "cat": "Briefs", "price": 899, "old_price": 1199, "badge": "25% OFF", "rating": 4.9, "review_count": 312, "img": "https://images.unsplash.com/photo-1593702288056-7cc9c9c93e39?w=700&q=90&fit=crop&crop=top", "img2": "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=700&q=90&fit=crop&crop=top", "fabric": "82% Nylon, 18% Spandex", "fabric_type": "Performance", "color": "Navy", "tags": ["Athletic Support", "Recovery", "Power Fit"], "desc": "Train hard. Recover harder. Graduated compression technology supports muscles during peak performance and accelerates recovery — the brief for champions who never settle."},
]

REVIEWS_SEED = [
    {"name": "Arjun Malhotra", "loc": "Delhi", "tag": "Verified Buyer", "review": "The Valhalla trunk is the most comfortable innerwear I've ever worn. The fabric is butter-soft, never bunches, and holds its shape perfectly. Reordered three times.", "stars": 5, "init": "AM"},
    {"name": "Rohan Pillai", "loc": "Mumbai", "tag": "Verified Buyer", "review": "Finally an Indian brand that gets premium quality right. The Odin 3-pack is incredible value — feels luxury, washes beautifully, and stays soft after every wash.", "stars": 5, "init": "RP"},
    {"name": "Siddharth Kumar", "loc": "Bangalore", "tag": "Verified Buyer", "review": "Mjolnir sport boxers are a game changer for gym sessions. Zero riding, zero chafing, and they stay perfectly in place through the most intense workouts.", "stars": 5, "init": "SK"},
    {"name": "Vikram Singh", "loc": "Jaipur", "tag": "Verified Buyer", "review": "The Ragnarok thermal set saved me during a Himachal trip. Warm without bulk, and the merino doesn't smell even after multiple wears.", "stars": 5, "init": "VS"},
    {"name": "Aditya Rao", "loc": "Hyderabad", "tag": "Verified Buyer", "review": "Loki seamless trunks are invisible under slim-fit trousers. No lines, no adjustments needed all day. Worth every rupee.", "stars": 5, "init": "AR"},
    {"name": "Karan Mehta", "loc": "Pune", "tag": "Verified Buyer", "review": "Customer service responded within hours when I had a sizing question. Product quality matches the premium branding perfectly.", "stars": 4, "init": "KM"},
]


def run_seed(db) -> None:
    from app.config import settings
    from app.models import Product, Review, User
    from app.models.role import UserRole
    from app.security import hash_password

    admin_email = settings.admin_email.lower()
    if not db.query(User).filter(User.email == admin_email).first():
        db.add(
            User(
                email=admin_email,
                name=settings.admin_name,
                hashed_password=hash_password(settings.admin_password),
                role=UserRole.ADMIN.value,
            )
        )
        db.commit()

    if db.query(Product).count() == 0:
        for data in PRODUCTS_SEED:
            db.add(Product(**data))
        db.commit()

    if db.query(Review).count() == 0:
        for data in REVIEWS_SEED:
            db.add(Review(**data))
        db.commit()
