# Natural Language API - Sentiment (GCP)

GN-Sentiment (Natural language API - Sentiment) is a Python library for analyzing sentiments with GCP.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install gnsentiment.

```bash
pip install gnsentiment
```
or

```bash
pip install -i https://test.pypi.org/simple/ gnsentiment
```

## Usage

```python
from gnsentiment import Gnsentiment

s = Gnsentiment('path_key.json')

s.analyze_sentiment('ejemplo texto')
# return: dict(...)

s.sentiment(1)
# return: 1

```

## License
[MIT](https://choosealicense.com/licenses/mit/)
