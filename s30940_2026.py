import random


def generate_sequence(length: int) -> str:
    """Returns a random DNA sequence of the specified length."""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choices(nucleotides, k=length))


def calculate_stats(sequence: str) -> dict:
    """Returns a dictionary of sequence statistics."""
    length = len(sequence)
    counts = {nuc: sequence.count(nuc) for nuc in ['A', 'C', 'G', 'T']}
    stats = {nuc: round(counts[nuc] / length * 100, 2) for nuc in ['A', 'C', 'G', 'T']}
    gc = round((counts['G'] + counts['C']) / length * 100, 2)
    stats['GC'] = gc
    stats['gc_ratio_A'] = gc
    return stats


if __name__ == "__main__":
    pass
