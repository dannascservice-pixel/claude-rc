# -*- coding: utf-8 -*-
"""
Monta o vídeo final a partir de:
  - roteiro.py          (cenas, textos, imagens)
  - <work>/audio/*.mp3  (narração gerada por tts.py, + .json com tempos das frases)
  - <work>/img/*.jpg    (imagens baixadas por fetch_images.py, + credits.json)

Uso: python3 render.py <work_dir> <saida_dir>
"""
import json, math, os, re, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from roteiro import SCENES

WORK, OUT = sys.argv[1], sys.argv[2]
SEG = os.path.join(WORK, "seg"); os.makedirs(SEG, exist_ok=True); os.makedirs(OUT, exist_ok=True)
W, H, FPS, SR = 1920, 1080, 30, 48000
SS = 2  # supersampling dos stills para o zoom ficar suave
LEAD_CHAPTER, LEAD, TAIL = 1.2, 0.35, 0.75
GOLD = (214, 178, 112)
CREDITS = json.load(open(os.path.join(WORK, "img", "credits.json")))

def font(name, size, wght):
    f = ImageFont.truetype(os.path.join(HERE, "fonts", name), size)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
F_TITLE = lambda s: font("Cinzel[wght].ttf", s, 700)
F_CAP = lambda s: font("Cinzel[wght].ttf", s, 500)
F_BODY = lambda s: font("CormorantGaramond[wght].ttf", s, 500)
F_IT = lambda s: font("CormorantGaramond-Italic[wght].ttf", s, 500)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-3000:]); raise SystemExit("ffmpeg falhou")

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", p]).strip())

# ------------------------------------------------------------------ imagens
def grade(im):
    """Gradação 'documentário antigo': pouca saturação, tom quente, contraste suave."""
    im = ImageOps.exif_transpose(im).convert("RGB")
    g = ImageOps.grayscale(im)
    sep = ImageOps.colorize(g, black=(18, 14, 10), mid=(128, 104, 78), white=(240, 226, 200))
    im = Image.blend(sep, im, 0.28)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    return im

