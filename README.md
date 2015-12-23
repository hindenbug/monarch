# Monarch
Monarch is a throttle for communication via APN &amp; GCM push notifications.


# Install

	$ pip install monarch-dnd

# Getting Started

```python
import monarch
monarch.configure()
monarch.config.rule.add('notification', 'promotion', 60)

array = []
with monarch.throttle('notification', 10, 'promotion') as pipe:
    if pipe: array.append(1)
with monarch.throttle('notification', 10, 'promotion') as pipe:
	if pipe: array.append(2)

print array
# [1]
```
# Development

```
	$ python setup.py develop
```

# Tests
```
  $ python setup.py test
```

