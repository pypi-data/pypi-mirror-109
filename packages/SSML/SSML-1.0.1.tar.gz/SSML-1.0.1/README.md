# Project description
SSML is a SSML builder for Google Assistant and Amazon Alexa.

## Installing

```console
$ pip install -U ssml
```

## Usage
### For Google Assistant

1. Create an object
```python
from ssml import Google


g = Google()
```

2. Add text to the speech
```python
g.add_text("Hello World")
```

3. Build the SSML speech
```python
print(g.speak())
```


### For Amazon Alexa
Yet to come...

## Links
- Documentation: yet to come !!
- [PyPI Releases:](https://pypi.org/project/SSML/)
- [Source Code:](https://github.com/Shinyhero36/SSML/issues)
- [Issue Tracker:](https://github.com/Shinyhero36/SSML/issues)
