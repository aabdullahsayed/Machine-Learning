# 05 — Phylogenetics

Phylogenetics reconstructs evolutionary relationships between sequences/species as trees — used for tracking viral outbreaks, studying species evolution, and understanding gene families.

## Pipeline overview

```
sequences (FASTA) → multiple sequence alignment → distance/model calculation → tree building → visualization
```

## Step 1: Multiple sequence alignment (prerequisite)

```bash
mafft --auto sequences.fasta > aligned.fasta
```

## Step 2: Build a distance matrix

```python
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator

alignment = AlignIO.read("aligned.fasta", "fasta")
calculator = DistanceCalculator("identity")   # or 'blastn', 'trans' etc.
dm = calculator.get_distance(alignment)
print(dm)
```

## Step 3: Build a tree (Neighbor-Joining or UPGMA)

```python
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor

constructor = DistanceTreeConstructor()
nj_tree = constructor.nj(dm)          # Neighbor-Joining
# upgma_tree = constructor.upgma(dm)  # alternative method

from Bio import Phylo
Phylo.write(nj_tree, "tree.nwk", "newick")
```

## Step 4: Visualize

```python
from Bio import Phylo
import matplotlib.pyplot as plt

tree = Phylo.read("tree.nwk", "newick")
tree.ladderize()  # sorts branches for cleaner display

fig, ax = plt.subplots(figsize=(8, 6))
Phylo.draw(tree, axes=ax, do_show=False)
plt.savefig("phylo_tree.png", dpi=150)
```

## Maximum likelihood trees (more rigorous, for real analyses)

```bash
# IQ-TREE — finds best-fit substitution model and builds ML tree with bootstrap support
iqtree2 -s aligned.fasta -m MFP -bb 1000 -nt 4
```

```python
from Bio import Phylo

tree = Phylo.read("aligned.fasta.treefile", "newick")
Phylo.draw_ascii(tree)   # quick terminal visualization
```

## Use case: tracking pathogen evolution (e.g. viral outbreak lineage)

```python
from Bio import SeqIO, AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import subprocess

# 1. Collect samples from different outbreak locations/times
records = list(SeqIO.parse("outbreak_samples.fasta", "fasta"))
print(f"{len(records)} viral genomes collected")

# 2. Align
subprocess.run(["mafft", "--auto", "outbreak_samples.fasta"],
                stdout=open("outbreak_aligned.fasta", "w"))

# 3. Build tree
alignment = AlignIO.read("outbreak_aligned.fasta", "fasta")
dm = DistanceCalculator("identity").get_distance(alignment)
tree = DistanceTreeConstructor().nj(dm)

# 4. Inspect clades — samples that cluster together may share a transmission source
for clade in tree.get_nonterminals():
    tip_names = [t.name for t in clade.get_terminals()]
    if len(tip_names) >= 2:
        print("Cluster:", tip_names)
```

This is the same conceptual approach used by Nextstrain for real-time pathogen surveillance (e.g. SARS-CoV-2, influenza).

## Use case: comparing tree topologies

```python
from Bio import Phylo

tree1 = Phylo.read("tree_geneA.nwk", "newick")
tree2 = Phylo.read("tree_geneB.nwk", "newick")

terms1 = set(t.name for t in tree1.get_terminals())
terms2 = set(t.name for t in tree2.get_terminals())
print("Shared taxa:", terms1 & terms2)
```

Full topology comparison (Robinson-Foulds distance) is available via `ete3` or `dendropy` for rigorous congruence testing between gene trees and species trees.

## Exercise

1. Build a Neighbor-Joining tree from 10 homologous gene sequences across species and visualize it.
2. Compare NJ vs. UPGMA trees on the same data — do they agree on major clades?
3. Run IQ-TREE on the same alignment and compare bootstrap support values to the distance-based tree's structure.

**You've completed the Advanced track.** Continue to `04-projects/project-ideas.md` to apply everything.
