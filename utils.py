import numpy as np

from sound import *


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def match_kernels(dic1, dic2, max_match=3):
    # Do it quickly: find best match and iterate
    n1, n2 = len(dic1), len(dic2)
    n_matches = min(min(n1, n2), max_match)
    n_found = 0
    matches = []
    seen = []
    tot_score = 0
    for id1 in dic1.keys():
        if n_found >= n_matches:
            pass
        best_score = np.inf
        current_match = -1
        k1 = dic1[id1]
        for id2 in dic2.keys():
            if id2 in seen:
                continue
            k2 = dic2[id2]
            diff = Sound(k1._samples)
            diff.add_extend(k2, -1, 0)
            score = diff.norm()
            if score < best_score:
                current_match = id2
                best_score = score
        matches.append((id1, current_match))
        seen.append(current_match)
        tot_score += best_score
        n_found += 1
    return matches, tot_score/n_matches
