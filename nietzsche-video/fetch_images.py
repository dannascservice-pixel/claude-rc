"""Baixa as imagens do roteiro do Wikimedia Commons e grava créditos/licenças.
Uso: python3 fetch_images.py <pasta_saida>"""
import hashlib, json, os, re, sys, time, urllib.parse, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from roteiro import SCENES
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "PhilosophyVideoBot/1.0 (educational)"}
def get(url, binary=False):
    for i in range(6):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            return r if binary else json.loads(r)
        except Exception as e:
            print("  retry", e, flush=True); time.sleep(15 * (i + 1))
    raise SystemExit("falhou: " + url)
files = sorted({f for s in SCENES for f in s["shots"]})
cpath = os.path.join(OUT, "credits.json")
credits = json.load(open(cpath)) if os.path.exists(cpath) else {}
todo = [f for f in files if f not in credits or not os.path.exists(credits[f]["file"])]
# 1) metadados de todas as imagens em uma única consulta
meta = {}
for i in range(0, len(todo), 40):
    d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(
        action="query", titles="|".join("File:" + f for f in todo[i:i + 40]), prop="imageinfo",
        iiprop="url|extmetadata|size", format="json")))
    norm = {n["to"]: n["from"] for n in d["query"].get("normalized", [])}
    for p in d["query"]["pages"].values():
        meta[norm.get(p["title"], p["title"])[5:]] = p["imageinfo"][0]
# 2) baixa miniaturas em tamanhos padronizados (sem consulta extra à API)
for f in todo:
    ii = meta[f]; md = ii.get("extmetadata", {})
    clean = lambda k: re.sub("<[^>]+>", "", md.get(k, {}).get("value", "")).strip()
    name = f.replace(" ", "_"); h = hashlib.md5(name.encode()).hexdigest()
    tw = next((x for x in (1920, 1280, 960, 500) if ii["width"] > x), None)
    if tw:
        url = f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{urllib.parse.quote(name)}/{tw}px-{urllib.parse.quote(name)}"
        if name.lower().endswith((".tif", ".tiff")): url += ".jpg"
    else:
        url = ii["url"]
    dest = os.path.join(OUT, re.sub(r"[^A-Za-z0-9._-]", "_", f).rsplit(".", 1)[0] + ".jpg")
    if not os.path.exists(dest):
        data = get(url, binary=True); open(dest, "wb").write(data)
    credits[f] = dict(artist=clean("Artist"), license=clean("LicenseShortName"),
                      page=ii["descriptionurl"], file=dest)
    json.dump(credits, open(cpath, "w"), ensure_ascii=False, indent=1)
    print(f"ok {f} [{credits[f]['license']}]", flush=True); time.sleep(2)
print("TODAS", len(credits), "de", len(files))
