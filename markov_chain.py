import random
from collections import Counter, defaultdict

START = "__START__"
END = "__END__"
MAX_EVENTS = 100_000

def build_counts(songs, order):
    """Conta quantas vezes cada transição acontece."""
    counts = defaultdict(Counter)

    for song in songs:
        sequence = [START] * order + song + [END]

        for i in range(order, len(sequence)):
            state = tuple(sequence[i - order : i])
            next_symbol = sequence[i]

            counts[state][next_symbol] += 1

    return counts

def calculate_probabilities(counts):
    """Calcula as probabilidades de transição."""
    probabilities = {}

    for state, transitions in counts.items():
        total = sum(transitions.values())

        probabilities[state] = {
            symbol: count / total for symbol, count in transitions.items()
        }

    return probabilities

def train_markov_model(songs, order):
    counts = build_counts(songs, order)
    return calculate_probabilities(counts)

def sample_next(options, rng):
    """Sorteia a próxima transição."""
    return rng.choices(
        list(options),
        weights=options.values(),
    )[0]

def generate_new_song(probs, order, seed):
    """Gera uma nova sequência usando a Cadeia de Markov."""
    rng = random.Random(seed)
    state = (START,) * order
    song = []

    for _ in range(MAX_EVENTS):
        next_symbol = sample_next(probs[state], rng)

        if next_symbol == END:
            return song

        song.append(next_symbol)
        state = state[1:] + (next_symbol,)

    return song