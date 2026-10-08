import muspy
import numpy as np

RESOLUTION = 4
ACCEPTED_EXTENSIONS = {".mid", ".midi"}

def load_corpus(directory):
    paths = sorted(
        path
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in ACCEPTED_EXTENSIONS
    )

    if not paths:
        raise ValueError("Nenhum arquivo MIDI encontrado no corpus.")

    songs = []

    for path in paths:
        try:
            songs.append(read_midi(path))
            print(f"Adicionada: {path.name}")
        except Exception as error:
            print(f"Erro em {path.name}: {error}")

    if not songs:
        raise ValueError("Nenhuma música MIDI válida no corpus.")

    return songs

def read_midi(path):
    music = muspy.read_midi(path)
    music.tracks = [track for track in music.tracks if not track.is_drum]
    music.adjust_resolution(target=RESOLUTION)
    roll = music.to_pianoroll_representation(encode_velocity=False)
    active = np.flatnonzero(roll.any(axis=1))

    if not len(active):
        raise ValueError("Música sem notas.")

    roll = roll[active[0] : active[-1] + 1]

    return [tuple(np.flatnonzero(row)) for row in roll]

def write_midi(song, path):
    roll = np.zeros((len(song), 128), dtype=bool)

    for time, pitches in enumerate(song):
        roll[time, list(pitches)] = True

    music = muspy.from_pianoroll_representation(roll, resolution=RESOLUTION, encode_velocity=False,)

    muspy.write_midi(path, music)
