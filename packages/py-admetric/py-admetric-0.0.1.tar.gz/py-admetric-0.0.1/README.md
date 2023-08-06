# py-admetric

## What is py-admetric?
Provide calculation methods often used in digital advertising industry

## What does py-admetric provide?
1. CPI (Cost Per Impression)
2. CPM (Cost Per Thousand Impressions (Cost Per Mille))
3. CPC (Cost Per Click)
4. CPA (Cost Per Action (Cost Per Acquisition))
5. CPV (Cost Per View)
6. CTR (Click Through Rate)
7. VTR (View Through Rate)
8. CVR (Conversion Rate)

## Installation
```shell
$ pip install py-admetric
```

## Usage and Example
### Example: CPM
```python
from py_admetric import py_admetric
cpm = py_admetric.cpm(50000, 1000)
```
