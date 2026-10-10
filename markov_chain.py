#########################################################################
"""
markov_chain.py

Implementação de uma Cadeia de Markov de ordem N.
"""

# Dependências
from collections import Counter, defaultdict

# Constantes
START = "<SOS>"
END = "<EOS>"
#########################################################################

def train_markov_model(songs, order):
    """Treina o modelo de Markov a partir do corpus, retornando
    as probabilidades de transição para cada contexto."""
    song_sequences = add_start_end_symbols(songs, order)
    transitions = count_transitions(song_sequences, order)
    markov_probabilities = calculate_transition_probabilities(transitions)

    return markov_probabilities


def add_start_end_symbols(songs, order):
    """Adiciona os símbolos de início e fim a cada música do corpus."""
    song_sequences = []

    for song in songs:
        sequence = [START] * order + song + [END]
        song_sequences.append(sequence)

    return song_sequences


def count_transitions(song_sequences, order):
    """Conta quantas vezes cada símbolo aparece após cada contexto
    de tamanho `order`."""
    transitions = defaultdict(Counter)

    for sequence in song_sequences:
        for i in range(order, len(sequence)):
            context = tuple(sequence[i - order:i])
            next_symbol = sequence[i]
            transitions[context][next_symbol] += 1

    return transitions


def calculate_transition_probabilities(transitions):
    """Calcula P(próximo símbolo | contexto)."""
    probabilities = {}

    for context, next_symbols in transitions.items():
        total = sum(next_symbols.values())
        probabilities[context] = {
            symbol: count / total for symbol, count in next_symbols.items()
        }

    return probabilities