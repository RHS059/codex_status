"""Convert this thread's five newest generated images for the status gallery.

Run after image generation, then use the printed list in the gallery node's
images field (newest first). Original images are preserved.
"""
import argparse, json
from pathlib import Path
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('source',type=Path)
args=parser.parse_args()
destination=Path(__file__).parent/'assets'/'generated'
destination.mkdir(parents=True,exist_ok=True)
files=sorted((p for p in args.source.iterdir() if p.suffix.lower() in ('.png','.jpg','.jpeg','.webp')),key=lambda p:p.stat().st_mtime,reverse=True)[:5]
items=[]
for p in files:
    name=p.stem+'.webp'
    with Image.open(p) as im:
        im.convert('RGBA' if 'A' in im.getbands() else 'RGB').save(destination/name,'WEBP',quality=90,method=6)
    items.append({'src':'assets/generated/'+name,'alt':'Generated reference image '+str(len(items)+1)})
print(json.dumps(items,indent=2))
