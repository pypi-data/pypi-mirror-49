# python-lib-template

```python
config = Config('./ciao.yaml')

# writes a new field in config
config.write(f'cose.cosa', 'ciao')
print(config['cose']['cosa']) # ciao

# pushes a new obj in config
config.push(f'arrays.array_id', 1)
config.push(f'arrays.array_id', 2)
print(config['arrays']['array_id']) # [1, 2]

```

```yaml
cose:
    cosa: ciao

arrays:
    array_id:
        - 1
        - 2
```