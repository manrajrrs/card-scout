# Card Scout

An AI agent that identifies Riftbound trading cards from a photo, built to support my own card selling (in progress).

## Results

## Eval

30 photos of Riftbound cards (owned + eBay-sourced), scored by exact match per field against hand-written labels (`labels.csv`).
Labels are written from the physical card before the model runs and never edited to fit results.

| Run | Cards | Prompt change | Full match | Name | Set code | Number | Rarity |
|-----|-------|---------------|-----------|------|----------|--------|--------|
| 1 | 1-10 | Baseline | 3/10 | 4/10 | 10/10 | 10/10 | 7/10 |
| 2 | 1-10 | Ask for full card name including subtitle eg. Kai'Sa, Survivor | 8/10 | 10/10 | 10/10 | 10/10 | 8/10 |
| 3 | 1-10 | Add rarity granularity eg. Alternate Art, Overnumbered, Signature | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |
| 4 | 1-20 (held-out) | None | 20/20 | 20/20 | 20/20 | 20/20 | 20/20 |
| 5 | 1-30 (all) | None | 20/30 | 26/30 | 30/30 | 24/30 | 21/30 |
| 6 | 1-30 (all) | Translate Chinese/Korean to English, refine number eg. SFD 230*/221 | 21/30 | 27/30 | 29/30 | 24/30 | 22/30 |

## Known failures
- Number suffixes (a, b, *) are dropped or misread due to blur, angles, glare from sleeves etc.
- Chinese cards: the model sometimes returns a name that differs from the printed name (card26: printed "Kennen, Heart of the Tempest", model returned "Heart of Fury").
- Rarity is low on variants (Alternate Art, Signature, Promo).

## How it works

Upload a photo to `POST /identify`. The image is base64-encoded and sent to Anthropic's Claude Haiku vision model, which returns the card name, set code, number and rarity as JSON.

```json
{"name": "Teemo, Strategist", "set_code": "SFD", "number": "230/221", "rarity": "Overnumbered"}
```

Stack: Python, FastAPI, Docker.

## Run it

Create a `.env` file with your key:

```
ANTHROPIC_API_KEY=your-key-here
```

With Docker:

```bash
docker build -t card-scout .
docker run --env-file .env -p 8000:8000 card-scout
```

Or locally:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://localhost:8000/docs` to upload a photo.

![Swagger UI at /docs](image-1.png)

## Run the eval

```bash
python eval.py
```

Reads `labels.csv`, runs each photo in `test_cards/` through the model and prints accuracy per field.

## Next

- Held-out test set
- Price lookup from legitimate APIs
- GitHub Actions CI
- MCP server◊