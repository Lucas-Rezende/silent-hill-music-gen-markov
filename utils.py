#########################################################################
"""
utils.py

Definições de constantes e funções auxiliares para a leitura dos arquivos
MIDI.
"""

# Dependências
from pathlib import Path

# Constantes
ACCEPTED_EXTENSIONS = {".mid", ".midi"}
#########################################################################

def get_midi_paths(dir: str | Path) -> list[Path]:
    dir = Path(dir)
    midi_files = []

    if not dir.exists():
        raise FileNotFoundError(f"Este diretório não existe: {dir}")
    if not dir.is_dir():
        raise NotADirectoryError(f"Este não é um diretório: {dir}")

    for path in dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in ACCEPTED_EXTENSIONS:
            midi_files.append(path)

    midi_files.sort()

    if not midi_files:
        raise ValueError(f"Nenhum arquivo MIDI (.mid ou .midi) encontrado em: {dir}")

    return midi_files