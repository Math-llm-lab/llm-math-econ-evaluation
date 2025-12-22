---
id: credit_var_quantile
title: Credit VaR 99.9% (Vasicek, infinitely granular) + MC sanity check
difficulty: hard
tags: risk, var, gaussian-copula, simulation
expected_answer_format: "float (VaR in million USD)"
---

## Problem
**NDA-safe note:** synthetic numbers, inspired by real math/econ modeling, not copied from private systems.

## Model
Compute analytic VaR (Vasicek, infinitely granular portfolio) for E=100, LGD=0.6, PD=0.02, rho=0.2, alpha=0.999, and confirm with MC sanity check.

## Output
Return only the final numeric answer in the expected format.

## Common failure modes
Phi vs Phi^-1, rho mistakes, returning q_alpha not VaR, unstable MC.
