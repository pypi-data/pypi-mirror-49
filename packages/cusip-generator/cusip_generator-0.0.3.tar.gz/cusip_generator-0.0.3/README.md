# cusip_generator
Generate modified CUSIPs given Bloomberg Tickers

# Usage
```bash
    # install the package
    pip install cusip_generator
```

```python
    # in your project
    from cusip_generator import Generator
    generator = Generator('AIH8 Index')
    cusip = generator.convert_to_cusip()
```

# Run Tests
`python -m unittest discover tests`


