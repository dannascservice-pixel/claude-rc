"""Gera thumbnail (1280x720) e descricao_youtube.txt com créditos das imagens."""
import json, os, sys
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
WORK, OUT = sys.argv[1], sys.argv[2]
CR = json.load(open(os.path.join(WORK, "img", "credits.json")))
def font(n, s, w):
    f = ImageFont.truetype(os.path.join(HERE, "fonts", n), s); f.set_variation_by_axes([w]); return f
# ---- thumbnail
W, H = 1280, 720
src = Image.open(CR["Edvard Munch - Friedrich Nietzsche - MM.M.00724 - Munch Museum.jpg"]["file"]).convert("RGB")
# retrato de Munch à direita, ocupando a altura toda, rosto em destaque
crop = src.crop((0, int(src.height * 0.12), src.width, int(src.height * 0.62)))
ph = H; pw = int(crop.width * ph / crop.height)
img = Image.new("RGB", (W, H), (12, 10, 8)); img.paste(crop.resize((pw, ph), Image.LANCZOS), (W - pw + 40, 0))
g = ImageOps.colorize(ImageOps.grayscale(img), (10, 8, 6), (120, 90, 60), (250, 225, 185))
img = ImageEnhance.Contrast(Image.blend(g, img, 0.35)).enhance(1.25)
grad = Image.linear_gradient("L").rotate(90).resize((W, H))  # 255 à esquerda -> escurece o lado do texto
mask = grad.point(lambda v: int(max(0, min(255, (v - 70) * 1.6))))
img = Image.composite(Image.new("RGB", (W, H), (10, 8, 6)), img, mask)
d = ImageDraw.Draw(img)
def outline(xy, t, f, fill):
    d.text(xy, t, font=f, fill=fill, stroke_width=4, stroke_fill=(0, 0, 0))
outline((50, 150), "NIETZSCHE", font("Cinzel[wght].ttf", 118, 800), (250, 244, 232))
outline((56, 300), "TRANSCENDEU", font("Cinzel[wght].ttf", 74, 700), (214, 178, 112))
outline((56, 390), "E ENLOUQUECEU", font("Cinzel[wght].ttf", 74, 700), (205, 60, 45))
outline((60, 500), "a história real do filósofo", font("CormorantGaramond-Italic[wght].ttf", 52, 600), (235, 225, 210))
img.save(os.path.join(OUT, "thumbnail.jpg"), quality=92)
# ---- descrição
lines = ["Nietzsche: o homem que transcendeu e enlouqueceu", "",
 "Turim, janeiro de 1889. Um homem abraça um cavalo numa praça e desaba. Ele havia acabado de anunciar a morte de Deus e o além-do-homem — e nunca mais escreveria uma linha. Esta é a história de Friedrich Nietzsche: o filho do pastor que virou o filósofo do martelo, o andarilho solitário dos Alpes, o profeta de Zaratustra, e o homem que passou seus últimos onze anos em silêncio.", "",
 "CAPÍTULOS"]
# capítulos com tempos reais a partir dos segmentos renderizados
import subprocess
from roteiro import SCENES
t = 0.0
for s in SCENES:
    if s.get("chapter") or s.get("title"):
        name = "Introdução" if s["id"] == "01_turim" else ("Abertura" if s.get("title") else s["chapter"])
        lines.append(f"{int(t // 60):02}:{int(t % 60):02} {name}")
    t += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                        os.path.join(WORK, "seg", s["id"] + ".mp4")]))
lines += ["", "Obras citadas: O Nascimento da Tragédia (1872), A Gaia Ciência (1882), Assim Falou Zaratustra (1883–85), Além do Bem e do Mal (1886), Genealogia da Moral (1887), Crepúsculo dos Ídolos, O Anticristo e Ecce Homo (1888).", "",
 "Nota: o episódio do cavalo em Turim vem de relatos posteriores e pode ser em parte lendário; a causa da doença de Nietzsche segue debatida.", "",
 "#Nietzsche #Filosofia #EternoRetorno #AlémDoHomem #DeusEstáMorto", "",
 "CRÉDITOS DAS IMAGENS (Wikimedia Commons)"]
for f, c in sorted(CR.items()):
    lines.append(f"- {f.rsplit('.',1)[0]} — {(c['artist'] if c['artist'] and 'Unknown' not in c['artist'] else 'autor desconhecido')} — {c['license']} — {c['page']}")
lines += ["", "Música: trilha ambiente original sintetizada para este vídeo.", "Narração: voz sintética (pt-BR)."]
open(os.path.join(OUT, "descricao_youtube.txt"), "w").write("\n".join(lines) + "\n")
print("ok")
