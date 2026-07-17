# Practice — Statistics

1. Compute mean, median, and standard deviation by hand for the dataset `[2, 4, 4, 4, 5, 5, 7, 9]`. Verify with `numpy`.
2. Z-score normalize a small dataset by hand, then verify with `(X - X.mean()) / X.std()`.
3. Run a paired t-test (using `scipy.stats.ttest_rel`) comparing two lists of model accuracy scores across cross-validation folds — interpret the resulting p-value.
4. Derive (on paper) the MLE estimate for the mean of a Gaussian distribution, following the steps in `MLE.md`, and confirm it's the sample mean.
5. Train two models on the same small dataset — one deliberately too simple (underfitting) and one deliberately too complex/overfit — and plot both training and validation loss to visualize the bias-variance tradeoff directly.
6. Explain in your own words: why does adding L2 regularization typically increase training error slightly but can decrease validation/test error?

✅ Done? Move to `05-Optimization`.
