---
title: Contribute
layout: page
---


It's very easy to contribute to the database of good practices.

# File architecture

The actual content is in the directory `_tips`. Inside you have one directory for each practice. Inside you have a file named `LANGUAGE.md` for each language. You also have a directory named `_LANGUAGE` per language.

```
_tips
└── timing-attack
    ├── _python
    │   ├── app.py
    │   ├── app.pyc
    │   ├── hack.py
    │   ├── requirements.txt
    │   ├── test.py
    │   └── venv
    ├── js.md
    └── python.md
```

# File format

The content markdown file respect this format:

```markdown
---
title: Example of practice
language: Example of language
---

Content starts here.
```

Content is jekyll collection, see [here](https://jekyllrb.com/docs/frontmatter/).

# How to contribute?

If you want to add content or fix content, just do a pull-request and we will try to review it and merge it asap.

# Add a language for an existing practice

If you want to add a new language for an existing practice, you can start by copying an existing language content for you language. Remember to change the language in the frontmatter block but keeps the same title.

Also create a directory for this language if you have example of vulnerable code.

# Add a new existing practice

If you want to add a new practice, create a directory for this practice in `_libs`. In this new repository, copy the template located in `_libs/_template.md` and name it `LANGUAGE.md`. Then add a directory named `_LANGUAGE` if you have vulnerable code to share.
