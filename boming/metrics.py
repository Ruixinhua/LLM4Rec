import numpy as np

def calculate_metrics(true_pos, rank_hat):
    """
    true_pos: pos item ['C1', 'C3', 'C5']
    rank_hat: ranking list ['C2', 'C5', 'C1', 'C3', 'C4'] 
    return: auc, mrr, ndcg5, ndcg10
    """

    # Get the ranks of the true positives in rank_hat
    ranks = [rank_hat.index(item) + 1 if item in rank_hat else len(rank_hat) + 1 for item in true_pos]
    
    # AUC calculation
    num_negatives = len(rank_hat) - len(true_pos)
    num_better_ranks = sum([r for r in ranks if r <= len(rank_hat)])
    auc = (num_better_ranks - len(true_pos) * (len(true_pos) + 1) / 2) / (len(true_pos) * num_negatives)
    
    # MRR calculation
    mrr = 0
    for rank in ranks:
        if rank <= len(rank_hat):
            mrr += 1.0 / rank
    mrr /= len(true_pos)
    
    # DCG and NDCG calculation
    def dcg_at_k(r, k):
        r = np.asarray(r)[:k]
        return np.sum(r / np.log2(np.arange(2, r.size + 2)))
    
    def ndcg_at_k(r, k, method=0):
        dcg_max = dcg_at_k(sorted(r, reverse=True), k)
        if not dcg_max:
            return 0.
        return dcg_at_k(r, k) / dcg_max

    binary_relevance = [1 if i in true_pos else 0 for i in rank_hat]
    ndcg5 = ndcg_at_k(binary_relevance, 5)
    ndcg10 = ndcg_at_k(binary_relevance, 10)

    return auc, mrr, ndcg5, ndcg10
