from PIL import Image

img = Image.open('photo-person.png').convert('RGBA')
OW = 100
OH = round(100*img.size[1]/img.size[0])
small = img.resize((OW, OH))
px = small.load()

CW, CH = 560, 500
out = Image.new('RGB', (CW, CH), (12, 12, 14))
op = out.load()
scale = max(CW/OW, CH/OH)
ox, oy = (CW-OW*scale)/2, (CH-OH*scale)/2

def boost(c): return min(255, (c/255)**0.85*360 + 8)

for y in range(0, OH):
    for x in range(0, OW):
        r, g, b, a = px[x, y]
        if a < 100:
            continue
        feat = max(0, a - 200) / 55.0   # 0..1
        bright = (r+g+b)/3
        r, g, b = boost(r), boost(g), boost(b)
        z = 1 - bright/255
        size = max(2, int(1.0 + z*1.6 + feat*3.2))
        al = 0.35 + z*0.4 + feat*0.25
        X, Y = int(ox+x*scale), int(oy+y*scale)
        for dy in range(size):
            for dx in range(size):
                xx, yy = X+dx, Y+dy
                if 0 <= xx < CW and 0 <= yy < CH:
                    br, bg_, bb = op[xx, yy]
                    op[xx, yy] = (int(br*(1-al)+r*al), int(bg_*(1-al)+g*al), int(bb*(1-al)+b*al))

out.save('dot-preview.png')
print('done')