def still(img_file, out_png):
    if os.path.exists(out_png): return
    TW, TH = W * SS, H * SS
    im = grade(Image.open(img_file))
    ar = im.width / im.height
    if ar >= 1.25:  # paisagem: preenche a tela
        canvas = ImageOps.fit(im, (TW, TH), Image.LANCZOS)
    else:           # retrato: fundo desfocado + imagem inteira no centro
        bg = ImageOps.fit(im, (TW // 8, TH // 8), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6))
        bg = ImageEnhance.Brightness(bg.resize((TW, TH), Image.LANCZOS)).enhance(0.38)
        h = int(TH * 0.94); w = int(h * ar)
        fg = im.resize((w, h), Image.LANCZOS)
        sh = Image.new("L", (TW, TH), 0); ImageDraw.Draw(sh).rectangle(
            [(TW - w) // 2 - 10, (TH - h) // 2 - 10, (TW + w) // 2 + 10, (TH + h) // 2 + 10], fill=170)
        bg.paste(Image.new("RGB", (TW, TH), 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(40)))
        bg.paste(fg, ((TW - w) // 2, (TH - h) // 2))
        canvas = bg
    # vinheta
    yy, xx = np.mgrid[0:TH, 0:TW].astype(np.float32)
    d = np.sqrt(((xx - TW / 2) / (TW / 2)) ** 2 + ((yy - TH / 2) / (TH / 2)) ** 2)
    v = np.clip(1.0 - 0.55 * np.clip(d - 0.55, 0, None) ** 1.4, 0.25, 1)
    arr = (np.asarray(canvas).astype(np.float32) * v[..., None]).clip(0, 255).astype(np.uint8)
    Image.fromarray(arr).save(out_png)

# ------------------------------------------------------------------ overlays de texto
def text_center(draw, y, txt, f, fill, spacing=1.0):
    for line in txt.split("\n"):
        bb = draw.textbbox((0, 0), line, font=f)
        draw.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), line, font=f, fill=fill)
        y += int((bb[3] - bb[1]) * 1.0 + f.size * 0.45 * spacing)
    return y

def block_h(draw, txt, f, spacing=1.0):
    h = 0
    for line in txt.split("\n"):
        bb = draw.textbbox((0, 0), line, font=f); h += int((bb[3] - bb[1]) + f.size * 0.45 * spacing)
    return h

def shade(alpha_max=200, band=None):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if band:
        y0, y1 = band
        a = np.zeros((H, W), np.float32)
        for y in range(H):
            t = 1.0 if y0 <= y <= y1 else max(0, 1 - min(abs(y - y0), abs(y - y1)) / 140)
            a[y, :] = t * alpha_max
        im.putalpha(Image.fromarray(a.astype(np.uint8)))
    else:
        im.putalpha(alpha_max)
    return im

def ov_chapter(txt, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    parts = txt.split(". ", 1)
    num, name = (parts[0], parts[1]) if len(parts) == 2 and len(parts[0]) <= 4 else ("", txt)
    sh = shade(150, (H - 300, H - 120)); im = Image.alpha_composite(im, sh); d = ImageDraw.Draw(im)
    y = H - 285
    if num:
        y = text_center(d, y, num, F_CAP(44), GOLD + (255,))
    y = text_center(d, y + 4, name.upper(), F_TITLE(64), (245, 238, 225, 255))
    d.line([(W / 2 - 120, y + 8), (W / 2 + 120, y + 8)], fill=GOLD + (255,), width=2)
    im.save(path)

def ov_quote(q, src, path):
    im = shade(165); d = ImageDraw.Draw(im)
    fq, fs = F_IT(76), F_CAP(34)
    hq = block_h(d, q, fq, 0.6)
    y = (H - hq - 120) / 2
    text_center(d, y - 120, "“", F_BODY(160), GOLD + (220,))
    y = text_center(d, y, q, fq, (248, 242, 230, 255), 0.6)
    d.line([(W / 2 - 60, y + 22), (W / 2 + 60, y + 22)], fill=GOLD + (255,), width=2)
    text_center(d, y + 46, src.upper(), fs, GOLD + (255,))
    im.save(path)

def ov_duality(card, path):
    a, ad, b, bd = card
    im = shade(215); d = ImageDraw.Draw(im)
    for cx, name, desc in ((W * 0.27, a, ad), (W * 0.73, b, bd)):
        for txt, f, fill, yy in ((name.upper(), F_TITLE(92), (245, 238, 225, 255), H / 2 - 110),
                                 (desc, F_IT(48), GOLD + (255,), H / 2 + 20)):
            bb = d.textbbox((0, 0), txt, font=f)
            d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], yy), txt, font=f, fill=fill)
    d.line([(W / 2, H / 2 - 150), (W / 2, H / 2 + 120)], fill=GOLD + (200,), width=2)
    im.save(path)

def ov_title(path):
    im = shade(110); d = ImageDraw.Draw(im)
    y = text_center(d, H / 2 - 170, "NIETZSCHE", F_TITLE(170), (248, 242, 230, 255))
    d.line([(W / 2 - 260, y + 6), (W / 2 + 260, y + 6)], fill=GOLD + (255,), width=3)
    text_center(d, y + 34, "o homem que transcendeu e enlouqueceu", F_IT(72), GOLD + (255,))
    text_center(d, y + 140, "1844 — 1900", F_CAP(36), (220, 210, 195, 230))
    im.save(path)

def ov_outro(path):
    im = shade(120); d = ImageDraw.Draw(im)
    y = text_center(d, H / 2 - 120, "VOCÊ ACEITARIA\nO ETERNO RETORNO?", F_TITLE(84), (248, 242, 230, 255), 0.5)
    d.line([(W / 2 - 200, y + 10), (W / 2 + 200, y + 10)], fill=GOLD + (255,), width=2)
    text_center(d, y + 40, "comente  ·  inscreva-se", F_IT(56), GOLD + (255,))
    im.save(path)

# ------------------------------------------------------------------ tempos
def norm(s): return re.sub(r"[^a-zà-ú ]", "", s.lower())

def find_window(bounds, quote_text):
    """Janela [ini, fim] em que a narração lê o trecho citado."""
    lines = [l for l in re.split(r"[\n.]", quote_text) if l.strip()]
    first, last = norm(lines[0])[:25], norm(lines[-1])[-20:]
    i0 = next((i for i, b in enumerate(bounds) if first.strip() and first.strip()[:18] in norm(b["text"])), None)
    i1 = next((i for i, b in enumerate(bounds) if i >= (i0 or 0) and last.strip()[-14:] in norm(b["text"])), None)
    if i0 is None: return None
    i1 = i1 if i1 is not None else i0
    return bounds[i0]["start"], bounds[i1]["end"]

# ------------------------------------------------------------------ cenas
def file_of(shot): return CREDITS[shot]["file"]

def render_scene(k, s):
    mp3 = os.path.join(WORK, "audio", s["id"] + ".mp3")
    bounds = json.load(open(os.path.join(WORK, "audio", s["id"] + ".json")))
    lead = LEAD_CHAPTER if s.get("chapter") or s.get("title") else LEAD
    adur = dur(mp3)
    total = lead + adur + TAIL + (1.5 if s.get("outro") else 0) + (0.8 if s.get("title") else 0)
    nframes = int(round(total * FPS)); total = nframes / FPS
    out = os.path.join(SEG, f"{s['id']}.mp4")
    meta = dict(id=s["id"], lead=lead, total=total, bounds=bounds, mp3=mp3)
    if os.path.exists(out): return meta

    shots = s["shots"]; n = len(shots)
    inputs, filt = [], []
    per = total / n
    for j, shot in enumerate(shots):
        png = os.path.join(SEG, f"{s['id']}_{j}.png"); still(file_of(shot), png)
        nf = int(round(per * FPS)) if j < n - 1 else nframes - int(round(per * FPS)) * (n - 1)
        zin = (k + j) % 2 == 0
        z = f"1.0+0.10*on/{nf}" if zin else f"1.10-0.10*on/{nf}"
        px = ["0", "0.5", "-0.5"][(k + j) % 3]
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{nf / FPS:.3f}", "-i", png]
        filt.append(
            f"[{j}:v]zoompan=z='{z}':x='(iw-iw/zoom)/2+{px}*(iw-iw/zoom)/2*on/{nf}':"
            f"y='(ih-ih/zoom)/2':d=1:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[s{j}]")
    # cortes internos com crossfade simples via concat
    filt.append("".join(f"[s{j}]" for j in range(n)) + f"concat=n={n}:v=1:a=0[base]")
    last = "base"; idx = n

    def add_overlay(png, t0, t1):
        nonlocal last, idx
        inputs.extend(["-loop", "1", "-framerate", str(FPS), "-t", f"{total:.3f}", "-i", png])
        t0 = max(0.0, t0); t1 = min(total, t1)
        filt.append(f"[{idx}:v]format=rgba,fade=t=in:st={t0:.2f}:d=0.7:alpha=1,"
                    f"fade=t=out:st={max(t0 + 0.8, t1 - 0.7):.2f}:d=0.7:alpha=1[o{idx}]")
        filt.append(f"[{last}][o{idx}]overlay=0:0:format=auto[v{idx}]")
        last = f"v{idx}"; idx += 1

    if s.get("title"):
        p = os.path.join(SEG, "ov_title.png"); ov_title(p); add_overlay(p, 0.3, total - 0.2)
    if s.get("outro"):
        p = os.path.join(SEG, "ov_outro.png"); ov_outro(p); add_overlay(p, lead + 0.2, total)
    if s.get("chapter"):
        p = os.path.join(SEG, f"ov_ch_{s['id']}.png"); ov_chapter(s["chapter"], p); add_overlay(p, 0.2, 4.6)
    if s.get("quote"):
        p = os.path.join(SEG, f"ov_q_{s['id']}.png"); ov_quote(*s["quote"], p)
        win = find_window(bounds, s["quote"][0])
        t0, t1 = (win[0] + lead - 0.3, win[1] + lead + 2.2) if win else (total - 9, total)
        if s.get("chapter"): t0 = max(t0, 5.0)
        add_overlay(p, t0, max(t1, t0 + 5))
    if s.get("card"):
        p = os.path.join(SEG, f"ov_card_{s['id']}.png"); ov_duality(s["card"], p)
        win = find_window(bounds, s["card"][0] + "\n" + s["card"][3])
        t0, t1 = (win[0] + lead - 0.3, win[1] + lead + 1.8) if win else (total / 3, total * 2 / 3)
        add_overlay(p, t0, t1)

    filt.append(f"[{last}]noise=alls=7:allf=t,fade=t=in:st=0:d=0.6,"
                f"fade=t=out:st={total - 0.6:.3f}:d=0.6,format=yuv420p[vout]")
    tmp = out[:-4] + ".part.mp4"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[vout]",
         "-frames:v", str(nframes), "-c:v", "libx264", "-preset", "fast", "-crf", "19",
         "-r", str(FPS), "-threads", "2", tmp])
    os.replace(tmp, out)
    print("cena", s["id"], f"{total:.1f}s")
    return meta

