# pygments-acl2

A [Pygments](https://pygments.org/) lexer for [ACL2](https://acl2.org).

## Install

```bash
pip install git+https://github.com/gjurgensen/pygments-acl2
```

This registers the lexer under the name `acl2`:

```bash
pygmentize -l acl2 foo.lisp
```

## Without installing

Copy `pygments_acl2.py` into your project and load it by path:

```bash
pygmentize -x -l pygments_acl2.py:ACL2Lexer foo.lisp
```

## LaTeX (minted)

If installed, use `acl2` as the language:

```latex
\begin{minted}{acl2}
(defun foo (x) x)
\end{minted}
```

Otherwise, use the file directly:

```latex
\begin{minted}{pygments_acl2.py:ACL2Lexer -x}
(defun foo (x) x)
\end{minted}
```

minted 3 additionally restricts both plugins and custom lexer files; see the
[latexminted docs](https://pypi.org/project/latexminted/).

## License

BSD 2-Clause. Derived from the Emacs Lisp lexer distributed with Pygments.
See [LICENSE](LICENSE). The [AUTHORS](AUTHORS) file is copied from the upstream Pygments project.
