import torch as th

def unfolding(n, A):
    """
    Unfold tensor A along the nth mode.
    Args:
        n (int): The mode along which to unfold.
        A (torch.Tensor): The tensor to be unfolded.
    
    Returns:
        torch.Tensor: Unfolded tensor of shape (shape[n], prod(shape) / shape[n])

    For example: 
    A with shape (a, b, c, d) and n = 0 -> unfolded_A with shape (a, b*c*d)
    A with shape (a, b, c, d) and n = 1 -> unfolded_A with shape (b, a*c*d)
    A with shape (a, b, c, d) and n = 2 -> unfolded_A with shape (c, a*b*d)
    A with shape (a, b, c, d) and n = 3 -> unfolded_A with shape (d, a*b*c)
    """
    shape = A.shape
    # Permute dimensions to bring nth dimension to the front
    sizelist = list(range(len(shape)))
    sizelist[n], sizelist[0] = 0, n
    # Reshape after permuting to get unfolded matrix
    return A.permute(sizelist).reshape(shape[n], -1)

def truncated_svd_var(X, var=0.9, return_rank=False, return_full_rank=False):
    """
    Perform SVD and truncate the singular values based on explained variance threshold.
    
    Args:
        X (torch.Tensor): 2D tensor to be decomposed.
        var (float): Explained variance threshold (default: 0.9).
    
    Returns:
        U (torch.Tensor): Left singular vectors.
        S (torch.Tensor): Singular values (truncated).
        Vt (torch.Tensor): Right singular vectors (truncated).
    """
    # Compute full SVD
    U, S, Vt = th.linalg.svd(X, full_matrices=False)
    # Compute explained variance
    total_variance = th.sum(S**2)
    explained_variance = th.cumsum(S**2, dim=0) / total_variance
    
    
    if return_rank:
        # Find the number of singular values needed to meet the variance threshold
        k = th.searchsorted(explained_variance, var).item() + 1
        return U[:, :k], S[:k], Vt[:k, :], k
    elif return_full_rank:
        return U, S, Vt, S**2/total_variance
    else:
        # Find the number of singular values needed to meet the variance threshold
        k = th.searchsorted(explained_variance, var).item() + 1
        return U[:, :k], S[:k], Vt[:k, :]
            

def svd_mode_n(n, A, var=0.9, return_full_rank=False, return_rank=False):
    """
    Perform SVD along the nth mode of tensor A.
    
    Args:
        n (int): Mode along which to perform SVD.
        A (torch.Tensor): The tensor to decompose.
        var (float): Explained variance threshold (default: 0.9).
    
    Returns:
        U (torch.Tensor), S (torch.Tensor), Vt (torch.Tensor): Truncated SVD components.
    """
    unfolded_A = unfolding(n, A)
    return truncated_svd_var(unfolded_A, var, return_full_rank=return_full_rank, return_rank=return_rank)


def hosvd_var(A, var=0.9, return_rank=False, return_full_rank=False):
    """
    Perform truncated Higher Order Singular Value Decomposition (HOSVD) on tensor A.
    
    Args:
        A (torch.Tensor): The tensor to be decomposed.
        var (float): Explained variance threshold (default: 0.9).
    
    Returns:
        S (torch.Tensor): Core tensor after HOSVD.
        u_list (list): List of factor matrices (U) for each mode.
    """
    S = A.clone()
    u_list = []
    # Loop over each mode of the tensor
    if not return_rank and not return_full_rank:
        for i in range(A.dim()):
            u, _, _ = svd_mode_n(i, A, var)
            # Perform tensor contraction along the ith mode
            S = th.tensordot(S, u, dims=([0], [0]))
            u_list.append(u)
        return S, u_list
    elif return_rank:
        rank_list = []
        for i in range(A.dim()):
            u, _, _, r = svd_mode_n(i, A, var, return_rank=True)
            S = th.tensordot(S, u, dims=([0], [0]))
            u_list.append(u)
            rank_list.append(r)
        return S, u_list, rank_list
    elif return_full_rank:
        ex_var_list = []
        for i in range(A.dim()):
            u, _, _, r = svd_mode_n(i, A, var, return_full_rank=True)
            S = th.tensordot(S, u, dims=([0], [0]))
            u_list.append(u)
            ex_var_list.append(r)
        return S, u_list, ex_var_list

def restore_hosvd(S, u_list):
    """
    Restore the original tensor from the core tensor and factor matrices.
    
    Args:
        S (torch.Tensor): Core tensor from HOSVD.
        u_list (list): List of factor matrices from HOSVD.
    
    Returns:
        torch.Tensor: The restored tensor.
    """
    restored_tensor = S.clone()
    # Perform tensor contraction to restore the original tensor
    for u in u_list:
        restored_tensor = th.tensordot(restored_tensor, u.t(), dims=([0], [0]))

    return restored_tensor