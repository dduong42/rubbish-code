# pokemon_music

A useless context manager that plays pokemon music during a long task
(< 15 minutes).

Example:

```python
import time
from pokemon import pokemon_music

with pokemon_music():
    time.sleep(10)
    print("Success !")
```
