# An Picat Extention for IPython and Jupyter Notebook

## Prerequisites
* [Picat](http://www.picat-lang.org)
* [Jupyter Notebook](http://jupyter.readthedocs.org/en/latest/install.html)


## Instalation via pip
```text
pip install jupyter
pip install ipicat
```

Add `--user` to install in your private environment.


## Use
Inside a Jupyter Notebook with Python3 kernel, in a first cell, load the extension:
```text
%load_ext ipicat
```

In other cell write a complete Picat program. It is important to note that the execution starts with the `main` predicate:
```text
%%picat

main =>
    println('Teste'),
    X = 1+1,
    println(X).
```

You can execute a Picat script that is in the same directory that the notebook:
```text
%picat -e t.pi
```

