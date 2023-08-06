# thunk-dict

Dictionaries that enable the lazy evaluation and memoization of callable entries. thunk-dict is meant to serve as a convenient wrapper the lazy evaluation of potentially computationally expensive calls.

## Use case

Because Python eagerly evaluates expressions, it is not possible include calls to functions within a dictionary without evaluating those calls first. To mimic lazy evaluation, one may turn to tricks like:

```python
dictionary = {
  "key1": computationally_expensive_function
}

# Call the function later on
result = dictionary["key1"]()
```

or alternatively, if you also wanted to pass in arguments later on,

```python
dictionary = {
  "key1": lambda *args, **kwargs: computationally_expensive_function(*args, **kwargs)
}

# Call the function later on
result = dictionary["key1"]("blah", parameter=100)
```

However, this approach suffers from two issues:

1. It complicates the typing of your dictionaries and its entries and creates boilerplate (as in the second example).
2. Reaccess requires the computationally expensive functions to be called again (i.e. the call isn't memoized)

thunk-dict attempts to resolve both of these issues.

```python
from thunk_dict import ThunkDict
dictionary = ThunkDict({
  "key1": computationally_expensive_function
})

# Get result from call via simple access
result = dictionary["key1"]

# Subsequent accesses use the memoized result.
```

For noncallable entries, thunk-dict works just like a regular dict. thunk-dict also features the same API as regular Python dictionaries, meaning you don't have to sacrifice anything by using its wrapper.

## Features
1. Convenient thunk-like behavior in dictionaries
2. Works for any objects that register with dict
3. Very low overhead

## Installation

From PyPi
```bash
pip install thunk-dict
```

From source distribution
```bash
git clone https://github.com/kevalii/thunk-dict.git
cd https://github.com/kevalii/thunk-dict.git
pip install .
```