<img src="https://images.ctfassets.net/ek6qkphcgu1d/wjdJ8KzwnJW7opcxmcEfs/f6b2cd55a007a2cb06b47e1a6eaf1be9/Primer-logo_Final.png" width="280">

## Automate Python SDK
This is the unofficial Python SDK for Primer Automate.

## Getting Started

### Nomenclature/Glossary
| **Term** | **Definition** |
| --- | --- |
| **Models**| A list of the models in your account (templates you’ve liked and want to use). This is unique to you.  Each model links to a page where you can get predictions or API credentials.|
| **Datasets** | Data you upload is shared amongst your organization. Can be used in model preview or to get large scale predictions.|
| **Prediction** | A prediction is what a model does with a piece of data you provide it. Each model may provide a different kind of result, but every unique judgment it makes is a prediction. |
| **Labels** | Each prediction provides one or a number of labels. If a model can predict ten labels, for example our COVID classification model, your prediction will include ten results for the ten labels. |


### Requirements

Python 3.6 or later.

The SDK has some requirements, so before installing, make sure to run:

```
pip install -r requirements.txt
```

## Usage

### How to create a classifier

```python
import csv
from automate_client import AutomateClient, AutomateClassifierDatasetRow

## Create a client with your Automate username and password
client = AutomateClient(username="USERNAME", password="PASSWORD")

## You just need to map the rows of your training data to
## the AutomateClassifierDatasetRow object (the text, and then an array of labels)
csv_rows = []
with open("./training_data.csv", encoding="utf-8") as documents:
    reader = csv.reader(documents)
    rows = list(reader)

    ## Don't need the header row
    rows = rows[1:]

    for row in rows:
        text = row[0]
        labels = row[1]

        csv_rows.append(AutomateClassifierDatasetRow(text, labels)) # { "text": "Some text!", "labels": ["Label A", "Label B"]}

## Give the classifier a name, and pass your training data
## It will automatically detect if it's a binary, multi-label or multiclass depending on the setup of your `labels` across all your AutomateClassifierDatasetRow
client.make_classifier('SDK', data=csv_rows)
```

## How to get your models

```python
## Create a client with your Automate username and password
client = AutomateClient(username="USERNAME", password="PASSWORD")

models = client.get_models()['models']
```

## How to get your datasets

```python
## Create a client with your Automate username and password
client = AutomateClient(username="USERNAME", password="PASSWORD")

datasets = client.get_datasets()['datasets']
```
