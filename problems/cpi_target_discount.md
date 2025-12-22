---
id: cpi_target_discount
title: CPI targeting discount via bisection
difficulty: medium
tags: index-numbers, bisection
expected_answer_format: "float (t in [0,1])"
---

## Problem
**NDA-safe note:** synthetic numbers, inspired by real math/econ modeling, not copied from private systems.

## Model
CPI(t)=(200+100+EI_c(t))/3, EI_c(t)=(10*(1-0.21t)/3.15)*100. Find t so CPI(t)=200 using bisection.

## Output
Return only the final numeric answer in the expected format.

## Common failure modes
Wrong scaling x100, wrong coefficient 0.21, percent vs fraction, not bounding t.
