import click

encode_table = {
    '0': 'ATA', '1': 'TCT', '2': 'GCG', '3': 'GTG', '4': 'AGA',
    '5': 'CGC', '6': 'ATT', '7': 'ACC', '8': 'AGG', '9': 'CAA',
    'A': 'ACT', 'B': 'CAT', 'C': 'TCA', 'D': 'TAC', 'E': 'CTA',
    'F': 'GCT', 'G': 'GTC', 'H': 'CGT', 'I': 'CTG', 'J': 'TGC',
    'K': 'TCG', 'L': 'ATC', 'M': 'ACA', 'N': 'CTC', 'O': 'TGT',
    'P': 'GAG', 'Q': 'TAT', 'R': 'CAC', 'S': 'TGA', 'T': 'TAG',
    'U': 'GAT', 'V': 'GTA', 'W': 'TCC', 'X': 'AGT', 'Y': 'GAC',  # W를 TCC로 변경
    'Z': 'GCA', '.': 'ACG',
    'START': 'ATG', 'STOP': 'TAA'
}

decode_table = {v: k for k, v in encode_table.items()}

def encode(text):
    result = ['ATG']  # START 코드
    for ch in text.upper():
        if ch in encode_table and ch not in ('START', 'STOP'):
            result.append(encode_table[ch])
        # 지원하지 않는 문자는 무시
    result.append('TAA')  # STOP 코드
    return ''.join(result)

def decode(seq):
    seq = seq.upper()
    # START 코드 위치 찾기
    start = seq.find('ATG')
    if start == -1:
        return 'Invalid sequence: missing START codon.'
    
    # START 이후부터 3개씩 읽으면서 STOP 코돈 찾기
    coding_seq = seq[start+3:]
    result = []
    
    for i in range(0, len(coding_seq), 3):
        codon = coding_seq[i:i+3]
        if len(codon) < 3:
            break
        if codon == 'TAA':  # STOP 코돈 발견
            break
        char = decode_table.get(codon)
        if char and char not in ('START', 'STOP'):
            result.append(char)
    
    return ''.join(result)

@click.group()
def cli():
    """DNA Writer CLI"""
    pass

@cli.command(name="encode")
@click.argument('text')
def encode_text(text):
    """문자열을 DNA 코드로 인코딩합니다."""
    click.echo(encode(text))

@cli.command(name="decode")
@click.argument('dna')
def decode_dna(dna):
    """DNA 코드를 문자열로 디코딩합니다."""
    click.echo(decode(dna))

if __name__ == '__main__':
    cli()