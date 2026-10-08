import base64, json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

PROMPT = "This is a TCG Riftbound card, return raw JSON only (no markdown, no code fences, no extra text) with the keys: name (biggest font size on the card), set_code (eg. OGN, SFD etc.), number (number/set number) and rarity"

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
