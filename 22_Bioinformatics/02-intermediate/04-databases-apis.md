# 04 — Biological Databases & APIs

Real bioinformatics work constantly pulls from public databases. Know how to query them programmatically instead of manually clicking through websites.

## NCBI Entrez (genes, sequences, literature)

```python
from Bio import Entrez, SeqIO

Entrez.email = "you@example.com"

# Search PubMed
handle = Entrez.esearch(db="pubmed", term="CRISPR gene editing", retmax=5)
record = Entrez.read(handle)
print(record["IdList"])

# Fetch a gene record
handle = Entrez.efetch(db="gene", id="7157", rettype="gene_table", retmode="text")  # TP53
print(handle.read()[:500])
```

## Ensembl REST API

```python
import requests

server = "https://rest.ensembl.org"
gene_symbol = "BRCA1"

r = requests.get(
    f"{server}/lookup/symbol/homo_sapiens/{gene_symbol}",
    headers={"Content-Type": "application/json"}
)
data = r.json()
print(data["id"], data["start"], data["end"], data["seq_region_name"])
```

## Use case: fetch a gene's sequence + orthologs

```python
import requests

server = "https://rest.ensembl.org"
gene_id = "ENSG00000012048"  # BRCA1

# Get orthologs
r = requests.get(
    f"{server}/homology/id/{gene_id}?type=orthologues",
    headers={"Content-Type": "application/json"}
)
homologies = r.json()["data"][0]["homologies"]
for h in homologies[:5]:
    print(h["target"]["species"], h["target"]["id"])
```

## UniProt (protein data)

```python
import requests

r = requests.get("https://rest.uniprot.org/uniprotkb/P04637.fasta")  # TP53 protein
print(r.text)

r = requests.get("https://rest.uniprot.org/uniprotkb/P04637.json")
data = r.json()
print(data["proteinDescription"]["recommendedName"]["fullName"]["value"])
```

## KEGG (pathways)

```python
import requests

r = requests.get("https://rest.kegg.jp/get/hsa:7157")  # TP53 human gene
print(r.text[:500])

r = requests.get("https://rest.kegg.jp/link/pathway/hsa:7157")
print(r.text)  # pathways this gene is involved in
```

## Use case: build a local mini gene database from queries

```python
import requests
import pandas as pd

genes = ["TP53", "BRCA1", "BRCA2", "EGFR", "KRAS"]
records = []

for symbol in genes:
    r = requests.get(
        f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}",
        headers={"Content-Type": "application/json"}
    )
    d = r.json()
    records.append({
        "symbol": symbol,
        "ensembl_id": d.get("id"),
        "chromosome": d.get("seq_region_name"),
        "start": d.get("start"),
        "end": d.get("end"),
        "biotype": d.get("biotype"),
    })

df = pd.DataFrame(records)
df.to_csv("gene_summary.csv", index=False)
print(df)
```

## Rate limiting & good API citizenship

```python
import time
import requests

def safe_get(url, headers=None, delay=0.5):
    time.sleep(delay)  # avoid hammering public APIs
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp
```

Always set `Entrez.email`, respect rate limits, and cache results locally (`.csv`/`.json`) so you don't re-query unnecessarily.

## Exercise

1. Given a list of 10 gene symbols, fetch each one's chromosome location from Ensembl and save to a CSV.
2. Query UniProt for a protein's sequence and compute its length and amino acid composition.
3. Use KEGG to find which pathways a gene of interest participates in, and print them as a clean list.

**You've completed the Intermediate track.** Continue to `03-advanced/01-genome-assembly.md`.
