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
        name="d6-product-array-v2.png",
        prompt=(
            "Photorealistic product photograph of a NASA VSAT-style vertical lunar solar "
            "array: a freestanding deployable unit with a wide tripod base structure, a "
            "sun-tracking gimbal, a tall telescoping extension mast, and a large flat "
            "rectangular photovoltaic panel array mounted high on the mast, dark blue "
            "solar cells in a visible grid, aerospace-grade aluminum structure, "
            "three-quarter angle, clean isolated subject on plain background, high detail "
            "studio product photography"
        ),
        size="1024x1024",
        transparent=True,
    ),
    dict(
        name="d6-product-h2o2storage-v2.png",
        prompt=(
            "Photorealistic product photograph of two aerospace composite overwrapped "
            "pressure vessels (COPV) for hydrogen and oxygen storage: cylindrical tanks "
            "with domed ends, dark woven carbon fiber overwrap with visible crisscross "
            "fiber winding pattern and resin sheen, polished metallic boss and valve "
            "fitting at the top of each tank, mounted side by side in a simple aluminum "
            "support cradle, three-quarter angle, clean isolated subject on plain "
            "background, high detail studio product photography"
        ),
        size="1024x1024",
        transparent=True,
    ),
    dict(
        name="d6-product-powermodule-v2.png",
        prompt=(
            "Photorealistic product photograph of a rugged spacecraft power distribution "
            "unit: a rectangular machined aluminum electronics chassis with milled "
            "stiffening ribs and cooling fins, a front panel populated with several "
            "MIL-38999 circular aerospace connectors and two stainless steel "
            "quick-disconnect fluid coupling ports for hydrogen and oxygen transfer, "
            "corner mounting flanges with bolt holes, gold-plated grounding stud, "
            "three-quarter angle, clean isolated subject on plain background, high detail "
            "studio product photography"
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
