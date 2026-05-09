
# Album number: s30940
# Date: 2026-05-06
# Description: DNA sequence generator and analysis tool for Bioinformatics.
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
    # Generate the DNA sequence
    sequence = generate_sequence(length)

    # Embed user's name at a random position (lowercase, not counted in stats)
    sequence_with_name = insert_name(sequence, name)

    # Format as FASTA and save to file
    fasta_content = format_fasta(seq_id, description, sequence_with_name)
    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(fasta_content)
    print(f"\nSequence saved to file: {filename}")

    # Calculate and print statistics (on clean sequence, without embedded name)
    stats = calculate_stats(sequence)
    print(f"\nSequence statistics (n={length}):")
    for nuc in ['A', 'C', 'G', 'T']:
        print(f"  {nuc}: {stats[nuc]:.2f}%")
    print(f"  GC-content: {stats['GC']:.2f}%")

    # --- Feature 3: Motif search ---
    if input("\nSearch for a motif? (y/n): ").strip().lower() == 'y':
        motif = input("Enter motif (e.g. ATG): ").strip().upper()
        positions = []
        start = 0
        while True:
            pos = sequence.find(motif, start)
            if pos == -1:
                break
            positions.append(pos + 1)  # 1-based biological convention
            start = pos + 1
        if positions:
            print(f"Motif '{motif}' found at positions: {positions}")
        else:
            print(f"Motif '{motif}' not found.")

    # --- Feature 4: Complementary & reverse complementary ---
    COMPLEMENT_MAP = str.maketrans('ACGTacgt', 'TGCAtgca')

    if input("\nGenerate complementary sequences? (y/n): ").strip().lower() == 'y':
        comp = sequence.translate(COMPLEMENT_MAP)
        rev_comp = comp[::-1]
        comp_filename = f"{seq_id}_complement.fasta"
        with open(comp_filename, 'w') as f:
            f.write(format_fasta(f"{seq_id}_COMP", "Complementary strand", comp))
            f.write("\n")
            f.write(format_fasta(f"{seq_id}_REVCOMP", "Reverse complementary strand", rev_comp))
        print(f"Complementary sequences saved to: {comp_filename}")
     # --- Feature 5: In silico transcription (DNA -> mRNA) ---
    if input("\nGenerate mRNA (transcription)? (y/n): ").strip().lower() == 'y':
        mrna = sequence.replace('T', 'U')
        mrna_filename = f"{seq_id}_mRNA.fasta"
        with open(mrna_filename, 'w') as f:
            f.write(format_fasta(f"{seq_id}_mRNA", "In silico transcription", mrna))
        print(f"mRNA saved to: {mrna_filename}")

    # --- Feature 6: Translation (DNA -> protein) ---
    CODON_TABLE = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
        'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    }

    if input("\nTranslate to protein? (y/n): ").strip().lower() == 'y':
        protein = []
        for i in range(0, len(sequence) - 2, 3):
            codon = sequence[i:i + 3]
            aa = CODON_TABLE.get(codon, '?')
            if aa == '*':
                protein.append('*')
                break
            protein.append(aa)
        print(f"Protein sequence: {''.join(protein)}")

    # --- Feature 9: ORF detection ---
    STOP_CODONS = {'TAA', 'TAG', 'TGA'}

    if input("\nSearch for ORFs? (y/n): ").strip().lower() == 'y':
        min_orf = validate_positive_int("Minimum ORF length (nt): ", min_val=3, max_val=length)
        orfs = []
        for i in range(len(sequence) - 2):
            if sequence[i:i + 3] == 'ATG':
                for j in range(i + 3, len(sequence) - 2, 3):
                    codon = sequence[j:j + 3]
                    if codon in STOP_CODONS:
                        orf_seq = sequence[i:j + 3]
                        if len(orf_seq) >= min_orf:
                            orfs.append({'start': i + 1, 'end': j + 3, 'length': len(orf_seq)})
                        break
        if orfs:
            print(f"Found {len(orfs)} ORF(s):")
            for orf in orfs:
                print(f"  Start: {orf['start']}, End: {orf['end']}, Length: {orf['length']} nt")
        else:
            print("No ORFs found.")
    # --- Feature 7 & 8: Sliding window GC analysis + HTML chart ---
    if input("\nRun sliding window GC analysis? (y/n): ").strip().lower() == 'y':
        import csv
        window = validate_positive_int("Window size (nt): ", min_val=1, max_val=length)
        step = validate_positive_int("Step size (nt): ", min_val=1, max_val=window)

        # Calculate GC per window
        sw_results = []
        for i in range(0, len(sequence) - window + 1, step):
            w_seq = sequence[i:i + window]
            gc = (w_seq.count('G') + w_seq.count('C')) / window * 100
            sw_results.append({'start_position': i + 1, 'gc_content': round(gc, 2)})

        # Save CSV
        csv_filename = f"{seq_id}_gc_sliding.csv"
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['start_position', 'gc_content'])
            writer.writeheader()
            writer.writerows(sw_results)
        print(f"Sliding window data saved to: {csv_filename}")

        # Save HTML chart (Feature 8) — no external libraries needed
        positions = [r['start_position'] for r in sw_results]
        gc_values = [r['gc_content'] for r in sw_results]
        max_pos = max(positions) if positions else 1
        W, H, PAD = 800, 300, 50

        def sx(p): return PAD + (p / max_pos) * (W - 2 * PAD)
        def sy(v): return H - PAD - (v / 100) * (H - 2 * PAD)

        path_d = "M " + " L ".join(f"{sx(positions[i]):.1f},{sy(gc_values[i]):.1f}"
                                    for i in range(len(positions)))
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>GC Content</title></head><body>
<h2>GC Content — Sliding Window</h2>
<svg width="{W}" height="{H}" style="border:1px solid #ccc">
  <text x="5" y="{sy(100):.0f}" font-size="10">100%</text>
  <text x="5" y="{sy(50):.0f}" font-size="10">50%</text>
  <text x="5" y="{sy(0):.0f}" font-size="10">0%</text>
  <line x1="{PAD}" y1="{sy(50):.0f}" x2="{W-PAD}" y2="{sy(50):.0f}" stroke="#eee"/>
  <path d="{path_d}" fill="none" stroke="#2196F3" stroke-width="1.5"/>
  <line x1="{PAD}" y1="{PAD}" x2="{PAD}" y2="{H-PAD}" stroke="#333"/>
  <line x1="{PAD}" y1="{H-PAD}" x2="{W-PAD}" y2="{H-PAD}" stroke="#333"/>
</svg></body></html>"""

        chart_filename = f"{seq_id}_gc_chart.html"
        with open(chart_filename, 'w') as f:
            f.write(html)
        print(f"GC chart saved to: {chart_filename}")

    print("\nDone!")


if __name__ == "__main__":
    main()
