import base64
import json
import os
import sys
import urllib.request
import urllib.error

from PIL import Image
import io

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    sys.exit("OPENAI_API_KEY not set in environment")

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "images", "stats")

IMAGES = [
    dict(
        name="d6-stat-orbital-thruster-v2.jpg",
        prompt="Photorealistic close-up of a robotic space station module firing its maneuvering thrusters in orbit near the Moon, bright orange-white engine burn against deep black space, solar panels catching cool blue rim light, stars visible, cinematic sci-fi documentary photography, ultra sharp, ultra detailed, high resolution",
        size="1024x1024",
    ),
]


def request_gpt_image(prompt, size):
    body = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": size,
        "quality": "high",
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    return base64.b64decode(data["data"][0]["b64_json"])


def request_dalle3(prompt, size):
    dalle_size = "1792x1024" if size == "1536x1024" else "1024x1024"
    body = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": dalle_size,
        "quality": "hd",
        "n": 1,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    url = data["data"][0]["url"]
    with urllib.request.urlopen(url, timeout=60) as img_resp:
        return img_resp.read()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    use_gpt_image = True
    for item in IMAGES:
        out_path = os.path.join(OUT_DIR, item["name"])
        print(f"Generating {item['name']}...")
        img_bytes = None
        if use_gpt_image:
            try:
                img_bytes = request_gpt_image(item["prompt"], item["size"])
            except urllib.error.HTTPError as e:
                err_body = e.read().decode(errors="replace")
                print(f"  gpt-image-1 failed ({e.code}): {err_body[:300]}")
                if e.code in (403, 404):
                    use_gpt_image = False
        if img_bytes is None:
            print("  falling back to dall-e-3")
            img_bytes = request_dalle3(item["prompt"], item["size"])

        im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        im.save(out_path, "JPEG", quality=92)
        print(f"  saved {out_path} ({len(img_bytes)} bytes)")


if __name__ == "__main__":
    main()
