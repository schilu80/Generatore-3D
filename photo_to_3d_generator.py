# build_exe.py
"""
Script per creare eseguibile del Generatore 3D
Usa PyInstaller per creare .exe (Windows), .app (Mac), o binario (Linux)
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """Installa PyInstaller se non presente"""
    print("📦 Verifico PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller già installato")
    except ImportError:
        print("⬇️ Installazione PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installato")

def create_spec_file():
    """Crea file .spec per configurazione avanzata"""
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['photo_to_3d_generator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinterdnd2',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'trimesh',
        'numpy',
        'scipy',
        'scipy.ndimage',
        'scipy.spatial',
        'skimage',
        'skimage.measure',
        'requests',
        'json',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'pytest',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Generatore3D',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = no console, True = with console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

# Per Mac
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Generatore3D.app',
        icon='icon.icns' if os.path.exists('icon.icns') else None,
        bundle_identifier='com.ai.generatore3d',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
        },
    )
"""
    
    with open('generatore3d.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ File .spec creato")

def build_executable():
    """Compila l'eseguibile"""
    print("\n🔨 Inizio compilazione...")
    print("⏳ Questo potrebbe richiedere alcuni minuti...\n")
    
    # Comandi PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',  # Un singolo file
        '--windowed',  # Senza console (GUI)
        '--name=Generatore3D',
        '--clean',  # Pulisci build precedenti
    ]
    
    # Aggiungi hidden imports
    hidden_imports = [
        'tkinterdnd2',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'scipy.ndimage',
        'scipy.spatial',
        'skimage.measure',
    ]
    
    for imp in hidden_imports:
        cmd.extend(['--hidden-import', imp])
    
    # Escludi moduli non necessari per ridurre dimensione
    excludes = [
        'matplotlib',
        'pandas',
        'pytest',
        'IPython',
        'jupyter',
    ]
    
    for exc in excludes:
        cmd.extend(['--exclude-module', exc])
    
    # Icona (se esiste)
    if os.path.exists('icon.ico'):
        cmd.extend(['--icon', 'icon.ico'])
    
    # File principale
    cmd.append('photo_to_3d_generator.py')
    
    # Esegui
    try:
        subprocess.check_call(cmd)
        print("\n✅ Compilazione completata!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Errore durante compilazione: {e}")
        return False

def create_installer_script():
    """Crea script installer per distribuzione"""
    
    # Script batch per Windows
    batch_content = """@echo off
echo ========================================
echo Generatore 3D - Installer
echo ========================================
echo.

echo Installazione dipendenze opzionali...
echo.

REM Controlla Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Scarica Python da: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/2] Installazione COLMAP (opzionale per fotogrammetria)...
echo Per fotogrammetria, scarica COLMAP da:
echo https://colmap.github.io/install.html
echo.

echo [2/2] Installazione Blender (opzionale per export .blend)...
echo Per export .blend, scarica Blender da:
echo https://www.blender.org/download/
echo.

echo ========================================
echo Installazione completata!
echo ========================================
echo.
echo Esegui: Generatore3D.exe
echo.
pause
"""
    
    with open('installer_windows.bat', 'w') as f:
        f.write(batch_content)
    
    # Script shell per Linux/Mac
    shell_content = """#!/bin/bash

echo "========================================"
echo "Generatore 3D - Installer"
echo "========================================"
echo ""

# Controlla Python
if ! command -v python3 &> /dev/null; then
    echo "ERRORE: Python non trovato!"
    echo "Installa Python 3.8+ dal tuo package manager"
    exit 1
fi

echo "[1/3] Installazione COLMAP (opzionale per fotogrammetria)..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux: sudo apt install colmap"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Mac: brew install colmap"
fi
echo ""

echo "[2/3] Installazione Blender (opzionale)..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Linux: sudo snap install blender --classic"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Mac: brew install --cask blender"
fi
echo ""

echo "[3/3] Installazione rembg (opzionale per rimozione sfondo)..."
pip3 install rembg
echo ""

echo "========================================"
echo "Installazione completata!"
echo "========================================"
echo ""
echo "Esegui: ./Generatore3D"
echo ""
"""
    
    with open('installer_unix.sh', 'w') as f:
        f.write(shell_content)
    
    # Rendi eseguibile
    os.chmod('installer_unix.sh', 0o755)
    
    print("✅ Script installer creati")

