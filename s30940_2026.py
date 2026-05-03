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

def validate_id(prompt: str) -> str:
    """Gets a sequence ID from the user.
    Repeats the prompt if the ID contains whitespace or is empty."""
    while True:
        seq_id = input(prompt).strip()
        if not seq_id:
            print("Error: ID cannot be empty.")
        elif any(c.isspace() for c in seq_id):
            print("Error: ID cannot contain whitespace.")
        else:
            return seq_id


def main():
    """Main program flow."""
    print("=" * 50)
    print("  DNA Sequence Generator — FASTA format")
    print("=" * 50)

    # Get sequence length from user (with validation)
    length = validate_positive_int("Enter sequence length: ")

    # Get sequence ID (no whitespace allowed)
    seq_id = validate_id("Enter sequence ID: ")

    # Description is optional
    description = input("Enter a description of the sequence (optional): ").strip()

    # Name to embed inside the sequence
    name = input("Enter your name: ").strip()