# ------------------------------------------------------------------ áudio
def load_wav(mp3):
    tmp = mp3[:-4] + ".48k.wav"
    if not os.path.exists(tmp):
        run(["ffmpeg", "-y", "-i", mp3, "-ac", "1", "-ar", str(SR), tmp])
    with wave.open(tmp) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def music(n):
    """Trilha ambiente sombria sintetizada (drone em Ré menor), sem direitos autorais."""
    t = np.arange(n) / SR
    out = np.zeros(n, np.float32)
    chords = [[73.42, 110.0, 146.83, 174.61], [65.41, 98.0, 130.81, 155.56],
              [58.27, 87.31, 116.54, 146.83], [55.0, 82.41, 110.0, 138.59]]  # Dm, Cm, Bb, A
    period = 16.0
    rng = np.random.default_rng(7)
    for ci, ch in enumerate(chords):
        phase = (t / period - ci / len(chords)) % 1.0  # cada acorde ocupa 1/4 do ciclo com crossfade longo
        env = np.clip(1 - np.abs(((phase * len(chords)) % len(chords)) - 0.5) / 1.1, 0, 1) ** 1.5
        for f in ch:
            for det in (-0.6, 0.0, 0.6):
                ph = rng.uniform(0, 2 * np.pi)
                out += env * (np.sin(2 * np.pi * (f + det) * t + ph) +
                              0.25 * np.sin(2 * np.pi * 2 * (f + det) * t + ph)) * 0.05
    # sub grave e "vento"
    out += 0.10 * np.sin(2 * np.pi * 36.71 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 23))
    noise = rng.standard_normal(n).astype(np.float32)
    k = 400; noise = np.convolve(noise, np.ones(k) / k, mode="same") * 6
    out += noise * 0.05 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 31))
    out *= 0.9 + 0.1 * np.sin(2 * np.pi * t / 7.3)
    return (out / np.abs(out).max()).astype(np.float32)

