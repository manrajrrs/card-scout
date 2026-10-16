# Card Scout

An AI agent that identifies Riftbound trading cards from a photo, built to support my own card selling (in progress).

## Results

Eval: 10 photos of my own Riftbound cards, scored by exact match against hand-written labels (`labels.csv`).

| Run | Change | Full match | Name | Set code | Number | Rarity |
|-----|--------|-----------|------|----------|--------|--------|
| 1 | Baseline prompt | 3/10 | 4/10 | 10/10 | 10/10 | 7/10 |
| 2 | Prompt asks for the full card name, including the subtitle | 8/10 | 10/10 | 10/10 | 10/10 | 8/10 |
| 3 | Prompt adds guidance for identifying rarity | 10/10 | 10/10 | 10/10 | 10/10 | 10/10 |

Each row is a single run, and model output varies slightly between runs. The prompt was tuned on these same 10 cards, so these scores are on the tuning set. A held-out set is planned.

## How it works

Upload a photo to `POST /identify`. The image is base64-encoded and sent to Anthropic's Claude Haiku vision model, which returns the card name, set code, number and rarity as JSON.

```json
{"name": "Teemo", "set_code": "SFD", "number": "230/221", "rarity": "Overnumbered"}
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