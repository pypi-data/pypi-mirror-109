from setuptools import setup

ld = """
I have noticed that switch/case statements are coming to Python, so I thought it would be amusing to release the 101002938662893028482039th "Missing switch/case package" to this platform.

```python
import switchem

MONKEY = 1
ELEPHANT = 2
GIRAFFE = 3
HORSE = 4
SQUIRREL = 5
SQUID = 6
COW = 7
SARCASTIC_FRINGEHEAD = 8

with switchem(HORSE) as case:
    if case(MONKEY):
        print("It is a monkey")
        raise case
    
    if case(ELEPHANT, GIRAFFE, HORSE):
        print("It is not a monkey for sure")
    
    if case(SQUIRREL):
        print("It could be a squirrel")
        raise case
    
    print("It is definitely not a monkey, elephant, giraffe, horse, or squirrel")
```

This has the fall-through behaviour (fall-through will activate as soon as the correct value is checked).
To "break", raise the case object within the context.
"""

setup(
    name='switchem',
    packages=["switchem"],
    version='1.0.0',
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    install_requires=["onetrick~=2.1"],
    python_requires="~=3.9",
    long_description=ld,
    long_description_content_type="text/markdown"
)