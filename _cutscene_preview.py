# -*- coding: utf-8 -*-
import os, sys
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()
pygame.mixer.init()

_fake = type('S', (), {'play': lambda *a,**k: None, 'stop': lambda *a: None})
pygame.mixer.Sound = lambda **k: _fake()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jogo

FPS = jogo.FPS

# Tempos (segundos) de captura de cada cena
cenas = [
    (2.0,  "cena0_batalha_final.png"),
    (6.0,  "cena1_dispositivo.png"),
    (11.0, "cena2_distorcao.png"),
    (17.0, "cena3_buraco_negro.png"),
    (22.0, "cena4_sugado.png"),
    (27.0, "cena5_saga_continua.png"),
]

for t_seg, filename in cenas:
    g = jogo.Game.__new__(jogo.Game)
    g.highscore = 0
    g.sfx = {}; g.music = None
    g.state = jogo.Game.CUTSCENE
    g._init_game()
    g.state = jogo.Game.CUTSCENE
    g.cutscene_timer = int(t_seg * FPS)
    g.ct_px = float(jogo.W // 2)
    g.ct_py = float(jogo.H - 120)
    g.ct_bangle = t_seg * 0.022 * FPS

    # Simula posição da nave para cenas 3-4
    import math
    PI2 = 2 * math.pi
    if t_seg >= 14:
        prog = min(1.0, (t_seg - 14) / 11.0)
        angle = -math.pi/2 + prog * 5 * PI2
        radius = max(0.0, (1.0 - prog) * 200)
        g.ct_px = jogo.W//2 + math.cos(angle)*radius*(1-prog*0.5)
        g.ct_py = (jogo.H-120) + (jogo.H//2-(jogo.H-120))*prog + math.sin(angle)*radius*0.35

    # Gera partículas simuladas
    import random
    random.seed(int(t_seg * 10))
    if t_seg < 4:
        for _ in range(18):
            bx = jogo.W//2 + random.uniform(-20,20)
            jogo.spawn_particles(g.particles, bx, 130+random.uniform(-8,8),
                                 jogo.PHASES[9]['bc'], n=4, spd=3)
    elif t_seg < 8:
        for _ in range(8):
            jogo.spawn_particles(g.particles, jogo.W//2, 130, (200,0,255), n=3, spd=5)
    elif t_seg < 14:
        for _ in range(12):
            jogo.spawn_particles(g.particles,
                jogo.W//2+random.uniform(-20,20), jogo.H//2+random.uniform(-20,20),
                jogo.PHASES[9]['ui'], n=3, spd=4)

    # Avança partículas para parecer que estão no meio da animação
    for p in g.particles:
        age = random.uniform(0.1, 0.5)
        p[4] = max(0.01, p[5] - age)

    g._draw_cutscene()
    jogo.screen.blit(jogo._scanline, (0,0))
    pygame.image.save(jogo.screen, filename)
    print(f"Salvo: {filename}")

pygame.quit()
print("Todas as cenas capturadas!")
