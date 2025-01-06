# Football-Adapted Wisconsin Card Sorting Test (WCST)

## Overview
This repository contains a Python implementation of a football-adapted Wisconsin Card Sorting Test, designed to assess cognitive flexibility and decision-making in football contexts. The experiment is built using PsychoPy and is suitable for research in sports psychology and cognitive science.

## Key Features
- Role-based scenarios (Attacker, Midfielder, Defender)
- 9 trials with 10 scenarios each
- Integrated demographic data collection
- Automated error classification (perseverative/non-perseverative)
- Comprehensive data output in CSV format

## Directory Structure
```
football-wcst/
│
├── football-wcst.py                 # Main experiment script
│
├── scenarios/             # Stimulus images
│   ├── attacker/         # Attacker-specific scenarios
│   ├── midfielder/       # Midfielder-specific scenarios
│   ├── defender/         # Defender-specific scenarios
│   └── macro/           # Macro tactical scenarios
│
├── analysis.rmd           # R Markdown analysis
│
└── results/              # Output directory for CSV files
```

## Image Naming Convention
Scenarios follow a strict naming convention:
- Role-specific: `[a/m/d][1-5]*.png`
- Macro scenarios: `m[1-5]*.png`
- Response options: `*_s.png` (selfish), `*_t.png` (team), `*_h.png` (hold)

## Data Output Format
The experiment generates CSV files with the following columns:
- Participant demographics (ID, age, gender, experience)
- Trial information
- Response data (selected rule, reaction time)
- Error classification
- Scenario tracking
- Feedback history
