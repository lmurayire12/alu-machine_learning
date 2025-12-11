#!/usr/bin/env python3
"""
Function to perform Principal Component Analysis (PCA) on a dataset.
"""
import numpy as np


def pca(X, var=0.95):
    """
    Performs PCA on a dataset.

    Args:
        X (np.ndarray): The dataset of shape (n, d) where n is the number
                        of data points and d is the number of dimensions.
                        All dimensions must have a mean of 0.
        var (float): The fraction of the variance that the PCA transformation
                     should maintain (0 < var <= 1).

    Returns:
        np.ndarray: The weights matrix, W, of shape (d, nd) where nd is
                    the new dimensionality of the transformed X, such that
                    'var' fraction of X's original variance is maintained.
    """
    if not isinstance(X, np.ndarray) or len(X.shape) != 2:
        raise TypeError("X must be a 2D numpy.ndarray")
    if not isinstance(var, (int, float)) or not (0 < var <= 1):
        raise ValueError("var must be a float between 0 and 1 (exclusive of 0)")

    # 1. Calculate the Covariance Matrix
    # Since X already has a mean of 0 for all dimensions, the covariance matrix
    # C is calculated as: C = (1/n) * X^T @ X
    # numpy's np.cov(X.T) handles the (1/(n-1)) scaling, but for consistency
    # and minimizing operations, we'll use the definition related to the
    # correlation matrix since the data is centered.
    # The convention is often to use the unbiased estimate (1/(n-1)),
    # which is what np.cov(X.T) does (rowvar=False is the default).
    # Since the prompt asks for "minimum number of operations to avoid floating
    # point errors," we'll use the reliable np.linalg.svd which is often
    # numerically superior to EIG (as suggested by the image performance note).
    # We will use the relation: Cov(X) = V @ S^2 @ V^T
    # However, standard PCA procedure uses the covariance matrix of the data,
    # which is derived from X.T @ X or X @ X.T.

    # Let's use SVD on X: X = U @ Sigma @ Vh
    # The squared singular values (Sigma^2) from SVD of X are proportional to
    # the eigenvalues of the covariance matrix C = (1/(n-1)) * X.T @ X.
    # The columns of Vh.T (which are the rows of Vh) are the principal components.
    
    # U, S, Vh = np.linalg.svd(X)
    # The eigenvectors of X.T @ X are the columns of V = Vh.T
    # The eigenvalues are S**2 / (n - 1)
    
    # 1. Calculate Covariance Matrix C
    # C = np.cov(X.T) # X.T because rowvar=True by default, we want columns as variables
    
    # 2. Get Eigenvectors (W_all) and Eigenvalues (Eigs) from the Covariance Matrix
    # Using np.linalg.eig for the covariance matrix:
    C = np.cov(X.T)
    # Eigs are the eigenvalues, W_all are the eigenvectors (principal components)
    Eigs, W_all = np.linalg.eig(C)
    
    # Ensure eigenvalues and eigenvectors are correctly matched (they should be)
    # The EIG function does not necessarily return sorted values.
    
    # 3. Sort Eigenvectors by descending Eigenvalues
    # Get the indices that would sort Eigs in descending order
    idx = np.argsort(Eigs)[::-1]
    
    # Sort eigenvalues and eigenvectors
    sorted_eigs = Eigs[idx]
    sorted_W = W_all[:, idx]  # Apply the sorting indices to the columns of W_all

    # 4. Calculate Cumulative Explained Variance
    # Total variance is the sum of all eigenvalues
    total_variance = np.sum(sorted_eigs)
    
    # Cumulative sum of sorted eigenvalues
    cumulative_variance = np.cumsum(sorted_eigs)
    
    # Calculate cumulative explained variance fraction
    explained_variance_ratio = cumulative_variance / total_variance

    # 5. Determine the New Dimensionality (nd)
    # Find the smallest number of components (nd) that maintains 'var' fraction
    # np.argmax returns the index of the first True value. We need the index + 1
    # because nd is the count of components.
    nd = np.argmax(explained_variance_ratio >= var) + 1

    # 6. Select the Weights Matrix W
    # W is the matrix containing the first 'nd' principal components (eigenvectors)
    # W should be of shape (d, nd)
    W = sorted_W[:, :nd]

    return W

if __name__ == '__main__':
    # Example usage with test data (assuming files are in the same directory)
    try:
        X = np.loadtxt("mnist2500_X.txt")
        # labels = np.loadtxt("mnist2500_labels.txt") # labels not needed for PCA
    except FileNotFoundError:
        print("Please ensure 'mnist2500_X.txt' is available for testing.")
        # Create a dummy dataset for demonstration if file not found
        print("Using dummy data for demonstration.")
        np.random.seed(42)
        X = np.random.rand(100, 10)
        # Manually center the dummy data (the prompt says input X is already centered)
        X = X - np.mean(X, axis=0)

    print(f"Original shape of X: {X.shape}")

    # Test with default variance (95%)
    W_95 = pca(X, var=0.95)
    print(f"Weights matrix W (var=0.95) shape: {W_95.shape}")

    # Test with a higher variance (99%)
    W_99 = pca(X, var=0.99)
    print(f"Weights matrix W (var=0.99) shape: {W_99.shape}")

    # Test with a lower variance (80%)
    W_80 = pca(X, var=0.80)
    print(f"Weights matrix W (var=0.80) shape: {W_80.shape}")

    # Verify that nd increases as var increases
    d_95 = W_95.shape[1]
    d_99 = W_99.shape[1]
    d_80 = W_80.shape[1]

    print(f"\nNew dimensionality for 95% variance: {d_95}")
    print(f"New dimensionality for 99% variance: {d_99}")
    print(f"New dimensionality for 80% variance: {d_80}")

    # Expected relationship: d_80 <= d_95 <= d_99
    print(f"Check: Is {d_80} <= {d_95} <= {d_99}? {'Yes' if d_80 <= d_95 <= d_99 else 'No'}")