def create_readme():
    """Crea README per distribuzione"""
    readme_content = """# Generatore 3D - Guida Utente

## 🚀 Avvio Rapido

### Windows
1. Doppio click su `Generatore3D.exe`
2. (Opzionale) Esegui `installer_windows.bat` per dipendenze extra

### Mac
1. Doppio click su `Generatore3D.app`
2. (Opzionale) Esegui `./installer_unix.sh` per dipendenze extra

### Linux
1. Esegui `./Generatore3D`
2. (Opzionale) Esegui `./installer_unix.sh` per dipendenze extra

---

## 📋 Requisiti

**Richiesti (già inclusi nell'eseguibile):**
- Python 3.8+
- tkinterdnd2
- Pillow (PIL)
- trimesh
- numpy
- scipy
- scikit-image
- requests

**Opzionali (per funzionalità extra):**
- COLMAP - Fotogrammetria multi-foto (https://colmap.github.io)
- Blender - Export formato .blend (https://www.blender.org)
- rembg - Rimozione sfondo migliorata (`pip install rembg`)

---

## 🎯 Metodi Disponibili

### Foto Singola (10 metodi):
1. **Depth Map** - Veloce, 5 secondi
2. **Normal Map** - Dettagli superficie
3. **Estrusione** - Solido per stampa 3D
4. **Rotazione 360°** - Oggetti simmetrici
5. **AI Completo 360°** - Raccomandato, 30 secondi
6. **NeRF** - Fotorealistico, 3-5 minuti
7. **Cloud AI** - Qualità massima (richiede API key)
8. **Gaussian Splatting** - Real-time viewer HTML
9. **Point-E** - Diffusion OpenAI
10. **DreamFusion** - Text-to-3D con prompt

### Foto Multiple:
- **Fotogrammetria** - Ricostruzione precisa con COLMAP (8-10+ foto)

---

## 🔑 API Keys (Opzionali)

Per Cloud AI e servizi avanzati:

```bash
# Windows (PowerShell)
$env:TRIPO_API_KEY="your-key"
$env:MESHY_API_KEY="your-key"
$env:OPENAI_API_KEY="your-key"

# Linux/Mac
export TRIPO_API_KEY="your-key"
export MESHY_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
```

**Dove ottenere le chiavi:**
- TripoSR: https://platform.tripo3d.ai (50 generazioni/mese gratis)
- Meshy: https://www.meshy.ai (200 credits gratis)
- OpenAI: https://platform.openai.com

---

## 💡 Consigli per Migliori Risultati

### Foto Singola:
✅ Immagine chiara, ben illuminata
✅ Sfondo uniforme (bianco/nero)
✅ Oggetto centrato
✅ Risoluzione 1000x1000px o superiore

### Fotogrammetria (multi-foto):
✅ 8-10+ foto da diverse angolazioni
✅ Sovrapposizione 60-80% tra foto
✅ Illuminazione costante
✅ Sfondo statico

### Text-to-3D (DreamFusion):
✅ Prompt dettagliati in inglese
✅ Specifica stile (realistic, cartoon, etc.)
✅ Menziona materiali (metal, wood, etc.)

---

## 📁 Formati Export

- **PLY** - Point cloud, universale
- **OBJ** - Mesh con texture
- **STL** - Stampa 3D
- **BLEND** - Blender nativo (richiede Blender)
- **HTML** - Viewer interattivo (solo Gaussian Splatting)

---

## 🐛 Troubleshooting

### "COLMAP non trovato"
- Installa COLMAP: https://colmap.github.io/install.html
- Oppure usa metodi per foto singola

### "Blender non trovato"
- Installa Blender: https://www.blender.org
- Oppure disabilita export .blend

### Eseguibile non si avvia
- Windows: Esegui come amministratore
- Mac: Sistema > Preferenze > Sicurezza, consenti app
- Linux: `chmod +x Generatore3D`

### Memoria insufficiente
- Riduci risoluzione immagini
- Usa un solo metodo alla volta
- Chiudi applicazioni inutilizzate

---

## 📞 Supporto

Per problemi, suggerimenti o contributi:
- GitHub: [link-repo]
- Email: support@example.com

---

## 📄 Licenza

MIT License - Libero per uso personale e commerciale

---

## 🙏 Credits

Basato su tecnologie:
- NeRF (Neural Radiance Fields)
- Gaussian Splatting (3DGS)
- Point-E (OpenAI)
- DreamFusion (Google Research)
- COLMAP (Photogrammetry)
"""
    
    with open('README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README creato")

def package_distribution():
    """Pacchettizza per distribuzione"""
    print("\n📦 Creazione pacchetto distribuzione...")
    
    # Crea cartella dist se non esiste
    dist_folder = 'dist_package'
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    os.makedirs(dist_folder)
    
    # Copia eseguibile
    if os.path.exists('dist/Generatore3D.exe'):
        shutil.copy('dist/Generatore3D.exe', dist_folder)
    elif os.path.exists('dist/Generatore3D'):
        shutil.copy('dist/Generatore3D', dist_folder)
    elif os.path.exists('dist/Generatore3D.app'):
        shutil.copytree('dist/Generatore3D.app', 
                       os.path.join(dist_folder, 'Generatore3D.app'))
    
    # Copia file accessori
    files_to_copy = [
        'README.txt',
        'installer_windows.bat',
        'installer_unix.sh',
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, dist_folder)
    
    print(f"✅ Pacchetto creato in: {dist_folder}/")
    print("\n📋 Contenuto pacchetto:")
    for item in os.listdir(dist_folder):
        size = os.path.getsize(os.path.join(dist_folder, item))
        size_mb = size / (1024 * 1024)
        print(f"  - {item} ({size_mb:.1f} MB)")

def main():
    """Main build process"""
    print("=" * 50)
    print("🚀 BUILD ESEGUIBILE GENERATORE 3D")
    print("=" * 50)
    print()
    
    # Step 1: Verifica file sorgente
    if not os.path.exists('photo_to_3d_generator.py'):
        print("❌ ERRORE: File 'photo_to_3d_generator.py' non trovato!")
        print("   Assicurati di essere nella cartella corretta")
        return
    
    print("✅ File sorgente trovato")
    
    # Step 2: Installa PyInstaller
    install_pyinstaller()
    
    # Step 3: Crea file accessori
    create_readme()
    create_installer_script()
    
    # Step 4: Build
    print("\n" + "=" * 50)
    print("Inizio build...")
    print("=" * 50 + "\n")
    
    success = build_executable()
    
    if success:
        # Step 5: Pacchettizza
        package_distribution()
        
        print("\n" + "=" * 50)
        print("✅ BUILD COMPLETATO CON SUCCESSO!")
        print("=" * 50)
        print()
        print("📦 Eseguibile creato in: dist_package/")
        print()
        print("📋 Prossimi passi:")
        print("  1. Testa l'eseguibile")
        print("  2. Crea archivio ZIP per distribuzione")
        print("  3. (Opzionale) Firma l'eseguibile")
        print()
        print("🎉 Pronto per distribuzione!")
    else:
        print("\n❌ Build fallito. Controlla gli errori sopra.")

if __name__ == '__main__':
    main()
