# Имло лойиҳасининг асосий қисми Python кутубхонаси

## Муҳит

  * Python>=3.7


## Кутубхоналар

  * NLTK
  * Gensim
  * Spacy
  * HunSpell


## Пакетни ўрнатиш

```bash
$ pip install imlo
```


## Намуна

```python
from imlo.transliteration import lat2cyr, cyr2lat
...
text = lat2cyr('salom dunyo')
print(text)
```


## Тест қилиш тартиби

```bash
$ python -m unittest
```


## Ҳисса қўшиш

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## Лицензия
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
