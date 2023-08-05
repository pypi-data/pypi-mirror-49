# Open Dota 2 Python API

![coverage](https://gitlab.com/avalonparton/opendota2py/badges/master/coverage.svg) | [![PyPI version](https://badge.fury.io/py/opendota2py.svg)](https://badge.fury.io/py/opendota2py)

A Python 3 module for the OpenDota API

## Installation

```bash
pip3 install opendota2py
```

## Usage
 
[Documentation](https://avalonparton.gitlab.io/opendota2py/opendota2py/)

```python
>>> import opendota2py
>>> player = opendota2py.Player(82279028)
>>> player.mmr_estimate
2967
>>> match = player.recent_matches[0]
>>> match.radiant_win
True
>>> match.radiant_score
37
>>> hero = opendota2py.Hero(1)
>>> hero.name
'npc_dota_hero_antimage'
>>> hero.localized_name
'Anti-Mage'
>>> hero.legs
2
```
