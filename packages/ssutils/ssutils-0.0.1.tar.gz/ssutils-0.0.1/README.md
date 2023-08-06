# ssutils
collection of useful python functions


## Screenwriter

Use Screenwriter to prefix screen prints
**Examples**

### 1 - Default prefix ###

```python
from ssutils import Screenwriter

sw = Screenwriter ()
sw.echo ('my output')
```
```
Output:
2019-07-26 11:16:04 my output
```

### 2 - Date Time parts in prefix ###

```python
from ssutils import Screenwriter

sw = Screenwriter ('%Y-%m-%d %H:%M:%S.%f ')
sw.echo ('my output')
```
```
Output:
2019-07-26 11:16:04 my output
```

For format options, see http://strftime.org/
