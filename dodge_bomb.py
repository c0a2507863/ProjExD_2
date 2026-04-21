import os
import random
import sys
import time
import pygame as pg

# 定数
WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か画面外かを判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向判定結果（True: 画面内, False: 画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    爆弾とこうかとんが衝突したら画面を暗くし、Game Overの文字とこうかとんを表示する
    引数：screen (描画対象のSurface)
    """
    # 半透明の黒い画面
    gg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    gg_img.set_alpha(150)

    # フォントと文字の設定
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    # こうかとん画像（泣いている顔）
    gk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    gk_rct_l = gk_img.get_rect(center=(WIDTH // 2 - 250, HEIGHT // 2))
    gk_rct_r = gk_img.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2))

    # 描画
    screen.blit(gg_img, [0, 0])
    screen.blit(txt, txt_rct)
    screen.blit(gk_img, gk_rct_l)
    screen.blit(gk_img, gk_rct_r)

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    10段階の大きさを変えた爆弾Surfaceのリストと加速度のリストを準備する
    戻り値：(爆弾Surfaceのリスト, 加速度のリスト)
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾のリストを初期化
    bb_imgs, bb_accs = init_bb_imgs()
    vx, vy = +5, +5
    
    # 爆弾の初期設定
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        # 画面の更新
        screen.blit(bg_img, [0, 0]) 

        # こうかとんの移動処理
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # 爆弾のサイズと速度の更新
        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        # Rectのサイズを現在の画像に合わせる
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]

        # 爆弾の移動と壁判定
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    # 実行環境のカレントディレクトリをスクリプトの場所に固定
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pg.init()
    main()
    pg.quit()
    sys.exit()