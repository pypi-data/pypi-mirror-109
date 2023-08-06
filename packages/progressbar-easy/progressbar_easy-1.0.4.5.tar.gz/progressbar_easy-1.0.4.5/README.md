# Progress Bar
This is a simple progress bar that allows for easy use to display progress.

# FEATURES
- Timer to estimate time remaining
- Timer adjusts to rates
- Choice of length of bar
- Choice of character bar is made of
- Option for item count or percentage completed (or both)

# Usage
Imported with `from progressbar import ProgressBar`

Initialize object with `bar = ProgressBar(number of iterations)`

Use in loop. Inside loop at the end, put `bar.update()` or `bar += 1`.
Prefer `bar.update()`

## Or
Use as an iterator object

```Python
for i in ProgressBar(range(10)):
    ...
```