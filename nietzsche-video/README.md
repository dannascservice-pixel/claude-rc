# Nietzsche — o homem que transcendeu e enlouqueceu

Vídeo de ~13min38s (1080p) para canal de filosofia.

## Arquivos prontos (`saida/`)
- `nietzsche_o_homem_que_transcendeu_e_enlouqueceu.mp4` — vídeo final (não vai para o git por causa do tamanho)
- `nietzsche_legendas_ptBR.srt` — legendas para subir no YouTube
- `thumbnail.jpg` — miniatura 1280x720
- `descricao_youtube.txt` — título, descrição, capítulos e créditos das imagens

## Como regenerar
```
pip install edge-tts pillow numpy        # e ffmpeg instalado
python3 fetch_images.py work/img         # imagens do Wikimedia Commons + licenças
python3 tts.py work/audio                # narração (voz neural pt-BR)
python3 render.py work saida             # cenas, trilha, legendas e vídeo final
python3 extras.py work saida             # thumbnail e descrição
```
O texto da narração e a ordem das imagens ficam em `roteiro.py`.
