from PIL import Image, ImageDraw, ImageFilter

img = Image.open('photo.png').convert('RGB')
W, H = img.size
x0, y0 = int(W*0.26), 0
x1, y1 = int(W*0.70), int(H*0.70)
crop = img.crop((x0, y0, x1, y1))
cw, ch = crop.size  # 475 x 425

# polygon outlining the person, relative to crop coords
poly = [
    (0.29, 0.00), (0.62, 0.00), (0.72, 0.10), (0.76, 0.30),
    (0.75, 0.45), (0.72, 0.56), (0.78, 0.62), (0.86, 0.78),
    (0.90, 1.00), (0.18, 1.00), (0.22, 0.80), (0.24, 0.62),
    (0.25, 0.45), (0.245, 0.28), (0.255, 0.12),
]
mask = Image.new('L', (cw, ch), 0)
d = ImageDraw.Draw(mask)
d.polygon([(x*cw, y*ch) for x, y in poly], fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(2))

out = crop.convert('RGBA')
out.putalpha(mask)
out.save('photo-person.png')

prev = Image.new('RGB', (cw, ch), (12, 12, 14))
prev.paste(out, (0, 0), out)
prev.thumbnail((840, 840))
prev.save('ppv.png')
print('saved', cw, ch)
