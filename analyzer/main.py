from analyzer.nonlinearity import nonlinearity
from analyzer.sac import sac
from analyzer.du import differential_uniformity
from analyzer.bic import bic_nl, bic_sac
from analyzer.lap import lap
from analyzer.dap import dap
from analyzer.ad import algebraic_degree
from analyzer.to import transparency_order
from analyzer.ci import correlation_immunity

def analyze_sbox(sbox):
    return {
        "Nonlinearity (NL)": nonlinearity(sbox),
        "Strict Avalanche Criterion (SAC)": round(sac(sbox), 5),
        "BIC Nonlinearity (BIC-NL)": bic_nl(sbox),
        "BIC SAC (BIC-SAC)": round(bic_sac(sbox), 5),
        "Linear Approximation Probability (LAP)": lap(sbox),
        "Differential Approximation Probability (DAP)": dap(sbox),
        "Differential Uniformity (DU)": differential_uniformity(sbox),
        "Algebraic Degree (AD)": algebraic_degree(sbox),
        "Transparency Order (TO)": transparency_order(sbox),
        "Correlation Immunity (CI)": correlation_immunity(sbox)
    }
