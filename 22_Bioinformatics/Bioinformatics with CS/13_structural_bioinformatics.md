# 13. Structural Bioinformatics — Protein Structure

## Why this matters
A protein's 1D sequence folds into a specific 3D shape, and that shape determines its function — this is the sequence-structure-function paradigm. Structural bioinformatics is where biology meets computational geometry, graph theory, and (recently) deep learning (AlphaFold).

## Core concepts

- **PDB format**: text file listing every atom's 3D coordinates (`x, y, z`), organized by chain and residue. `Bio.PDB` parses this into a Structure → Model → Chain → Residue → Atom object hierarchy — a literal tree, good practice for hierarchical object traversal.
- **Secondary structure**: local folding patterns — alpha helices, beta sheets, loops — determined by backbone hydrogen bonding patterns (tools like DSSP compute this from 3D coordinates).
- **Contact maps**: an `N x N` binary/distance matrix where entry `(i,j)` shows whether residues `i` and `j` are spatially close (e.g., Cα-Cα distance < 8Å), even if far apart in sequence. This "flattens" 3D structure into a 2D matrix you can analyze with ordinary array/matrix tools — and it's exactly what modern structure-prediction deep learning models (AlphaFold's predecessors) predict from sequence alone.
- **RMSD (Root Mean Square Deviation)**: standard metric for how similar two structures are, after optimally superimposing them (Kabsch algorithm — an elegant application of SVD from linear algebra).

## Practice Project 13.1 — PDB structure analyzer

**Spec:**
1. Download a real PDB structure (e.g., lysozyme, PDB ID `1LYZ`, or myoglobin `1MBN`) using `Bio.PDB.PDBList`.
2. Parse it with `Bio.PDB.PDBParser`; write a function that reports: number of chains, number of residues per chain, and the full amino-acid sequence extracted directly from the 3D structure (compare this against the sequence you'd get from UniProt for the same protein — they should match).
3. Compute a **contact map**: for a chosen chain, compute Cα-Cα Euclidean distance between every pair of residues, threshold at 8Å, and visualize as a binary matrix image (matplotlib `imshow`). The diagonal band pattern you'll see corresponds to alpha helices; the off-diagonal parallel/antiparallel stripes correspond to beta sheets — identify a few by eye and note their approximate residue ranges.
4. Compute **secondary structure content** — if you have DSSP installed, run it via `Bio.PDB.DSSP`; otherwise, approximate helix regions using local Cα-Cα-Cα-Cα dihedral angle patterns.

## Practice Project 13.2 — Structural alignment (RMSD)

**Spec:**
1. Download two related structures (e.g., the same protein solved in two different PDB entries, or two homologous proteins from different species with solved structures).
2. Extract the shared Cα coordinates for aligned residues (use your Chapter 6 sequence alignment to figure out the residue correspondence first — this connects sequence and structure work directly).
3. Implement the **Kabsch algorithm** yourself: center both coordinate sets, compute the optimal rotation matrix via SVD of the covariance matrix, apply it, and compute RMSD of the superimposed structures.
4. Validate against `Bio.PDB.Superimposer`'s built-in RMSD calculation — confirm you get the same value.
5. Visualize before/after superposition if you have a 3D plotting tool available (matplotlib 3D scatter is enough for a rough check).

**Done when:** your contact map correctly reveals recognizable secondary-structure patterns, and your hand-implemented Kabsch/RMSD matches Biopython's built-in `Superimposer` output.

Next: `14_machine_learning_bioinformatics.md`.
