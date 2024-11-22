<!-- markdownlint-disable first-line-heading -->

<!-- markdownlint-capture -->
<!-- markdownlint-disable no-inline-html -->
<div align="center">
  <a href="https://github.com/censor-text/censore">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="public/logo-dark.png">
      <source media="(prefers-color-scheme: light)" srcset="public/logo-light.png">
      <img src="public/logo-dark.png" alt="Banner">
    </picture>
  </a>
  
  <!-- markdownlint-disable-next-line heading-start-left -->
  ### censore

  <p align="center">
    A tool for censoring obscene language
    <br />
    <br />
    <a href="https://github.com/censor-text/censore/issues/new?labels=bug"><b>Report Bug</b></a>
    ·
    <a href="https://github.com/censor-text/censore/issues/new?labels=enhancement"><b>Request Feature</b></a>
  </p>
</div>
<!-- markdownlint-restore -->

## About The Project

This tool helps identify and censor profanity with high accuracy. It supports multiple languages and can be used in various scenarios, such as chats, social networks, and more.

## ⚙️ Installation

```bash
pip3 install censore
```

## 🚀 Usage

### ProfanityFilter

First, initialize the `ProfanityFilter` class:

```python
from censore import ProfanityFilter
pf = ProfanityFilter()
```

By default `ProfanityFilter` will be initialized with all available languages

If you want to process the text only in certain languages, it is recommended to manually configure the list of languages ​​to be checked, this will greatly speed up the text processing:

```python
from censore import ProfanityFilter
pf = ProfanityFilter(languages=['en', 'uk'])
```

#### `custom_patterns`

You can add custom patterns of offensive words if they are not present:

```python
pf = ProfanityFilter(custom_patterns=["bad"])
text = "This is a very bad text, let's say 'baddest'"
pf.censor(text)
# 'This is a very ### text, let we say '#######''
```

As you can see it also censored the word "baddest" because it contains "bad"

But if you don't want it to censor that word, you can use the `custom_exclude_patterns` parameter:

```python
pf = ProfanityFilter(custom_patterns=["bad"], custom_exclude_patterns=["baddest"])
text = "This is a very bad text, let we say 'baddest'"
pf.censor(text)
# 'This is a very ### text, let we say 'baddest''
```

It will use only English (`en`) and Ukrainian (`uk`) languages

### `contains_profanity`

The `contains_profanity` method checks if the text contains obscene language:

```python
text = "This is a fucking bad text"
pf.contains_profanity(text)
# True
```

### `censor`

The `censor` method replaces obscene language with hashes (`#`):

```python
text = "This is a fucking bad text"
pf.censor(text)
# 'This is a ####### bad text'
```

#### `partial_censor`

You can also partially censor text using the `partial_censor` option:

```python
pf.censor(text, partial_censor=True)
# 'This is a fu###ng bad text'
```

#### `censor_symbol`

You can replace the hashes with any symbol, such as a monkey emoji 🙈:

```python
pf.censor(text, censor_symbol="🙈")
# 'This is a 🙈🙈🙈🙈🙈🙈🙈 bad text'
```

#### `languages`

It may be that you initialized only English and Ukrainian, but at some point you need to use Polish, for this you can use the `languages` parameter:

```python
text = "This is a kurwa блять bad text"
pf.censor(text, languages=['en', 'uk', 'pl'])
# 'This is a ##### ##### bad text'
```

It automatically initialized and loaded the Polish language into the list of languages and successfully censored everything, but don't you want to enter the list of languages ​​you want to use every time?

To simplify this, use the `additional_languages` option:

```python
pf.censor(text, additional_languages=['pl'])
# 'This is a ##### ##### bad text'
```

It has now added Polish to all initialized languages ​​and now we don't need to enter the full list of languages

---

## Other methods

### `censor_word`

This method censors any word

```python
pf.censor_word("anyword")
# '###'
```

#### `partial_censor`

You can also partially censor text using the `partial_censor` option:

```python
pf.censor_word("anyword", partial_censor=True)
# 'an###rd'
```

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the **MIT** License. See [**LICENSE**](LICENSE) for more information.

## 📨 Contact

**Telegram** - [@okineadev](https://t.me/okineadev)
