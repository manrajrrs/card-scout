import base64, json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

PROMPT = """
            This is a TCG Riftbound card,
            Return raw JSON only (no markdown, no code fences, no extra text) with the following keys:
            - name (usually biggest font size on the card but if there is additional text underneath on the same banner include this eg. 'Kai'Sa, Survivor' or 'Fizz, Trickster' but if the name is not on the banner eg 'Blind Monk' don't add Lee Sin if it's not on the banner)
            - set_code (eg. OGN, SFD, UNL, VEN, RAD etc.)
            - number (copy the card number exactly as printed + '/{set number}, including any letter or symbol suffix a,b,* - for example 230*/221 or 038a/166)
            - rarity (
                - if number contains a or b it's an Alternate Art,
                - if number is bigger than set number it's Overnumbered,
                - if Overnumbered with a * it's a Signature,
                - if number contains SP it's a Special (Vendetta exclusive),
                - if number contains P or if there is a small white banner above the gem/rarity symbol that says PROMO it's a Promo
                - if none of the above apply use the gem/rarity symbol (bottom centre of card)
                    - white pearl - Common
                    - blue triangle - Uncommon
                    - purple - Rare
                    - orange - Epic
                    
            For non-English cards eg. Chinese, Korean: Translate and use the English card name
                )
        """

def identify_card(image_bytes: bytes, media_type: str = "image/jpeg") -> dict:
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_b64}},
                {"type": "text", "text": PROMPT},
            ],
        }],
    )
        
    for block in response.content:
        if block.type == "text":
            return json.loads(block.text)

if __name__ == "__main__":
    with open("test_cards/card1.jpg", "rb") as f:
        print(identify_card(f.read()))
