# logging

Setting up and using the [logging package](https://docs.python.org/3/howto/logging.html) from the python standard library is not difficult. Configuring it across multiple files/modules may be slightly more challenging but both demands you - the developer - to read through the docs.

I encourage you to do that if you have some hours for reading and playing around with different modes.

But the reason to have logging set up in this template is to make you do log messages out-of-the box with a pre-configured loggging configuration unifying log messages for our python projects.  

Use the template's logging in your project with:
```python
from equayes.utils import log

logger = log.getLogger()

logger.debug("I'm a debug message")
logger.info("I'm an info message")
logger.warning("I'm a warning message")
logger.error("I'm an error message")
```

```{admonition} Tip
:class: tip
You can use logging also inside a jupyter notebook.
```

You can use the logger of course also inside a juyter notebook.  
Your log messages are displayed in a less verbose form in the standard output (your CLI by default) and are stored with full context in log files stored in `equayes/logs`. For each calendar day, a new log file is created, the old ones (up to 20) are renamed.
