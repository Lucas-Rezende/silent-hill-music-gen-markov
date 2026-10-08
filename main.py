import argparse
from pathlib import Path
from markov_chain import train_markov_model, generate_new_song
from midi_utils import load_corpus, write_midi

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("corpus", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--numsongs", type=int, required=True)

    args = parser.parse_args()

    if args.order < 1:
        parser.error("--order deve ser maior ou igual a 1.")
    if args.numsongs < 1:
        parser.error("--numsongs deve ser maior ou igual a 1.")

    return args

def generate_songs(probs, output, order, seed, numsongs):
    output.mkdir(parents=True, exist_ok=True)

    for i in range(numsongs):
        song = generate_new_song(probs, order, seed + i)
        path = output / f"markov_song_{i + 1:02d}.mid"

        write_midi(song, path)
        print(f"Gerada: {path}")

def main():
    args = parse_arguments()

    songs = load_corpus(args.corpus)
    probabilities = train_markov_model(songs, args.order)

    generate_songs(probabilities, args.output, args.order, args.seed, args.numsongs)

if __name__ == "__main__":
    main()
