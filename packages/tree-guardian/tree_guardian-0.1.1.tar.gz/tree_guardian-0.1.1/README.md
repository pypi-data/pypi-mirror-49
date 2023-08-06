# Tree Guardian

Track the changes into the filesystem and trigger callback on changes 
 detecting.


## Getting Started

### Installation

```bash

pip install tree-guardian
```

### Usage

Observe the changes into your project.

```python

from tree_guardian import observe

# Target function to trigger
def cb():
    from time import time

    print('[{}] Changes detected...'.format(time()))

observe(cb)  # Run observer
```
