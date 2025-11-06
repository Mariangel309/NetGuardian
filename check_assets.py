import os

expected = [
  "data/images/entities/player.png",
  "data/images/entities/player/idle",
  "data/images/entities/player/run",
  "data/images/entities/enemy/idle",
  "data/images/entities/enemy1/idle",
  "data/images/entities/enemy2/idle",
  "data/images/particles/particle",
  "data/images/backgrounds/background_0.png",
  "data/images/backgrounds/background_1.png",
  "data/images/backgrounds/background_2.png",
  "data/images/menu_backgrounds/primero.png",
  "data/images/menu_backgrounds/titulo.png",
  "data/images/menu_backgrounds/jugar.png",
  "data/images/ui/enemy_icon.png",
  "data/images/souls/corazon.png",
  "data/fonts/pixel_font.ttf"
]

missing = []
for p in expected:
    if not os.path.exists(p):
        missing.append(p)

if missing:
    print("Faltan estos assets (o rutas incorrectas):")
    for m in missing:
        print(" -", m)
else:
    print("Todos los assets esperados existen (o las rutas son correctas).")
