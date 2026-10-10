#########################################################################
"""
music_gen.py

Gera novas músicas a partir das probabilidades calculadas
pelo modelo de Markov.
"""

# Dependências
import random
from markov_chain import START, END
from pathlib import Path
import muspy

# Constantes
MAX_EVENTS = 50_000
#########################################################################

def generate_song(probs, order, seed):
    """
    Gera uma nova sequência usando o modelo treinado.
    """
    random_generator = random.Random(seed)
    context = (START,) * order
    song = []

    for _ in range(MAX_EVENTS):
        next_symbol = sample_next_symbol(probs, context, random_generator)

        if next_symbol == END:
            break

        song.append(next_symbol)
        context = context[1:] + (next_symbol,)

    return song


def sample_next_symbol(probs, context, random_generator):
    """
    Sorteia o próximo estado usando P(estado | contexto).
    """
    options = probs[context]
    return random_generator.choices(population=list(options), weights=options.values(), k=1)[0]

def write_midi(song, path: str | Path, resolution: int):
    """Converte a sequência gerada em um arquivo MIDI."""
    notes = []
    active_notes = {}

    for time, frame in enumerate(song):
        current_notes = set(frame)

        for pitch in current_notes:
            if pitch not in active_notes:
                active_notes[pitch] = time

        for pitch in list(active_notes):
            if pitch not in current_notes:
                start = active_notes.pop(pitch)
                notes.append(muspy.Note(time=start, pitch=pitch, duration=time - start, velocity=64))

    for pitch, start in active_notes.items():
        notes.append(muspy.Note(time=start, pitch=pitch, duration=len(song) - start, velocity=64))

    music = muspy.Music(resolution=resolution)
    music.tracks.append(muspy.Track(program=0, is_drum=False, notes=notes))

    muspy.write_midi(path, music)