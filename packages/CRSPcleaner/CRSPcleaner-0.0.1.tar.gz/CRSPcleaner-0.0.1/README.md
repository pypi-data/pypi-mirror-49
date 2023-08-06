# CRSPcleaner

This programme takes in a .csv format CRSP database file and returns a cleaned version as a pandas dataframe.

## Installation

Run the following to install:

```python
pip install CRSPcleaner
```

## Usage
Factors can be extracted in monthly ('m') and annual ('a') frequencies. The default is monthly.

```python
from CRSPcleaner import cleanCRSP

crsp_df = cleanCRSP()

# With CIK identifiers:
crsp_df = cleanCRSP(withCIKonly=True)

```

