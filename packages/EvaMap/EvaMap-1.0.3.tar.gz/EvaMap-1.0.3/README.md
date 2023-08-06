# LibraryEvaMap

A python library that can assess the quality of an RDF mapping.

### Installation

Installation in a `virtualenv` is recommended.

Assuming you already have `python 3` and `pip` installed

```bash
pip install EvaMap
```

### Initialize EvaMap

First, instantiation of an EvaMap object takes three parameters:

1) **rdf_ontology**: The ontology used in the yarrrml_mapping in RDF (turtle, xml or n3)
2) **yarrrml_mapping**: The RDF mapping of the json_data in YARRRML
3) **json_data**: The dataset in JSON format

```python
from EvaMap.EvaMap import EvaMap

evamap = EvaMap(rdf_ontology, yarrrml_mapping, json_data)
```

### Assess the mapping

You can assess the quality of the **yarrrml_mapping** by using the `evaluate_mapping` method:

```python
evamap.evaluate_mapping()
```

### Retrieve results

After evaluation, you can retrieve the total score of the **yarrrml_mapping** with _get_total_score()_ method:

```python
evamap.get_total_score() # e.g., 0.6805555555555557
```

or, a list of Dict representing score for each dimensions, metrics and feedbacks with _get_complet_result()_ method:

```python
evamap.get_complet_result()
```