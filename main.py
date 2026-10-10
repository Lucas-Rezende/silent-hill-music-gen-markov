#########################################################################
"""
main.py

Executa o pipeline de geração musical com cadeias de Markov.
"""

import argparse
from pathlib import Path

from markov_chain import train_markov_model
from midi_preprocessing import load_valid_midi_songs, convert_corpus_to_pianoroll
from music_gen import generate_song, write_midi
#########################################################################

def main():
    args = parse_arguments()

    midi_songs = load_valid_midi_songs(args.corpus)
    corpus = convert_corpus_to_pianoroll(midi_songs, args.resolution)
    probabilities = train_markov_model(corpus, args.order)

    corpus_name = args.corpus.name
    experiment = f"{corpus_name}_N{args.order:03d}_R{args.resolution}_S{args.seed}"
    output_dir = args.output / experiment
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(args.numsongs):
        seed = args.seed + i
        song = generate_song(probabilities, args.order, seed)

        filename = f"markov_{corpus_name}_N{args.order:03d}_R{args.resolution}_seed{seed}.mid"
        output_path = output_dir / filename

        write_midi(song, output_path, args.resolution)
        print(f"Gerada: {output_path} | seed={seed} | frames={len(song)}")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--resolution", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--numsongs", type=int, required=True)
    args = parser.parse_args()

    if args.order < 1:
        parser.error("--order deve ser maior ou igual a 1.")
    if args.resolution < 1:
        parser.error("--resolution deve ser maior ou igual a 1.")
    if args.numsongs < 1:
        parser.error("--numsongs deve ser maior ou igual a 1.")

    return args


if __name__ == "__main__":
    main()