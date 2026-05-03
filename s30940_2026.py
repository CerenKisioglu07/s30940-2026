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
    
def insert_name(sequence: str, name: str) -> str:
    """Inserts a name at a random position in the sequence.
    Name written in lowercase letters."""
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name.lower() + sequence[pos:]


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Returns a formatted FASTA record as a string."""
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"

    lines = [header]
    for i in range(0, len(sequence), line_width):
        lines.append(sequence[i:i + line_width])

    lines.append("# EOF_1")
    return '\n'.join(lines) + '\n'


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Gets an integer from the user in a range.
    In case of an error, repeats the question."""
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
        except ValueError:
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
