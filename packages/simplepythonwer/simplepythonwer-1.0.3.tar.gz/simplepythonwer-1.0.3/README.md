# SimplePythonWER

The purpose of this repo is to provide a well tested basic python implementation of levenshein / WER so it can be shared across projects.
It's based on [this](http://hetland.org/coding/python/levenshtein.py) with a couple of minor changes.


## Getting Started
 1. Install with: `pip install simplepythonwer`
 2. Import with: `from simplepythonwer import wer`
 3. Use with:
```python
>>> wer("the cat sat on the mat", "the mat sat on the cat")
0.3333333333333333
```

## Features
 - Simple, minimal and only in python with 0 external dependencies
 - It is versioned and can be pip installed
 - Provide examples with [tests](test/test_wer.py) to ensure it's working correctly

## Caveats and Gotchas
 - Providing an empty string or filled with whitespace ground-truth will intentionally raise a divide by zero.
 - It's possible to have greater than 100% WER if the ASR result is many times larger than the ground-truth, this is normal. 
   It's sometimes a good idea to cap the results at a 100% with min function e.g.
   ` min(wer(ground_truth, new_asr_string), 1.0)`, otherwise you could be exposed to unlimited error rate that could skew your averages.


## Change Log
 - v1.0.0 - First release - Minor ~15% speed improvements compared to original 
 - v1.0.1 - Fixed pip packaging and added install steps. Exclude tests from pip
 - v1.0.2 - Fixed pip packaging issue
 - v1.0.3 - Fixed divide by zero error when the ground truth is zero length (including evaluates to zero length since it's just whitespace)


## Tests
 Run with: `PYTHONPATH=$(pwd) python3 -m unittest discover .`
 Results:
```shell
rob@rob-T480s:~/projects/SimplePythonWER (master)$ PYTHONPATH=$(pwd) python3 -m unittest discover .
..
----------------------------------------------------------------------
Ran 9 tests in 0.001s

OK

```

##  Speed Improvements
```python
from simplepythonwer.simplepythonwer import *
import timeit
sentence = "the cat sat on the mat"*5
print(timeit.timeit('levenshtein(sentence, sentence[::-1])', number=10000, globals=globals()))
print(timeit.timeit('levenshtein_original(sentence, sentence[::-1])', number=10000, globals=globals()))
38.16882774699479
44.751817572047
```
