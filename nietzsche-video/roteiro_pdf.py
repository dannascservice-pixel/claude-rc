# -*- coding: utf-8 -*-
"""Gera o roteiro do vídeo em PDF a partir de roteiro.py.

Uso: python3 roteiro_pdf.py <saida.pdf> [<work_dir>]
Se <work_dir> for informado (pasta com seg/*.mp4), o PDF inclui o tempo de início de cada cena.
"""
import os, subprocess, sys
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from roteiro import SCENES

OUT = sys.argv[1]
WORK = sys.argv[2] if len(sys.argv) > 2 else None

LIB = "/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf"
for name, style in (("Serif", "Regular"), ("Serif-B", "Bold"), ("Serif-I", "Italic"), ("Serif-BI", "BoldItalic")):
    pdfmetrics.registerFont(TTFont(name, LIB % style))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFont(TTFont("Cinzel", os.path.join(HERE, "fonts", "Cinzel[wght].ttf")))

INK, GOLD, GREY = HexColor("#1c1814"), HexColor("#9a7430"), HexColor("#6b6258")
S = dict(
    title=ParagraphStyle("title", fontName="Cinzel", fontSize=40, leading=46, alignment=TA_CENTER, textColor=INK),
    sub=ParagraphStyle("sub", fontName="Serif-I", fontSize=17, leading=22, alignment=TA_CENTER, textColor=GOLD),
    meta=ParagraphStyle("meta", fontName="Serif", fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=GREY),
    chap=ParagraphStyle("chap", fontName="Cinzel", fontSize=15, leading=20, textColor=INK, spaceBefore=16, spaceAfter=2),
    time=ParagraphStyle("time", fontName="Serif", fontSize=9.5, leading=12, textColor=GOLD, spaceAfter=6),
    body=ParagraphStyle("body", fontName="Serif", fontSize=12, leading=18, alignment=TA_JUSTIFY, textColor=INK,
                        spaceAfter=4),
    note=ParagraphStyle("note", fontName="Serif-I", fontSize=9.5, leading=13, textColor=GREY, leftIndent=10,
                        spaceAfter=12),
    h2=ParagraphStyle("h2", fontName="Cinzel", fontSize=13, leading=18, textColor=INK, spaceBefore=14, spaceAfter=6),
    small=ParagraphStyle("small", fontName="Serif", fontSize=10.5, leading=15, textColor=INK, spaceAfter=4),
)

# O que aparece na tela em cada cena (descrição curta das imagens usadas)
VISUAL = {
    "01_turim": "Fotografia antiga da Piazza Carlo Alberto, em Turim.",
    "02_titulo": "Retrato de Nietzsche por Edvard Munch, com o título do vídeo.",
    "03_rocken": "A casa paroquial de Röcken, onde ele nasceu; Nietzsche jovem, em 1864.",
    "04_schopenhauer": "A escola de Pforta; retrato de Arthur Schopenhauer (1859).",
    "05_basileia": "Nietzsche em 1872, professor em Basileia.",
    "06_wagner": "Richard Wagner em 1871; a casa de Tribschen, no lago de Lucerna.",
    "07_tragedia": "Folha de rosto de O Nascimento da Tragédia (1872).",
    "08_ruptura": "Nietzsche por volta de 1875.",
    "09_andarilho": "O Caminhante sobre o Mar de Névoa, de Caspar David Friedrich; a casa de Nietzsche em Sils Maria.",
    "10_eterno_retorno": "O lago de Silvaplana, nos Alpes suíços.",
    "11_lou": "A fotografia de 1882 com Lou Salomé, Paul Rée e Nietzsche.",
    "12_deus_morto": "Nietzsche em 1882.",
    "13_zaratustra": "Folha de rosto de Assim Falou Zaratustra; texto datilografado por Nietzsche.",
    "14_abismo": "Litografia de Nietzsche por Edvard Munch (1906).",
    "15_1888": "A Piazza Carlo Alberto, em Turim.",
    "16_colapso": "Fotografia antiga do Palazzo Carignano, em Turim.",
    "17_overbeck": "Nietzsche doente, fotografado por Hans Olde (1899).",
    "18_silencio": "Nietzsche no leito, por Hans Olde; fotografia de 1899.",
    "19_elisabeth": "Elisabeth Nietzsche; a Villa Silberblick (Arquivo Nietzsche), em Weimar.",
    "20_morte": "O túmulo de Nietzsche em Röcken.",
    "21_causa": "Estudo da cabeça de Nietzsche, por Hans Olde.",
    "22_transcendeu": "Esboço de Nietzsche por Edvard Munch (1905–1906).",
    "23_final": "O Caminhante sobre o Mar de Névoa, de Caspar David Friedrich.",
    "24_outro": "A lápide de Nietzsche em Röcken, com a pergunta final na tela.",
}
HEADINGS = {"01_turim": "Introdução · Turim, janeiro de 1889", "02_titulo": "Abertura", "24_outro": "Encerramento"}


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def starts():
    """Tempo de início de cada cena, lido dos segmentos já renderizados."""
    if not WORK:
        return {}
    out, t = {}, 0.0
    for s in SCENES:
        out[s["id"]] = t
        p = os.path.join(WORK, "seg", s["id"] + ".mp4")
        if not os.path.exists(p):
            return {}
        t += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                            "-of", "csv=p=0", p]))
    out["_total"] = t
    return out


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Serif-I", 9); canvas.setFillColor(GREY)
    canvas.drawString(22 * mm, 13 * mm, "Nietzsche — o homem que transcendeu e enlouqueceu · roteiro")
    canvas.drawRightString(A4[0] - 22 * mm, 13 * mm, str(doc.page))
    canvas.restoreState()


