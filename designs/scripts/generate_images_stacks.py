import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    sys.exit("OPENAI_API_KEY not set in environment")

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "images")

IMAGES = [
    dict(
        name="d6-product-electrolyzer-v2.png",
        prompt=(
            "Photorealistic product photograph of a compact PEM electrolyzer stack: "
            "a small boxy filter-press unit with a dark gray anodized aluminum end plate "
            "fastened by eight stainless hex bolts around its perimeter, the side showing "
            "a tight stack of thin white ceramic separator plates, two small white plastic "
            "push-fit pneumatic tube fittings on the top face for O2 and H2 output ports "
            "and one water inlet fitting on the lower face, industrial laboratory hardware, "
            "three-quarter angle, clean isolated subject on plain background, high detail "
            "studio product photography"
        ),
        size="1024x1024",
        transparent=True,
    ),
    dict(
        name="d6-product-fuelcell-v2.png",
        prompt=(
            "Photorealistic product photograph of a PEM fuel cell stack: a tall rectangular "
            "stack of many thin dark graphite bipolar plates with visible layered edges, "
            "compressed between two thick machined bare-aluminum end blocks, threaded "
            "tie-rod studs with hex nuts and coil compression springs at the corners, two "
            "stainless steel compression tube fittings on the top plate, industrial "
            "laboratory hardware, three-quarter angle, clean isolated subject on plain "
            "background, high detail studio product photography"
        ),
        size="1024x1024",
        transparent=True,
    ),
]


def request_gpt_image(prompt, size, transparent):
    body = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": size,
        "quality": "high",
    }
    if transparent:
        body["background"] = "transparent"
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.load(resp)
    return base64.b64decode(data["data"][0]["b64_json"])


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for item in IMAGES:
        out_path = os.path.join(OUT_DIR, item["name"])
        print(f"Generating {item['name']}...")
        img_bytes = request_gpt_image(item["prompt"], item["size"], item["transparent"])
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"  saved {out_path} ({len(img_bytes)} bytes)")


if __name__ == "__main__":
    main()
