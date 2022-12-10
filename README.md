# Read Me

This repo is a minimal reproduction of a bug in [sphinx-graph] that causes links nested inside 'vertex' directives to break.

## Steps to Reproduce

```
cd docs
poetry run make html
```

then open `docs/_build/index.html` in a browser.

Observe that glossary links and 'ref' links work fine outside of the 'vertex' directives, but don't work when they're nested inside a directive.

Why????