def main():
    T = starts()
    mmss = lambda x: f"{int(x // 60):02}:{int(x % 60):02}"
    total = f" · duração {int(T['_total'] // 60)}min{int(T['_total'] % 60):02}s" if T else ""
    words = sum(len(s["text"].split()) for s in SCENES)
    story = [
        Spacer(1, 62 * mm),
        Paragraph("NIETZSCHE", S["title"]),
        Spacer(1, 4 * mm),
        HRFlowable(width="38%", thickness=1.2, color=GOLD, hAlign="CENTER"),
        Spacer(1, 5 * mm),
        Paragraph("o homem que transcendeu e enlouqueceu", S["sub"]),
        Spacer(1, 16 * mm),
        Paragraph("ROTEIRO DO VÍDEO", ParagraphStyle("k", parent=S["meta"], fontName="Cinzel", fontSize=11,
                                                      textColor=INK)),
        Spacer(1, 3 * mm),
        Paragraph(f"Narração completa{total} · {words} palavras", S["meta"]),
        Spacer(1, 58 * mm),
        Paragraph("O texto em tamanho normal é a narração, exatamente como é lida no vídeo.<br/>"
                  "As notas em itálico descrevem o que aparece na tela em cada trecho.", S["meta"]),
        PageBreak(),
    ]
    for s in SCENES:
        block = []
        head = HEADINGS.get(s["id"]) or s.get("chapter")
        if head:
            block.append(Paragraph(esc(head).upper(), S["chap"]))
            block.append(HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceAfter=3))
        if T:
            block.append(Paragraph(mmss(T[s["id"]]), S["time"]))
        block.append(Paragraph(esc(s["text"]), S["body"]))
        notes = ["Imagem: " + VISUAL[s["id"]]]
        if s.get("quote"):
            q, src = s["quote"]
            notes.append("Citação na tela: “" + esc(q.replace("\n", " ")) + "” (" + esc(src) + ")")
        if s.get("card"):
            a, ad, b, bd = s["card"]
            notes.append(f"Texto na tela: {esc(a)} — {esc(ad)} / {esc(b)} — {esc(bd)}")
        block.append(Paragraph("<br/>".join(notes), S["note"]))
        # mantém título, tempo e início do texto juntos; parágrafos longos podem quebrar de página
        story.append(KeepTogether(block) if len(s["text"]) < 900 else KeepTogether(block[:-2]))
        if len(s["text"]) >= 900:
            story.extend(block[-2:])

    story += [
        Paragraph("OBRAS CITADAS", S["h2"]),
        HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceAfter=5),
        Paragraph("O Nascimento da Tragédia (1872) · A Gaia Ciência (1882) · Assim Falou Zaratustra (1883–1885) · "
                  "Além do Bem e do Mal (1886) · Genealogia da Moral (1887) · O Caso Wagner, Crepúsculo dos Ídolos, "
                  "O Anticristo, Nietzsche contra Wagner e Ecce Homo (1888).", S["small"]),
        Paragraph("NOTAS", S["h2"]),
        HRFlowable(width="100%", thickness=0.6, color=GOLD, spaceAfter=5),
        Paragraph("O episódio do cavalo em Turim vem de relatos posteriores e pode ser, em parte, lendário; por isso "
                  "a narração o apresenta como relato. A causa da doença de Nietzsche continua em debate entre os "
                  "estudiosos. As citações são traduções livres para o português.", S["small"]),
    ]
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=24 * mm, rightMargin=24 * mm, topMargin=22 * mm,
                            bottomMargin=22 * mm, title="Nietzsche — o homem que transcendeu e enlouqueceu (roteiro)",
                            author="Canal de filosofia", subject="Roteiro de vídeo")
    doc.build(story, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print("ok", OUT)


if __name__ == "__main__":
    main()
