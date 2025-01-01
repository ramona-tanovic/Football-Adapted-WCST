# Football-Adapted Wisconsin Card Sorting Test (WCST)

## Overview
This repository contains a Python implementation of a football-adapted Wisconsin Card Sorting Test, designed to assess cognitive flexibility and decision-making in football contexts. The experiment is built using PsychoPy and is suitable for research in sports psychology and cognitive science.

## Key Features
- Role-based scenarios (Attacker, Midfielder, Defender)
- 9 trials with 10 scenarios each
- Integrated demographic data collection
- Automated error classification (perseverative/non-perseverative)
- Comprehensive data output in CSV format

## Prerequisites
```python
pip install psychopy
```

## Directory Structure
```
football-wcst/
│
├── main.py                 # Main experiment script
├── requirements.txt        # Dependencies
│
├── scenarios/             # Stimulus images
│   ├── attacker/         # Attacker-specific scenarios
│   ├── midfielder/       # Midfielder-specific scenarios
│   ├── defender/         # Defender-specific scenarios
│   └── macro/           # Macro tactical scenarios
│
└── results/              # Output directory for CSV files
```

## Image Naming Convention
Scenarios follow a strict naming convention:
- Role-specific: `[a/m/d][1-5]*.png`
- Macro scenarios: `m[1-5]*.png`
- Response options: `*_s.png` (selfish), `*_t.png` (team), `*_h.png` (hold)

## Running the Experiment
```python
python main.py
```

## Data Output Format
The experiment generates CSV files with the following columns:
- Participant demographics (ID, age, gender, experience)
- Trial information
- Response data (selected rule, reaction time)
- Error classification
- Scenario tracking
- Feedback history

## Example Data Analysis
```python
import pandas as pd

# Load experiment data
data = pd.read_csv('results/Football-Adapted_WCST_P001_2024-01-01.csv')

# Calculate basic metrics
accuracy = data['Correct'].mean()
perseverative_errors = data['Perseverative_Error'].sum()
mean_rt = data['Reaction_Time'].mean()
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add enhancement'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## Citation
If you use this implementation in your research, please cite:
```bibtex
@misc{football_wcst_2024,
  author = {[Author Name]},
  title = {Football-Adapted Wisconsin Card Sorting Test},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/[username]/football-wcst}
}
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- PsychoPy development team
- Wisconsin Card Sorting Test original authors
- [Your Institution Name]

## Contact
For questions or support, please open an issue or contact [your.email@institution.edu]

---
*Note: This experiment is part of ongoing research in sports cognition and decision-making. For research purposes only.*
