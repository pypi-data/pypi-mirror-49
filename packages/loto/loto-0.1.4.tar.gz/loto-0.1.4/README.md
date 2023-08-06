# loto : Lockout-Tagout

Loto provides a simple decorator for functions
that need to access critical sections with mutex locks.

When you decorate a function with `@LockoutTagout(tag)`,
the function call will block until it can acquire a mutex lock
shared between all functions with the same tag.


## Example

```python
from loto import LockoutTagout

from threading import Thread
from random import random
from time import sleep

data = [1, 2, 3]

@LockoutTagout('data1')
def readData1(sharedData):
    for val in sharedData:
        print(val)
        sleep(random())

@LockoutTagout('data1')
def writeData1(sharedData):
    for i in range(0, 3):
        sharedData[i] += 1
        sleep(random())

for i in range(0, 5):
    Thread(target=readData1, args=(data,)).start()
    Thread(target=writeData1, args=(data,)).start()
```

These two functions will lockout-tagout with the same tag,
so they will acquire a lock managed by this decorator class before
they're executed. This means that no two functions with the same
tag can be executing concurrently.


One mutex lock is managed per unique tag.


## Installation
You can install this module from PyPI with
```
pip install loto
```
