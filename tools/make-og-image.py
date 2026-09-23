from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG, CARD, STUB = "#f0f4fa", "#ffffff", "#e3ecfb"
INK, INK2, INK3, SKY, LINE = "#0f1d33", "#44536b", "#6b7a92", "#1d5fd1", "#d6dee9"

def jp(sz, bold=True):
    return ImageFont.truetype("C:/Windows/Fonts/" + ("meiryob.ttc" if bold else "meiryo.ttc"), sz)
def mono(sz, bold=True):
    return ImageFont.truetype("C:/Windows/Fonts/" + ("consolab.ttf" if bold else "consola.ttf"), sz)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
# 背景の淡い光
glow = Image.new("RGB", (W, H), BG)
ImageDraw.Draw(glow).ellipse((620, -260, 1500, 420), fill="#dbe7fa")
img = Image.blend(img, glow, 0.55)
d = ImageDraw.Draw(img)

# カード
CX0, CY0, CX1, CY1 = 90, 150, 1110, 500
d.rounded_rectangle((CX0, CY0, CX1, CY1), 26, fill=CARD)
SX = CX1 - 190                     # 半券の左端
d.rounded_rectangle((SX, CY0, CX1, CY1), 26, fill=STUB)
d.rectangle((SX, CY0, SX + 26, CY1), fill=STUB)

def dashed(x0, x1, y, color=LINE, dash=9, gap=7, w=2, vertical=False):
    t = x0
    while t < x1:
        e = min(t + dash, x1)
        d.line((y, t, y, e) if vertical else (t, y, e, y), fill=color, width=w)
        t = e + gap
dashed(CY0 + 20, CY1 - 20, SX, color="#c3d3ea", w=3, vertical=True)

# ヘッダ
d.text((132, 190), "BOARDING PASS", font=mono(22), fill=INK3)
d.text((770, 190), "NB 034", font=mono(22), fill=SKY)
dashed(132, SX - 40, 228)

# 区間
d.text((132, 258), "FROM", font=mono(18), fill=INK3)
d.text((132, 282), "HBY", font=mono(76), fill=INK)
d.text((134, 372), "飛行機・献血", font=jp(22, False), fill=INK2)
d.text((690, 258), "TO", font=mono(18), fill=INK3)
d.text((610, 282), "WEB", font=mono(76), fill=INK)
d.text((586, 372), "自作の Web サービス", font=jp(22, False), fill=INK2)
for i in range(9):                     # 点線の矢印
    x = 430 + i * 14
    d.line((x, 322, x + 8, 322), fill=SKY, width=4)
d.polygon([(556, 310), (580, 322), (556, 334), (562, 322)], fill=SKY)

dashed(132, SX - 40, 412)
for i, (k, v) in enumerate([("PASSENGER", "NOOBOW"), ("SEAT", "C#"), ("GATE", "JA-FLEET"), ("HOME", "KENKETSU")]):
    x = 132 + i * 185
    d.text((x, 432), k, font=mono(17), fill=INK3)
    d.text((x, 456), v, font=mono(26), fill=INK)

# 半券
d.text((SX + 54, 190), "CLASS", font=mono(18), fill=INK3)
d.text((SX + 50, 216), "DEV", font=mono(40), fill=SKY)
bx = SX + 62
for i, wd in enumerate([3, 6, 2, 8, 3, 3, 7, 2, 5, 3, 6, 2, 4, 8, 3, 5, 2, 6]):
    d.rectangle((bx, 290, bx + wd, 470), fill="#22324a")
    bx += wd + 6

# タイトル
d.text((92, 60), "NOOBOW", font=mono(58), fill=INK)
d.text((402, 84), "ぬーぼー", font=jp(28), fill=INK2)
d.text((92, 540), "飛行機と献血という趣味から、Web サービスを個人で開発・運営しています。", font=jp(26, False), fill=INK2)

# アバター（丸く切り抜き）
av = Image.open("C:/dev/portfolio/public/images/profile.webp").convert("RGBA").resize((150, 150), Image.LANCZOS)
plate = Image.new("RGBA", (150, 150), (227, 236, 251, 255))
mask = Image.new("L", (600, 600), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 599, 599), fill=255)
plate.alpha_composite(av)
plate.putalpha(mask.resize((150, 150), Image.LANCZOS))
img.paste(plate, (960, 20), plate)
d.ellipse((958, 18, 1112, 172), outline=SKY, width=4)

img.save("C:/dev/portfolio/public/images/og.png", optimize=True)
print(img.size)
