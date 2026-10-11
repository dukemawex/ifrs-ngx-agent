"""Small-cluster panel econometrics written out explicitly (numpy), so every step of the inference is auditable.

fe_ols(): within (bank fixed-effects) OLS by demeaning y and X within bank (Frisch-Waugh-Lovell), with
  - conventional (homoskedastic) standard errors, df = N - K - G;
  - CR1 bank-clustered standard errors, small-sample factor G/(G-1) * (N-1)/(N-K), t(G-1) reference;
    K counts the non-absorbed regressors (bank effects are nested within clusters, as in Stata xtreg);
  - wild cluster restricted (WCR) bootstrap-t p-values (Cameron, Gelbach & Miller 2008; Webb 2023 six-point
    weights, recommended when G < ~12), imposing H0: beta_k = 0, B = 9,999, fixed seed.
pooled_ols(): the same machinery without demeaning (intercept added).
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats

WEBB = np.array([-math.sqrt(1.5), -1.0, -math.sqrt(0.5), math.sqrt(0.5), 1.0, math.sqrt(1.5)])
B_DEFAULT = 9999
SEED = 20261011


def demean(a: np.ndarray, groups: np.ndarray) -> np.ndarray:
    a = np.asarray(a, float)
    out = a.copy()
    for g in np.unique(groups):
        m = groups == g
        out[m] = a[m] - a[m].mean(axis=0)
    return out


def _cr1_se(X, u, groups, XtXi, k_extra=0):
    N, K = X.shape
    G = len(np.unique(groups))
    meat = np.zeros((K, K))
    for g in np.unique(groups):
        s = X[groups == g].T @ u[groups == g]
        meat += np.outer(s, s)
    c = G / (G - 1) * (N - 1) / (N - K - k_extra)
    V = c * XtXi @ meat @ XtXi
    return np.sqrt(np.clip(np.diag(V), 0, None)), c


def wcr_pvalue(X, y, groups, k, B=B_DEFAULT, seed=SEED, k_extra=0):
    """Wild cluster restricted bootstrap-t p-value for H0: beta_k = 0 (two-sided, symmetric)."""
    N, K = X.shape
    ug, gi = np.unique(groups, return_inverse=True)
    G = len(ug)
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ X.T @ y
    u = y - X @ b
    se, c = _cr1_se(X, u, groups, XtXi, k_extra)
    t_obs = b[k] / se[k]
    Xr = np.delete(X, k, axis=1)
    br = np.linalg.pinv(Xr.T @ Xr) @ Xr.T @ y
    yr, ur = Xr @ br, y - Xr @ br
    rng = np.random.default_rng(seed)
    W = WEBB[rng.integers(0, 6, size=(G, B))]           # G x B
    Ys = yr[:, None] + ur[:, None] * W[gi, :]           # N x B
    Bs = XtXi @ X.T @ Ys                                # K x B
    Us = Ys - X @ Bs
    a = X @ XtXi[k]                                     # N: influence of obs on beta_k
    S = np.zeros((G, B))
    np.add.at(S, gi, a[:, None] * Us)
    se_k = np.sqrt(c * (S ** 2).sum(axis=0))
    t_star = Bs[k] / se_k
    return float(np.mean(np.abs(t_star) >= abs(t_obs))), float(t_obs)


def fit(X, y, groups, names, absorbed_groups=0, bootstrap=True, B=B_DEFAULT):
    """OLS on (already transformed) X, y. absorbed_groups = number of absorbed bank effects (for conventional df)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    N, K = X.shape
    G = len(np.unique(groups))
    XtXi = np.linalg.pinv(X.T @ X)
    b = XtXi @ X.T @ y
    u = y - X @ b
    df_conv = N - K - absorbed_groups
    s2 = (u @ u) / df_conv if df_conv > 0 else float("nan")
    se_conv = np.sqrt(np.clip(np.diag(XtXi) * s2, 0, None))
    se_cr1, _ = _cr1_se(X, u, groups, XtXi)
    out = []
    for k, nm in enumerate(names):
        t_conv = b[k] / se_conv[k] if se_conv[k] > 0 else float("nan")
        t_cr1 = b[k] / se_cr1[k] if se_cr1[k] > 0 else float("nan")
        p_conv = 2 * stats.t.sf(abs(t_conv), df_conv) if df_conv > 0 else float("nan")
        p_cr1 = 2 * stats.t.sf(abs(t_cr1), G - 1)
        tcrit = stats.t.ppf(0.975, G - 1)
        p_wcb = wcr_pvalue(X, y, groups, k, B=B)[0] if bootstrap and K >= 1 and G >= 3 else float("nan")
        out.append({"term": nm, "coef": b[k], "se_conventional": se_conv[k], "p_conventional": p_conv,
                    "se_cr1": se_cr1[k], "t_cr1": t_cr1, "p_cr1_tG1": p_cr1,
                    "ci95_low_cr1": b[k] - tcrit * se_cr1[k], "ci95_high_cr1": b[k] + tcrit * se_cr1[k],
                    "p_wild_cluster_bootstrap": p_wcb})
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1 - (u @ u) / ss_tot if ss_tot > 0 else float("nan")
    return out, {"N": N, "clusters": G, "K": K, "df_conventional": df_conv, "r2": r2, "resid": u, "XtXi": XtXi, "b": b}


def vif(X: np.ndarray, names: list[str]) -> dict[str, float]:
    """VIF of each column of an (already demeaned) design, via auxiliary regressions without intercept."""
    out = {}
    for k, nm in enumerate(names):
        if X.shape[1] == 1:
            out[nm] = 1.0
            continue
        y = X[:, k]; Z = np.delete(X, k, axis=1)
        bz = np.linalg.pinv(Z.T @ Z) @ Z.T @ y
        r2 = 1 - ((y - Z @ bz) ** 2).sum() / (y ** 2).sum() if (y ** 2).sum() > 0 else 0
        out[nm] = 1 / (1 - r2) if r2 < 1 else float("inf")
    return out


def influence(X, y, XtXi, b, k):
    """Leverage, Cook's distance and DFBETA(k) for the transformed regression."""
    N, K = X.shape
    h = np.einsum("ij,jk,ik->i", X, XtXi, X)
    u = y - X @ b
    s2 = (u @ u) / max(N - K, 1)
    cook = (u ** 2 / (K * s2)) * h / np.clip((1 - h) ** 2, 1e-12, None)
    dfb = np.zeros(N)
    for i in range(N):
        m = np.ones(N, bool); m[i] = False
        Xi, yi = X[m], y[m]
        bi = np.linalg.pinv(Xi.T @ Xi) @ Xi.T @ yi
        si = math.sqrt(((yi - Xi @ bi) ** 2).sum() / max(N - 1 - K, 1))
        dfb[i] = (b[k] - bi[k]) / (si * math.sqrt(XtXi[k, k]))
    return h, cook, dfb


def residual_tests(u: np.ndarray, X: np.ndarray) -> dict:
    jb = stats.jarque_bera(u)
    # Breusch-Pagan (Koenker studentised): n * R2 of u^2 on X
    e2 = u ** 2
    Z = np.column_stack([np.ones(len(u)), X])
    bz = np.linalg.pinv(Z.T @ Z) @ Z.T @ e2
    r2 = 1 - ((e2 - Z @ bz) ** 2).sum() / ((e2 - e2.mean()) ** 2).sum()
    bp = len(u) * r2
    return {"jarque_bera_p": float(jb.pvalue), "breusch_pagan_lm": float(bp),
            "breusch_pagan_p": float(stats.chi2.sf(bp, X.shape[1]))}
