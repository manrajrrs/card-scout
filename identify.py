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
            - number (number/set number)
            - rarity (
                - if number contains a or b it's an Alternate Art / Alt Art,
                - if the number is bigger than the set number it's Overnumbered,
                - if it's Overnumbered with a * it's a Signature,
                - if the number contains SP it's a Special (Vendetta exclusive),
                - if the number contains P it's a Promo
                - if none of the above apply:
                    - if the gem is a white pearl it's a Common
                    - if the gem is a blue triangle it's a Uncommon
                    - if the gem is purple it's a Rare
                    - if the gem is orange it's an Epic
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
