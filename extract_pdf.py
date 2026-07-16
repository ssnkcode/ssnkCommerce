import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import fitz

pdf_path = r'C:\Users\ssnk\Desktop\img_lola\web\LISTA DE JUGUETES - CT.1500 0.pdf (2).pdf'
doc = fitz.open(pdf_path)
print(f'Total pages: {len(doc)}')
print()
for i, page in enumerate(doc):
    text = page.get_text()
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    joined = ' | '.join(lines)
    print(f'PAGE {i+1}: {joined}')