def srt_time(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def wrap_chunks(text, maxc=84):
    words, chunks, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > maxc and cur: chunks.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    if cur: chunks.append(cur)
    return chunks

def main():
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max(1, (os.cpu_count() or 2) // 2)) as ex:
        metas = list(ex.map(render_scene, range(len(SCENES)), SCENES))
    total = sum(m["total"] for m in metas); N = int(round(total * SR)) + SR
    voice = np.zeros(N, np.float32); srt, n_srt, t = [], 1, 0.0
    for m in metas:
        a = load_wav(m["mp3"]); i = int(round((t + m["lead"]) * SR))
        voice[i:i + len(a)] += a[:N - i]
        for b in m["bounds"]:
            chunks = wrap_chunks(b["text"]); L = sum(len(c) for c in chunks)
            st = t + m["lead"] + b["start"]; span = b["end"] - b["start"]
            for c in chunks:
                d = span * len(c) / L
                half = len(c) // 2; sp = c.rfind(" ", 0, half + 10) if len(c) > 42 else -1
                txt = c[:sp] + "\n" + c[sp + 1:] if sp > 0 else c
                srt.append(f"{n_srt}\n{srt_time(st)} --> {srt_time(st + d)}\n{txt}\n"); n_srt += 1; st += d
        t += m["total"]
    # trilha com ducking sob a voz
    mus = music(N)
    env = np.convolve(np.abs(voice), np.ones(SR // 10) / (SR // 10), mode="same")
    duck = np.where(env > 0.01, 1.0, 0.0).astype(np.float32)
    duck = np.convolve(duck, np.ones(SR // 2) / (SR // 2), mode="same")
    gain = 0.17 - 0.10 * duck
    fade = np.minimum(1, np.minimum(np.arange(N) / (SR * 3), (N - np.arange(N)) / (SR * 5)))
    mix = voice * 1.0 + mus * gain * fade
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    wav = os.path.join(WORK, "mix.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767 * 0.95).astype(np.int16).tobytes())
    open(os.path.join(OUT, "nietzsche_legendas_ptBR.srt"), "w").write("\n".join(srt))
    lst = os.path.join(SEG, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.join(SEG, m['id'] + '.mp4')}'\n" for m in metas))
    final = os.path.join(OUT, "nietzsche_o_homem_que_transcendeu_e_enlouqueceu.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "fast", "-b:v", "8M",
         "-maxrate", "10M", "-bufsize", "16M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", final])
    print("FINAL", final, f"{total / 60:.1f} min")

if __name__ == "__main__":
    main()
