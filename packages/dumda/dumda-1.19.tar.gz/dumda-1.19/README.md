# Dumda
Python Library to get fast extensive Dummy Data for testing
## Installation
```
pip install dumda
```


## Usage

### Cities

```python
from dumda.cities import Cities

# initialize cities class
c = Cities()

# get the full list of all available cities (23k+ cities)
c.get_all()
```

Of course, rarely or ever will someone need a list of 23 thousand cities. Not to mention the impact on speed.\
in more common cases, you can extract sample sizes of cities.

#### get single
```python
from dumda.cities import Cities
c = Cities()
c.get_single()
```
#### output:
```bash
'Scicli'
```

#### get a random set of cities
the most basic implementation; get a list of randomly selected cities of a chosen amount
```python
from dumda.cities import Cities
c = Cities()

c.get_random_cities(10)
```

#### output:
```bash

```




### Names

```python
pass
```
### Phone Numbers
```python
pass
```

### Example
```python
pass
```