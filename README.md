# Rainbow Drift

A small browser drifting game featuring a Blender-authored unicorn kart rendered on an HTML canvas.

![Rainbow Drift gameplay](playable-desktop.jpg)

## Play

Extract `rainbow-drift.zip` and open `index.html`, or serve the source directory locally:

```sh
python3 -m http.server 8000 --directory game
```

Then open <http://localhost:8000>.

## Controls

- Drive with WASD or the arrow keys.
- Hold a steering key above 35 km/h to drift and charge a boost.
- Release steering to use the boost.
- Press R to restart.
- On a touch screen, use the four on-screen controls.

## Source

- `game/` contains the dependency-free browser game.
- `rainbow-drift.blend` is the Blender source scene.
- `create_asset.py` rebuilds the Blender scene, preview, and web kart geometry.
- `rainbow-drift.zip` contains the ready-to-play game.

## Rebuild and check

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python create_asset.py
(cd game && zip -9 -q ../rainbow-drift.zip index.html kart.js)
unzip -t rainbow-drift.zip
```

## License

Copyright (C) 2026 Andrea Liliana Griffiths

Licensed under the GNU Affero General Public License v3.0 only. See [LICENSE](LICENSE).
