<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD041 -->

<div align="center">
  <a href="https://github.com/censor-text/censore">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="public/logo-dark.png" alt="Banner">
      <source media="(prefers-color-scheme: light)" srcset="public/logo-light.png" alt="Banner">
      <img src="public/logo-dark.png" alt="Banner">
    </picture>
  </a>

<h3 align="center">censore</h3>

  <p align="center">
    A tool for censoring obscene language
    <br />
    <br />
    <a href="https://github.com/censor-text/censore/issues/new?labels=bug"><b>Report Bug</b></a>
    ·
    <a href="https://github.com/censor-text/censore/issues/new?labels=enhancement"><b>Request Feature</b></a>
  </p>
</div>

## About The Project

This tool helps identify and censor profanity

It can be used in **any** cases, for example for text censorship, for audio and video censorship, etc.

## ⚙️ Installation

Just run this command in the terminal:

```bash
pip3 install censore
```

## 🚀 Usage

Before you can start working with the text, you **need** to initialize the `Censor` class with the preloaded languages:

```python
from censore import ProfanityFilter

censor = ProfanityFilter(languages=["en", "uk"])
```

If no language was specified, all languages will be loaded by default

### `censor_text`

To censor text, use the `censor_text` method:

```python
censor.censor_text("fuck you")
# #### you
```

It can censor **different languages ​​at the same time**, here is an example:

```python
censor.censor_text("fuck you хуєсос")
# #### you ######
```

> [!TIP]
> The tool also recognizes masked words such as `@ssh0le` (asshole) and censors them

#### `censoring_char` parameter

As you can see, this function replaced the bad word with `#`

You can choose any other character to censor, such as **monkey** 🙈:

```python
censor.censor_text("fuck you", censor_symbol="🙈")
# 🙈🙈🙈🙈 you
```

---

#### `languages` and `additional_languages` parameters

If you have a special case and you need to censor the text in some specific languages ​​other than the preloaded ones, you can specify them in the `languages` parameter:

```python
censor.censor_text("fuck you хуєсос kapullo", languages=["en", "es"])
# **** you хуєсос *******
```

Oh, the Ukrainian word `хуєсос` was **not** censored 😨

We could add Ukrainian to the `languages` parameter, but would you like to enter there every time the standard languages ​​and additional ones that should be used only in this case (in this case Spanish) ?

I think not, then we can just use the `additional_languages` option:

```python
censor.censor_text("fuck you хуєсос kapullo", additional_languages=["es"])
# **** you ****** *******
```

✨ Perfectly! Now, in addition to English and Ukrainian, Spanish will be used in this operation

---

#### `partial_censor` parameter

You can use partial censoring to leave only the first and last letters:

```python
censor.censor("assfucker", partial_censor=True)
# as#####er
```

#### `custom_words` parameter

This parameter allows you to add custom words for censore

Here is an example:

```python
censor.censor_text("fuck you lololo, abc", custom_patterns=["lololo", "abc"])
# #### you ######, ###
```

This can be useful if the tool does not define a word or if you have some specific words

If you do notice any missing word, please make an [**issue**](https://github.com/censor-text/profanity-list/issues/new?labels=new+word) or [**PR**](https://github.com/censor-text/profanity-list/pull/new) with a new word in the [repository with lists of these words](https://github.com/censor-text/profanity-list), we will be **very** grateful 😉

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
