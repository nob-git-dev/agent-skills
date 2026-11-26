#!/usr/bin/env python3
"""シェーダー記事のイラスト（SVG）を生成する。標準ライブラリのみ。"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

INK, MUTED, LINE = "#1F2937", "#6B7280", "#D1D5DB"
BLUE, BLUE_L = "#2563EB", "#DBEAFE"
ORANGE, ORANGE_L = "#EA580C", "#FFEDD5"
GREEN, GREEN_L = "#16A34A", "#DCFCE7"
PURPLE, PURPLE_L = "#7C3AED", "#EDE9FE"
GRAY_L = "#F3F4F6"
FONT = "Noto Sans CJK JP"


def svg(name, w, h, body, title):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
         f'font-family="{FONT}">\n<rect width="{w}" height="{h}" fill="#FFFFFF"/>\n'
         f'{t(32, 48, title, 26, INK, "bold")}\n{body}\n</svg>\n')
    (OUT / f"{name}.svg").write_text(s, encoding="utf-8")


def t(x, y, s, size=18, fill=INK, weight="normal", anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{s}</text>')


def r(x, y, w, h, fill, stroke="none", rx=8, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke=MUTED, sw=2, arrow=False, dash=None):
    a = f' marker-end="url(#arr{stroke[1:]})"' if arrow else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{a}{d}/>'


def defs(color=MUTED):
    ms = "".join(f'<marker id="arr{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
                 f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                 for c in (INK, MUTED, BLUE, ORANGE, GREEN, PURPLE))
    return f'<defs>{ms}</defs>'


def student(cx, cy, fill=BLUE, s=1.0):
    """机に座った生徒（頭＋胴）。"""
    return (f'<circle cx="{cx}" cy="{cy - 10*s}" r="{7*s}" fill="{fill}"/>'
            f'<rect x="{cx - 9*s}" y="{cy - 2*s}" width="{18*s}" height="{14*s}" rx="{4*s}" fill="{fill}"/>')


def shelf(x, y, w=110, h=200, label="本棚＝メモリ"):
    p = [r(x, y, w, h, "#FEF3C7", "#B45309", 6)]
    for i in range(1, 5):
        yy = y + i * h / 5
        p.append(line(x, yy, x + w, yy, "#B45309", 2))
        for j in range(5):
            p.append(r(x + 8 + j * 19, yy - 30, 12, 26, ["#F59E0B", "#FCD34D", "#D97706"][(i + j) % 3], rx=2))
    p.append(t(x + w / 2, y + h + 26, label, 16, "#92400E", "bold", "middle"))
    return "".join(p)


# 1. たとえの全体像: CPU と GPU と本棚
def fig1():
    b = [defs()]
    b.append(r(40, 80, 330, 330, GRAY_L, LINE, 12))
    b.append(t(205, 112, "CPU＝少数の優秀な先生", 19, INK, "bold", "middle"))
    for i, x in enumerate([110, 205, 300]):
        b.append(student(x, 200, PURPLE, 2.2))
    b.append(t(205, 290, "難しい問題・手順の多い仕事を", 16, MUTED, "normal", "middle"))
    b.append(t(205, 314, "1人ずつ素早くこなす", 16, MUTED, "normal", "middle"))
    b.append(t(205, 370, "数人〜数十人", 20, PURPLE, "bold", "middle"))
    b.append(r(400, 80, 400, 330, BLUE_L, LINE, 12))
    b.append(t(600, 112, "GPU＝同じ問題を一斉に解く大教室", 19, INK, "bold", "middle"))
    for row in range(7):
        for col in range(14):
            b.append(student(428 + col * 26, 145 + row * 28, BLUE, 0.85))
    b.append(t(600, 370, "数千人の生徒に、同じ号令", 20, BLUE, "bold", "middle"))
    b.append(shelf(840, 120, 120, 220))
    b.append(line(838, 230, 808, 230, ORANGE, 4, True))
    b.append(t(500, 455, "この記事のたとえ：生徒＝計算する部品、本棚＝メモリ、本棚との往復＝データの読み出し", 17, INK, "normal", "middle"))
    svg("01-classroom", 1000, 490, "".join(b), "この記事のたとえ：GPU は「大教室」、メモリは「本棚」")


# 2. ピクセルシェーダー
def fig2():
    b = [defs()]
    # 画面
    b.append(r(40, 80, 420, 280, "#111827", rx=10))
    import math
    cell = 20
    for yy in range(12):
        for xx in range(19):
            cx, cy = 60 + xx * cell + cell / 2, 100 + yy * cell + cell / 2
            d = math.hypot(cx - 210, cy - 180)
            v = max(0, min(1, 1 - d / 150))
            g = int(40 + 200 * v)
            b.append(f'<rect x="{60+xx*cell}" y="{100+yy*cell}" width="{cell-2}" height="{cell-2}" fill="rgb({g},{int(g*0.85)},{int(g*0.5)})"/>')
    b.append(r(60 + 9 * cell - 2, 100 + 5 * cell - 2, cell + 2, cell + 2, "none", ORANGE, 2, 3))
    b.append(t(250, 390, "フルHD＝横1920×縦1080＝約207万個の点", 17, INK, "bold", "middle"))
    b.append(line(470, 210, 560, 210, ORANGE, 3, True))
    b.append(r(570, 90, 390, 250, ORANGE_L, ORANGE, 12))
    b.append(t(765, 125, "1つの点に対する手順（シェーダー）", 18, INK, "bold", "middle"))
    steps = ["① 光がどの角度で当たるか", "② 表面の色・質感はどうか", "③ だから明るさはこう", "→ この点の色が決まる"]
    for i, s in enumerate(steps):
        b.append(t(600, 170 + i * 38, s, 18, INK if i < 3 else ORANGE, "bold" if i == 3 else "normal"))
    b.append(t(500, 440, "どの点も同じ手順で、隣の答えを待たずに計算できる → 生徒を何千人並べても仕事が分けられる", 18, BLUE, "bold", "middle"))
    svg("02-pixel-shader", 1000, 470, "".join(b), "シェーダーの元の仕事：画面の点ごとに陰影を計算する")


# 3. 年表
def fig3():
    b = [defs()]
    b.append(line(60, 250, 950, 250, INK, 4, True))
    ev = [
        (1988, "RenderMan", "ピクサーの規格で\nシェーダーが広まる", GRAY_L, MUTED, -1),
        (1999, "固定機能", "GeForce 256\n手順は回路に焼き付け", GRAY_L, MUTED, 1),
        (2001, "書けるシェーダー", "GeForce 3（DirectX 8）\n手順をプログラムで", BLUE_L, BLUE, -1),
        (2006, "統合シェーダー", "GeForce 8800 GTX\n128個が頂点もピクセルも", BLUE_L, BLUE, 1),
        (2007, "CUDA", "絵でない計算を\nそのまま書ける", GREEN_L, GREEN, -1),
        (2012, "AlexNet", "ゲーム用GPU 2枚で\n画像認識を大差で更新", GREEN_L, GREEN, 1),
        (2017, "行列専用の回路", "Tensor Core\nTPU論文・NPU", ORANGE_L, ORANGE, -1),
    ]
    xs = [95, 220, 345, 475, 605, 735, 870]
    for (yr, head, desc, fill, col, side), x in zip(ev, xs):
        b.append(f'<circle cx="{x}" cy="250" r="9" fill="{col}"/>')
        b.append(t(x, 285 if side < 0 else 228, str(yr), 18, col, "bold", "middle"))
        by = 90 if side < 0 else 305
        b.append(line(x, 241 if side < 0 else 259, x, by + 110 if side < 0 else by, col, 2, dash="4 4"))
        b.append(r(x - 74, by, 148, 110, fill, col, 10))
        b.append(t(x, by + 28, head, 16, INK, "bold", "middle"))
        for i, d in enumerate(desc.split("\n")):
            b.append(t(x, by + 56 + i * 24, d, 12, INK, "normal", "middle"))
    b.append(t(500, 460, "灰：絵だけの時代　青：手順を書けるようになる　緑：絵以外へ　橙：行列専用の回路が生まれる", 16, MUTED, "normal", "middle"))
    svg("03-timeline", 1000, 490, "".join(b), "シェーダーの進化：決まった仕事 → 書ける → 何でも計算 → 行列専用へ")


# 4. 分離 → 統合
def fig4():
    b = [defs()]
    b.append(r(40, 80, 430, 310, GRAY_L, LINE, 12))
    b.append(t(255, 112, "2006年より前：係が分かれている", 19, INK, "bold", "middle"))
    b.append(r(65, 135, 180, 170, PURPLE_L, PURPLE, 10))
    b.append(t(155, 160, "頂点係", 17, PURPLE, "bold", "middle"))
    for i in range(3):
        for j in range(3):
            b.append(student(105 + j * 50, 200 + i * 38, PURPLE, 1.0))
    b.append(r(265, 135, 180, 170, BLUE_L, BLUE, 10))
    b.append(t(355, 160, "ピクセル係", 17, BLUE, "bold", "middle"))
    for i in range(3):
        for j in range(3):
            b.append(student(305 + j * 50, 200 + i * 38, BLUE if (i + j) % 2 else "#93C5FD", 1.0))
    b.append(t(255, 340, "頂点の多い場面ではピクセル係が暇、", 16, MUTED, "normal", "middle"))
    b.append(t(255, 364, "その逆もある", 16, MUTED, "normal", "middle"))
    b.append(line(478, 235, 542, 235, ORANGE, 5, True))
    b.append(r(550, 80, 410, 310, GREEN_L, GREEN, 12))
    b.append(t(755, 112, "GeForce 8800 GTX：札が外れる", 19, INK, "bold", "middle"))
    for i in range(4):
        for j in range(8):
            b.append(student(600 + j * 44, 165 + i * 38, GREEN, 1.0))
    b.append(t(755, 340, "128個の同じ計算ユニットが", 16, INK, "normal", "middle"))
    b.append(t(755, 364, "頂点もピクセルもその場で分担", 16, INK, "normal", "middle"))
    b.append(t(500, 440, "何でも解ける生徒が128人いるなら、絵でなくてもいいのでは？ → CUDA（2007年）へ", 19, GREEN, "bold", "middle"))
    svg("04-unified-shader", 1000, 470, "".join(b), "統合シェーダー：「頂点係」「ピクセル係」の札が外れた")


# 5. 行列の掛け算
def fig5():
    b = [defs()]
    def grid(x, y, n, size, hl_row=None, hl_col=None, hl_cell=None, color=BLUE):
        p = []
        for i in range(n):
            for j in range(n):
                f = "#FFFFFF"
                if hl_row is not None and i == hl_row:
                    f = BLUE_L
                if hl_col is not None and j == hl_col:
                    f = GREEN_L
                if hl_cell is not None and (i, j) == hl_cell:
                    f = ORANGE
                p.append(f'<rect x="{x+j*size}" y="{y+i*size}" width="{size}" height="{size}" fill="{f}" stroke="{LINE}"/>')
        return "".join(p)
    b.append(grid(50, 110, 6, 32, hl_row=2))
    b.append(t(146, 330, "左の表：1行（青）", 16, BLUE, "bold", "middle"))
    b.append(t(270, 210, "×", 40, INK, "bold", "middle"))
    b.append(grid(300, 110, 6, 32, hl_col=4))
    b.append(t(396, 330, "右の表：1列（緑）", 16, GREEN, "bold", "middle"))
    b.append(t(520, 210, "＝", 40, INK, "bold", "middle"))
    b.append(grid(550, 110, 6, 32, hl_cell=(2, 4)))
    b.append(t(646, 330, "答えの1マス（橙）", 16, ORANGE, "bold", "middle"))
    b.append(r(770, 100, 200, 220, GRAY_L, LINE, 10))
    b.append(t(870, 130, "1マス＝", 17, INK, "bold", "middle"))
    b.append(t(870, 160, "青と緑を順に掛けて", 15, INK, "normal", "middle"))
    b.append(t(870, 185, "全部足す", 15, INK, "normal", "middle"))
    b.append(t(870, 230, "答えのマスどうしは", 15, INK, "normal", "middle"))
    b.append(t(870, 255, "互いに無関係", 17, ORANGE, "bold", "middle"))
    b.append(t(870, 285, "＝ピクセルと同じ", 15, INK, "normal", "middle"))
    b.append(r(50, 360, 920, 100, ORANGE_L, ORANGE, 10))
    b.append(t(80, 395, "4096×4096 の表どうし：掛け算と足し算 4096×4096×4096 ＝ 約687億組", 19, INK, "bold"))
    b.append(t(80, 433, "使う数字は表3枚で約5000万個だけ → 1つの数字を約4096回も使い回す計算", 19, ORANGE, "bold"))
    svg("05-matmul", 1000, 490, "".join(b), "AI の計算の正体：行列（数字の表）の掛け算")


# 6. 素朴 vs タイリング
def fig6():
    b = [defs(ORANGE)]
    b.append(r(30, 75, 455, 360, GRAY_L, LINE, 12))
    b.append(t(257, 105, "素朴なやり方：掛けるたびに本棚へ", 18, INK, "bold", "middle"))
    b.append(shelf(60, 140, 90, 160))
    for i in range(4):
        y = 150 + i * 42
        b.append(student(400, y + 10, BLUE, 1.2))
        b.append(line(395, y + 5, 160, 200 + (i - 1.5) * 15, ORANGE, 2, True, "6 4"))
    b.append(t(257, 360, "1マスにつき 8192回 × 約1680万マス", 16, INK, "normal", "middle"))
    b.append(t(257, 392, "＝ 約1374億回の往復", 21, ORANGE, "bold", "middle"))
    b.append(t(257, 420, "必要な数字（5000万個）の約2700倍", 15, MUTED, "normal", "middle"))
    b.append(r(515, 75, 455, 360, GREEN_L, GREEN, 12))
    b.append(t(742, 105, "タイリング：班の机に置いて使い回す", 18, INK, "bold", "middle"))
    b.append(shelf(545, 140, 90, 160))
    b.append(line(645, 220, 700, 220, ORANGE, 4, True))
    b.append(r(705, 170, 120, 100, "#FFFFFF", GREEN, 8))
    b.append(t(765, 196, "班の机", 15, GREEN, "bold", "middle"))
    b.append(t(765, 218, "共有メモリ", 13, MUTED, "normal", "middle"))
    for k in range(3):
        b.append(r(722 + k * 30, 232, 24, 24, ORANGE_L, ORANGE, 3))
    for i in range(4):
        b.append(student(880, 150 + i * 42 + 10, BLUE, 1.2))
        b.append(line(872, 155 + i * 42, 830, 220, GREEN, 2))
    b.append(t(742, 360, "32×32 の区画をまとめて運び、全員で何度も使う", 16, INK, "normal", "middle"))
    b.append(t(742, 392, "往復は約32分の1に", 21, GREEN, "bold", "middle"))
    b.append(t(742, 420, "それでも1回の命令で計算は1組ずつ", 15, MUTED, "normal", "middle"))
    svg("06-tiling", 1000, 460, "".join(b), "シェーダーでの行列計算：本棚との往復をどう減らすか")


# 7. Tensor Core
def fig7():
    b = [defs()]
    b.append(r(40, 80, 420, 300, GRAY_L, LINE, 12))
    b.append(t(250, 112, "シェーダーの生徒", 20, INK, "bold", "middle"))
    b.append(student(250, 190, BLUE, 2.4))
    b.append(r(170, 240, 160, 50, "#FFFFFF", BLUE, 8))
    b.append(t(250, 272, "a × b + c", 22, BLUE, "bold", "middle"))
    b.append(t(250, 340, "1回の命令で 1組", 22, BLUE, "bold", "middle"))
    b.append(t(500, 240, "→", 40, INK, "bold", "middle"))
    b.append(r(540, 80, 420, 300, ORANGE_L, ORANGE, 12))
    b.append(t(750, 112, "Tensor Core（2017年 Volta〜）", 20, INK, "bold", "middle"))
    for i in range(4):
        for j in range(4):
            b.append(f'<rect x="{600+j*30}" y="{140+i*30}" width="28" height="28" fill="{ORANGE}" opacity="{0.45+0.12*((i+j)%4)}"/>')
    b.append(t(660, 285, "4×4 のはんこ", 17, ORANGE, "bold", "middle"))
    b.append(t(830, 175, "小さな行列の", 16, INK, "normal", "middle"))
    b.append(t(830, 200, "掛け算を丸ごと", 16, INK, "normal", "middle"))
    b.append(t(830, 225, "一発で押す", 16, INK, "normal", "middle"))
    b.append(t(750, 340, "1サイクルで 64組（＝64倍）", 22, ORANGE, "bold", "middle"))
    b.append(t(500, 430, "今の GPU の AI 性能の大部分はこの「はんこ」から。主役はもうシェーダーではない", 18, INK, "bold", "middle"))
    svg("07-tensor-core", 1000, 460, "".join(b), "Tensor Core：生徒に「4×4 のはんこ」を配った")


# 8. シストリックアレイ
def fig8():
    b = [defs(BLUE)]
    n, size, x0, y0 = 5, 62, 250, 120
    for i in range(n):
        for j in range(n):
            x, y = x0 + j * size, y0 + i * size
            b.append(r(x + 4, y + 4, size - 8, size - 8, GREEN_L, GREEN, 6))
            b.append(t(x + size / 2, y + size / 2 + 6, "×＋", 15, GREEN, "bold", "middle"))
            if j < n - 1:
                b.append(line(x + size - 4, y + size / 2, x + size + 4, y + size / 2, BLUE, 2, True))
            if i < n - 1:
                b.append(line(x + size / 2, y + size - 4, x + size / 2, y + size + 4, ORANGE, 2))
    for i in range(n):
        b.append(line(x0 - 70, y0 + i * size + size / 2, x0 + 2, y0 + i * size + size / 2, BLUE, 3, True))
        b.append(r(x0 - 110, y0 + i * size + 18, 34, 26, BLUE_L, BLUE, 4))
    b.append(t(x0 - 93, y0 - 12, "入力の数字", 15, BLUE, "bold", "middle"))
    b.append(t(x0 + n * size / 2, y0 - 12, "掛け算器のマス目（初代TPUは 256×256）", 16, INK, "bold", "middle"))
    for j in range(n):
        b.append(line(x0 + j * size + size / 2, y0 + n * size - 2, x0 + j * size + size / 2, y0 + n * size + 34, ORANGE, 3, True))
    b.append(t(x0 + n * size / 2, y0 + n * size + 64, "下へ：途中の合計が流れて答えになる", 15, ORANGE, "bold", "middle"))
    b.append(r(620, 110, 350, 300, GRAY_L, LINE, 10))
    lines_ = [("各マスの生徒は本棚に行かない", INK, "bold"),
              ("左から来た数字 × 自分の席の数字", INK, "normal"),
              ("＋ 上から来た途中の合計", INK, "normal"),
              ("→ 右と下へ渡す（バケツリレー）", BLUE, "bold"),
              ("", INK, "normal"),
              ("65536個 × 7億回/秒 × 2", INK, "normal"),
              ("＝ 約92兆回/秒（92 TOPS）", GREEN, "bold"),
              ("初代TPU（2015年）は 75W のカード", MUTED, "normal")]
    for i, (s, c, w) in enumerate(lines_):
        b.append(t(640, 145 + i * 33, s, 16, c, w))
    b.append(t(500, 545, "「1つの数字を何千回も使い回す」行列の性質を、配線の形そのもので実現した", 18, INK, "bold", "middle"))
    svg("08-systolic", 1000, 575, "".join(b), "TPU のシストリックアレイ：数字がバケツリレーで流れる")


# 9. TPU と NPU
def fig9():
    b = [defs()]
    b.append(r(40, 80, 440, 320, BLUE_L, BLUE, 12))
    b.append(t(260, 115, "TPU：データセンターの大教室", 20, INK, "bold", "middle"))
    for k in range(4):
        b.append(r(80 + k * 95, 140, 80, 120, "#FFFFFF", BLUE, 6))
        for m in range(5):
            b.append(line(88 + k * 95, 160 + m * 20, 152 + k * 95, 160 + m * 20, BLUE, 2))
    b.append(t(260, 300, "巨大なモデルを、最大の速さで", 18, INK, "normal", "middle"))
    b.append(t(260, 330, "大量に回す", 18, INK, "normal", "middle"))
    b.append(t(260, 375, "目標：速さと電気代あたりの量", 18, BLUE, "bold", "middle"))
    b.append(r(520, 80, 440, 320, PURPLE_L, PURPLE, 12))
    b.append(t(740, 115, "NPU：手元の機器の小さな教室", 20, INK, "bold", "middle"))
    b.append(r(700, 140, 80, 140, "#FFFFFF", PURPLE, 14))
    b.append(r(715, 160, 50, 30, PURPLE_L, PURPLE, 4))
    b.append(t(740, 181, "NPU", 13, PURPLE, "bold", "middle"))
    b.append(r(722, 225, 36, 18, GREEN_L, GREEN, 3))
    b.append(r(722, 225, 26, 18, GREEN, rx=3))
    b.append(t(740, 300, "顔認証・写真処理・音声などを", 18, INK, "normal", "middle"))
    b.append(t(740, 330, "精度を落として小さく回す", 18, INK, "normal", "middle"))
    b.append(t(740, 375, "目標：電池を減らさないこと", 18, PURPLE, "bold", "middle"))
    b.append(t(500, 445, "中身の考え方は同じ側（行列専用の回路）。違うのは目標と割り切りの大きさ", 18, INK, "bold", "middle"))
    svg("09-tpu-npu", 1000, 475, "".join(b), "TPU と NPU：考え方は同じ、目標が違う")


# 10. 結論のスペクトル
def fig10():
    b = [defs()]
    b.append(f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient></defs>')
    b.append(r(60, 150, 880, 18, "url(#g)", rx=9))
    b.append(t(60, 135, "柔軟（何でも計算できる）", 17, BLUE, "bold"))
    b.append(t(940, 135, "効率（決まった計算を省電力で大量に）", 17, GREEN, "bold", "end"))
    items = [(120, "シェーダー", "使い回しは\nソフトの工夫\n（班の机）", BLUE_L, BLUE),
             (380, "Tensor Core", "使い回しは\nはんこの中だけ", ORANGE_L, ORANGE),
             (640, "TPU", "使い回しを\n配線に焼き込む\n（バケツリレー）", GREEN_L, GREEN),
             (860, "NPU", "TPUの考え方を\n小型・低精度に", PURPLE_L, PURPLE)]
    for x, name, desc, fill, col in items:
        b.append(f'<circle cx="{x}" cy="159" r="14" fill="#FFFFFF" stroke="{col}" stroke-width="4"/>')
        b.append(r(x - 95, 200, 190, 160, fill, col, 10))
        b.append(t(x, 232, name, 19, col, "bold", "middle"))
        for i, d in enumerate(desc.split("\n")):
            b.append(t(x, 270 + i * 28, d, 16, INK, "normal", "middle"))
    b.append(t(500, 410, "違いは「速さ」ではなく「同じ数字を、どこで何回使い回せる形か」", 21, INK, "bold", "middle"))
    b.append(t(500, 445, "そしてどれも最後は「本棚から届く速さ」＝メモリ帯域に縛られる", 17, ORANGE, "bold", "middle"))
    svg("10-spectrum", 1000, 480, "".join(b), "まとめ：使い回しをどこで実現するか")


for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10):
    f()
print("ok", len(list(OUT.glob("*.svg"))))
