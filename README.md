# Black Swan

This projects organizes all other services and provides an easy way of running all.

## If you create some service, you can add its repo as submodule
```
git submodule add <url> <folder>
```

## Start
```
git submodule update --recursive --init
git submodule update --recursive --remote --force
python3 start.py
```