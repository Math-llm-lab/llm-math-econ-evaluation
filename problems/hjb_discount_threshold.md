---
id: hjb_discount_threshold
title: HJB inequality critical discount rate
difficulty: medium
tags: stochastic-control, hjb, verification
expected_answer_format: "float (rho_critical)"
---

## Problem
**NDA-safe note:** synthetic numbers, inspired by real math/econ modeling, not copied from private systems.

## Model
At x=0,y=1,p=1,b=1,sigma=0.2,gamma=0.7 find smallest rho s.t. F(rho)>=0 (see models/hjb_discount_threshold.py).

## Output
Return only the final numeric answer in the expected format.

## Common failure modes
Sign error in gamma(gamma-1), missing 1/2, returning non-minimal rho.
