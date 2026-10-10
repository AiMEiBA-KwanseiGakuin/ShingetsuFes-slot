import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("キャラクター移動")

x, y = 300, 220  # 四角の初期位置
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()  # キー入力を取得
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5
    if keys[pygame.K_UP]:
        y -= 5
    if keys[pygame.K_DOWN]:
        y += 5

    screen.fill((0, 0, 0))  # 背景を黒で塗りつぶし
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 40, 40))  # 白い四角を描画
    pygame.display.flip()  # 画面更新
    clock.tick(60)  # 60FPSで実行

pygame.quit()
