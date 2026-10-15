from csv import DictReader
from identify import identify_card

FIELDS = ["name", "set_code", "number", "rarity"]

def compare(file: str):
    correct = dict.fromkeys(FIELDS, 0)
    full_matches = 0
    total = 0
    
    with open(file, newline='') as f:
        reader = DictReader(f)
        for row in reader:
            total += 1
            
            with open("test_cards/" + row['filename'], "rb") as img:
                result = identify_card(img.read())
            
            all_ok = True
            for field in FIELDS:
                if result[field] == row[field]:
                    correct[field] += 1
                else:
                    all_ok = False
                    print(f"MISS {row['filename']} {field}: expected {row[field]!r}, got {result[field]!r}")
            
            if all_ok:
               full_matches += 1
               
    parts = [f"{field} {correct[field]}/{total}" for field in FIELDS]
    print(f"Full match {full_matches}/{total} | " + " | ".join(parts))            
            
if __name__=="__main__":
    compare('labels.csv')