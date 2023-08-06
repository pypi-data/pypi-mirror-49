# pyterm_progress_bar

Prints a progress bar to the terminal from python.


### ProgressBar
```python
import pyterm_progress_bar

progress_bar = pyterm_progress_bar.ProgressBar(
    name='Progress',  # Default
    char='#'  # Default
)
progress_bar.start()

for i in range (0, 5):
    # Do stuff
    progress_bar.update((i+1)/5)  # between 0 and 1 inclusive.

```

### Loop
pyterm_progress_bar can automatically perform a loop for you to save you having to do the difficult math.

```python
import pyterm_progress_bar

def my_func(counter, data):  # data param is optional here
    # Do stuff
    # 'counter' is the loop counter
    # 'data' is whatever you pass as 'param' in the next step

loop = pyterm_progress_bar.Loop(
    my_func,
    number_of_iterations=300,
    param=['foo', 'bar', '🐙'],  # Optional
    progress_bar_name='Running my_func',  # Default
    progress_bar_char='#'  # Default
)
loop.execute()

```
