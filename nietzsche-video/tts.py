"""Gera a narração de cada cena com voz neural pt-BR (edge-tts), com legendas por frase."""
import asyncio, os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import edge_tts
from roteiro import SCENES
OUT = sys.argv[1]
VOICE, RATE, PITCH = "pt-BR-AntonioNeural", "-8%", "-4Hz"
async def one(s):
    mp3 = os.path.join(OUT, s["id"] + ".mp3"); js = os.path.join(OUT, s["id"] + ".json")
    if os.path.exists(mp3) and os.path.getsize(mp3) > 0 and os.path.exists(js): return
    com = edge_tts.Communicate(s["text"], VOICE, rate=RATE, pitch=PITCH, boundary="SentenceBoundary")
    bounds = []
    with open(mp3, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"].endswith("Boundary"):
                bounds.append(dict(start=ch["offset"]/1e7, end=(ch["offset"]+ch["duration"])/1e7, text=ch["text"]))
    json.dump(bounds, open(js, "w"), ensure_ascii=False)
    print("ok", s["id"], len(bounds), "frases")
async def main():
    for s in SCENES:
        for i in range(4):
            try: await one(s); break
            except Exception as e: print("retry", s["id"], e); await asyncio.sleep(3)
asyncio.run(main())
