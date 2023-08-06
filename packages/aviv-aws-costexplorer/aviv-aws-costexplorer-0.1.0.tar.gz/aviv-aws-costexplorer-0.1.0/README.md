# Aviv AWS CostExplorer

Aims to provide a quick and comprehensive interface to AWS costexplorer api.
This is useful to extract cost and usage (aka CAU) data, save it and to make it available for reporting and analysis.

## Requirements

- python >= 3.8
- boto3
- Access to AWS ce:cost_and_usage

## Usage

```python
from aviv_aws_costexplorer import costreporter

cr = costreporter.CostReporter()
costs = cr.get_cost_and_usage()
# Will print you last 3 months costs
print(costs)

# Show it nicely
import pandas as pd
df = pd.DataFrame(costs)
df.head()
```

## Development

```bash
pipenv install -d
```

## Test, Build, Release

```bash
# Run tests
pipenv run pytest -v tests/

# Build python package
python3 setup.py sdist bdist_wheel

# Release on testpypi
python3 -m twine upload --repository testpypi dist/*
```

Note: the Pypi release is also done during the CICD process.

## Contribute

Yes please! Send us your PR's
