# euros
[![](https://img.shields.io/badge/pypi-v0.0.3-blue)](https://pypi.org/project/euros/)

Simple script python destiné à convertir des chiffres en lettres, pour désigner un montant en euros en français littéral respectant les règles orthographiques.

Installation :
```python
python3 -m pip install euros
```

Exemples d'utilisation :

```python
>>> from euros import fr

>>> fr.conv(10) 
# Output : "dix euros"`

>>> fr.conv(120.99) 
# Output : "cent vint euros et quatre-vingt-dix-neuf centimes"
```
