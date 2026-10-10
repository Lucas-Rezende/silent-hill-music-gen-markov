#########################################################################
"""
midi_preprocessing.py

Dado o caminho para os arquivos MIDI, carrega-os e os converte em uma
representação piano roll, i.e., uma lista de tuplas contendo as notas
ativas em cada instante de tempo.
"""

# Dependências
from pathlib import Path
import muspy
import numpy as np
from utils import get_midi_paths
#########################################################################

def load_valid_midi_songs(directory: str | Path) -> list[muspy.Music]:
    """Carrega os arquivos MIDI e retorna apenas os válidos."""
    songs = []

    for path in get_midi_paths(directory):
        try:
            songs.append(muspy.read_midi(path))
        except Exception as error:
            print(f"Este arquivo MIDI não é válido: {path.name}: {error}")

    if not songs:
        raise ValueError("Nenhum arquivo MIDI válido foi encontrado.")

    return songs


def clean_song(song: muspy.Music, resolution: int) -> muspy.Music:
    """Remove drums e normaliza a resolução temporal."""
    song.tracks = [track for track in song.tracks if not track.is_drum]
    song.adjust_resolution(target=resolution)

    return song


def convert_to_pianoroll(song: muspy.Music, resolution: int) -> list[tuple[int, ...]]:
    """Converte uma música em uma sequência de notas ativas."""
    song = clean_song(song, resolution)
    roll = song.to_pianoroll_representation(encode_velocity=False)
    active_frames = np.flatnonzero(roll.any(axis=1))

    if not len(active_frames):
        raise ValueError("Música sem notas após o pré-processamento.")

    roll = roll[active_frames[0] : active_frames[-1] + 1]

    return [tuple(np.flatnonzero(frame)) for frame in roll]


def convert_corpus_to_pianoroll(corpus: list[muspy.Music], resolution: int) -> list[list[tuple[int, ...]]]:
    """Converte todo o corpus para piano roll, ignorando músicas sem notas válidas."""
    pianorolls = []

    for i, song in enumerate(corpus):
        try:
            pianorolls.append(convert_to_pianoroll(song, resolution))
        except ValueError as error:
            print(f"Música {i + 1} ignorada: {error}")

    if not pianorolls:
        raise ValueError("Nenhuma música válida após o pré-processamento.")

    return pianorolls