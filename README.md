# DoNotDisturb
DoNotDisturb is a throttle for communication via APN &amp; GCM push notifications. 


# Install

	$ python setup.py install

# Getting Started

```python
import dnd
dnd.configure()
dnd.config.rule.add('notification', 'promotion', 60)

array = []
with dnd.throttle('notification', 10, 'promotion') as pipe:
    if pipe: array.append(1)
with dnd.throttle('notification', 10, 'promotion') as pipe:
	if pipe: array.append(2)

print array
# [1]
```
# Development

	$ python setup.py develop

# Publish

	$ python setup.py sdist
	$ python setup.py sdist upload


