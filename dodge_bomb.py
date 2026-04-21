import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か画面が以下を判定する関数
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向判定結果（True: 画面内, False: 画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:   #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  #縦方向判定
        tate = False
    return yoko, tate
    

def gameover(screen: pg.Surface) -> None:
    gg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(gg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    gg_img.set_alpha(100)

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    

    gk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    gk_rct = gk_img.get_rect()
    gk_rct.center = 300, 200

    gg_img.blit(txt, [400, 265])  
    gg_img.blit(gk_img, [200, 265]) 
    gg_img.blit(gk_img, [800, 265])  
    screen.blit(gg_img, [0, 0])

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    ookisa = [1,2,3,4,5,6,7,8,9,10]
    kasoku = [1,2,3,4,5,6,7,8,9,10]



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))                       #爆弾用の空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)   #爆弾を描く
    bb_img.set_colorkey((0, 0, 0))                      #黒い枠を透明にする
    bb_rct = bb_img.get_rect()                          #爆弾Rectを取得する
    bb_rct.centerx = random.randint(0, WIDTH)           #爆弾の初期座標x
    bb_rct.centery = random.randint(0, HEIGHT)          #爆弾の初期座標y
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾の衝突判定
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)          #爆弾を動かす
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)     #爆弾を表示させる
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
