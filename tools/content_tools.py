import re
from schemas.data_models import ContentPiece

class ContentGenerator:
    def format_hashtags(self, hashtags: list) -> list:
        cleaned = []
        for h in hashtags:
            # Remove special characters and hashtags symbol
            h_clean = re.sub(r'[^\w]', '', h)
            if h_clean:
                cleaned.append(h_clean.lower())
        return cleaned

    def create_placeholder_context(self, segment: str, customer_name: str = "valued guest") -> dict:
        """Generates dynamic placeholders based on segment rules."""
        context = {"name": customer_name, "offer": ""}
        if segment == "vip":
            context["offer"] = "Complimentary dessert & priority reservation"
        elif segment == "churning":
            context["offer"] = "20% off your next delivery order using promo: WE_MISS_YOU"
        elif segment == "new":
            context["offer"] = "Free drink with your first dine-in order"
        else:
            context["offer"] = "Free delivery on orders above 30,000 UGX"
        return context
