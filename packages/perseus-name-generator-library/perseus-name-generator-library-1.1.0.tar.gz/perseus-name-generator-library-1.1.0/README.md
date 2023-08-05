# Perseus Name Generator Python Library

Wrapper of [Joao HENRIQUES's `name-gen` library](https://github.com/jotaf98/name-gen), a small module to generate names for characters, places, etc.

To install [Perseus Name Generator Python Library](https://github.com/dcaune/perseus-name-generator-python-library), simply enter the follow command line:

```bash
pip install perseus-name-generator
```

For generating names with a specific language, simply get an instance of the word generator for this language and call the method `generate_name`.  For example:

```python
>>> from majormode.utils.namegen import NameGeneratorFactory
>>> name_generator = NameGeneratorFactory.get_instance(NameGeneratorFactory.Language.Japanese)
>>> name_generator.generate_name()
'Ishimmi'
>>> name_generator.generate_name()
'Suita'
>>> name_generator.generate_name()
'Tashirara'
>>> name_generator.generate_name()
'Miyakai'
>>> name_generator.generate_name()
'Miharadase'
```
