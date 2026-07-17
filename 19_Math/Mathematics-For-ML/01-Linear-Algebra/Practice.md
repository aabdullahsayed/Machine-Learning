# Practice — Linear Algebra

1. By hand, compute the dot product of `[1, 2, 3]` and `[4, 5, 6]`. Then verify with `np.dot`.
2. Implement cosine similarity from scratch (no `sklearn`) and test it on two random vectors.
3. Multiply two 3×3 matrices by hand, then verify with `A @ B` in NumPy.
4. Compute the eigenvalues/eigenvectors of `[[2,0],[0,3]]` by hand, then verify with `np.linalg.eig`.
5. Load any small dataset (e.g., `sklearn.datasets.load_iris`), compute its covariance matrix, and find the top 2 principal components via `np.linalg.eig` — compare against `sklearn.decomposition.PCA`.
6. Implement L1 and L2 regularization penalties from scratch and add them to a simple linear regression loss function. Train with each and compare how many weights become exactly zero with L1 vs L2.
7. Explain in your own words: why does GPU hardware matter so much for deep learning, in terms of the matrix operations involved?

✅ Done? Move to `02-Calculus`.
