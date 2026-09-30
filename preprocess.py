from PIL import Image, ImageFilter
from collections import deque

img = Image.open('photo.png').convert('RGB')
W, H = img.size
x0, y0 = int(W*0.26), 0
x1, y1 = int(W*0.70), int(H*0.70)
crop = img.crop((x0, y0, x1, y1))
cw, ch = crop.size
px = crop.load()

TOL = 38          # color tolerance for region growing
TOL2 = TOL*TOL
bg = [[False]*cw for _ in range(ch)]

def close(c1, c2):
    return (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2 < TOL2

q = deque()
seeds = []
for x in range(cw):
    seeds += [(x, 0), (x, ch-1)]
for y in range(ch):
    seeds += [(0, y), (cw-1, y)]
for (sx, sy) in seeds:
    if not bg[sy][sx]:
        bg[sy][sx] = True
        q.append((sx, sy))
# multi-seed region growing: compare each pixel to its own parent (chained tolerance)
while q:
    cx, cy = q.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = cx+dx, cy+dy
        if 0 <= nx < cw and 0 <= ny < ch and not bg[ny][nx]:
            if close(px[nx, ny], px[cx, cy]):
                bg[ny][nx] = True
                q.append((nx, ny))

# hole fill: bg pixels not connected to border (already all connected by construction)
# -> invert: person = not bg
out = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
op = out.load()
kept = 0
for y in range(ch):
    for x in range(cw):
        if not bg[y][x]:
            r, g, b = px[x, y]
            op[x, y] = (r, g, b, 255)
            kept += 1

a = out.getchannel('A').filter(ImageFilter.GaussianBlur(1.0))
out.putalpha(a)
out.save('photo-cut.png')

prev = Image.new('RGB', (cw, ch), (12, 12, 14))
prev.paste(out, (0, 0), out)
prev.thumbnail((840, 840))
prev.save('pv.png')
print('kept', kept, 'of', cw*ch)
