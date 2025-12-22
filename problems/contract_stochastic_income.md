---
id: contract_stochastic_income
title: Optimal Consumption Under Stochastic Income (root solve + constraint)
difficulty: hard
tags: contract-theory, expected-utility, numerical-methods
expected_answer_format: "float (c_high)"
---

## Problem
**NDA-safe note:** synthetic numbers, inspired by real math/econ modeling, not copied from private systems.

## Model
Solve c_high such that V0=(0.5 ln(0.95)+0.5 ln(c_high))/(1-0.95)=3.0, with c_high>=1.1. Use bisection.

## Output
Return only the final numeric answer in the expected format.

## Common failure modes
Forgetting 1/(1-delta), using log10, ignoring constraint, no bracketing.
