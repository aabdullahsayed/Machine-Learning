# 16. Biological Networks & Systems Biology

## Why this matters
Genes and proteins don't act alone — they form networks (protein-protein interactions, gene regulatory networks, metabolic pathways). Analyzing these is pure graph theory applied to biology: centrality, clustering, shortest paths, and community detection all have direct biological interpretations.

## Common network types

| Network | Nodes | Edges |
|---|---|---|
| Protein-protein interaction (PPI) | Proteins | Physical/functional interaction |
| Gene regulatory network (GRN) | Genes/TFs | "Regulates" (often directed) |
| Metabolic network | Metabolites/reactions | Chemical conversion |
| Co-expression network | Genes | Correlated expression across samples |

## Graph metrics with biological meaning

- **Degree centrality**: highly-connected "hub" proteins are often essential (knocking them out is more likely lethal) — a real, published finding (the "centrality-lethality rule").
- **Betweenness centrality**: nodes that bridge different network regions — often bottleneck/regulatory proteins.
- **Community detection** (e.g., Louvain modularity): clusters of densely-interconnected nodes often correspond to a shared biological pathway or protein complex — this is a real, standard way to discover pathway modules from interaction data alone.
- **Shortest path**: e.g., how many interaction steps separate two proteins — used to study signal propagation.

## Practice Project 16.1 — PPI network analyzer

**Spec:**
1. Download a real PPI network for an organism (e.g., yeast or human) from STRING-db or BioGRID (a simple edge-list format is fine).
2. Load it with `networkx`. Report basic stats: number of nodes/edges, degree distribution (plot it — real biological networks are typically scale-free, with a long tail of high-degree hubs; verify this empirically on your loaded network).
3. Compute degree and betweenness centrality; list the top-10 hub proteins.
4. Cross-reference your top hub list against a list of known essential genes for that organism (public essential-gene databases exist, e.g., DEG) — what fraction of your top hubs are essential? Compare that to the fraction among randomly-selected proteins of similar degree, to test the centrality-lethality hypothesis yourself rather than just citing it.
5. Run community detection (`networkx` or `python-louvain`) and pick 2-3 discovered communities; look up the proteins in each — do they correspond to a recognizable biological pathway or complex (check a couple of proteins per community on UniProt/STRING)?

## Practice Project 16.2 — Differential co-expression network

**Spec:**
1. Reuse your RNA-seq expression matrix from Chapter 11 (or a real public one).
2. Build a co-expression network: compute pairwise correlation (Pearson or Spearman) between all gene pairs (or a manageable top-variance subset, since full all-pairs on thousands of genes is large), and threshold at some correlation cutoff to create edges.
3. Compare the network structure between two conditions (e.g., build separate control-only and treatment-only co-expression networks) — which gene modules gain or lose connectivity between conditions? This "differential network" idea is a real technique for finding condition-specific regulatory rewiring.
4. Overlay your Chapter 11 differentially-expressed gene list onto the network — are DE genes concentrated in particular network modules, or scattered randomly? Test this quantitatively (e.g., permutation test: is the number of DE genes in the top module higher than expected by chance?).

**Done when:** you can explain the centrality-lethality rule and have empirically tested it (not just cited it) on real data, and you've identified at least one network module you can defend as biologically coherent using external database lookups.

Next: `17_statistics_for_bioinformatics.md`.
