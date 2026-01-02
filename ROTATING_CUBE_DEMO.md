# Rotating Cube Demo

Ein Beispiel für die Erstellung eines sich drehenden 3D-Würfels mit BlenderMCP.

## Was macht dieses Demo?

Das `rotating_cube_example.py` Skript erstellt automatisch:
- ✨ Einen 3D-Würfel in Blender
- 🔄 Animierte Rotation um mehrere Achsen (250 Frames)
- 📸 Korrekt positionierte Kamera für optimale Sicht
- 💡 Beleuchtung mit einer Sonnen-Lichtquelle
- 🎨 Ein blaues metallisches Material für den Würfel

## Verwendung

### Voraussetzungen

1. **Blender** muss installiert und geöffnet sein
2. **BlenderMCP Addon** muss installiert und aktiviert sein
3. Die **Verbindung zu Claude** muss im BlenderMCP Panel aktiv sein

### Schritt-für-Schritt Anleitung

1. **Blender starten**
   ```bash
   blender
   ```

2. **BlenderMCP Addon aktivieren**
   - Drücken Sie `N` um die Sidebar anzuzeigen
   - Finden Sie das "BlenderMCP" Tab
   - Klicken Sie auf "Connect to Claude"

3. **Das Skript ausführen**
   ```bash
   python3 rotating_cube_example.py
   ```

   oder

   ```bash
   ./rotating_cube_example.py
   ```

4. **Animation abspielen**
   - In Blender: Drücken Sie `SPACEBAR` um die Animation zu starten
   - Der Würfel rotiert kontinuierlich im 3D-Raum

## Technische Details

### Animation
- **Start Frame:** 1
- **End Frame:** 250
- **Rotation:** Der Würfel dreht sich um die X- und Z-Achse
- **Interpolation:** Linear für gleichmäßige Rotation

### Kamera Position
- **Location:** (7, -7, 5)
- **Rotation:** Optimiert für isometrische Ansicht des Würfels

### Material
- **Farbe:** Blau (RGB: 0.1, 0.5, 0.9)
- **Metallic:** 0.7
- **Roughness:** 0.3

### Beleuchtung
- **Typ:** Sonnen-Licht (SUN)
- **Energy:** 2.0
- **Position:** (5, 5, 10)

## Code-Struktur

Das Skript verwendet die BlenderMCP Socket-API um:

```python
# 1. Szene vorbereiten (alte Objekte löschen)
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# 2. Würfel erstellen
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))

# 3. Keyframes für Animation setzen
cube.rotation_euler = (0, 0, 0)
cube.keyframe_insert(data_path="rotation_euler", frame=1)

# 4. Material zuweisen
mat.use_nodes = True
bsdf.inputs['Base Color'].default_value = (0.1, 0.5, 0.9, 1.0)
```

## Fehlerbehebung

### "Connection refused"
- Stellen Sie sicher, dass Blender läuft
- Überprüfen Sie, ob das BlenderMCP Addon aktiviert ist
- Klicken Sie auf "Connect to Claude" im BlenderMCP Panel

### Animation spielt nicht ab
- Drücken Sie `SPACEBAR` in Blender
- Überprüfen Sie die Timeline (standardmäßig am unteren Rand)
- Stellen Sie sicher, dass Frame 1-250 sichtbar ist

### Würfel ist nicht sichtbar
- Drücken Sie `Home` oder scrollen Sie mit dem Mausrad
- Drücken Sie `Numpad 0` für Kamera-Ansicht
- Überprüfen Sie, ob Objekte im Outliner sichtbar sind

## Anpassungen

Sie können das Skript anpassen, um:

- **Rotationsgeschwindigkeit ändern:** Passen Sie `scene.frame_end` an
- **Farbe ändern:** Modifizieren Sie `bsdf.inputs['Base Color'].default_value`
- **Größe ändern:** Ändern Sie `size=2` beim `primitive_cube_add`
- **Mehrere Achsen:** Fügen Sie weitere Keyframes hinzu

## Beispiel für Modifikationen

### Schnellere Rotation (120 Frames)
```python
scene.frame_end = 120
cube.rotation_euler = (2 * math.pi, 0, 2 * math.pi)
cube.keyframe_insert(data_path="rotation_euler", frame=120)
```

### Rote Farbe
```python
bsdf.inputs['Base Color'].default_value = (0.9, 0.1, 0.1, 1.0)
```

### Größerer Würfel
```python
bpy.ops.mesh.primitive_cube_add(size=5, location=(0, 0, 0))
```

## Weitere Ressourcen

- [BlenderMCP GitHub](https://github.com/ahujasid/blender-mcp)
- [Blender Python API Dokumentation](https://docs.blender.org/api/current/)
- [Blender Animation Tutorials](https://www.blender.org/support/tutorials/)
