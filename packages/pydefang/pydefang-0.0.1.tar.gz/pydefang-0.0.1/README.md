# pydefang
A defang/refang utility written in Python.

#### Usage
`pydefang` is installed as two command-line utilities accessible as `defang` and `refang` from the command-line.

You can use it to convert a url to a defanged version (make it safe(r) to share):

```
-$ defang 'https://www.malicious.org/legit.exe'
hxxps[:]//www[.]malicious[.]org/legit[.]exe

```

or if you need to make something a 'real' url again you can refang:
```text
-$ refang 'hxxps[:]//www[.]malicious[.]org/legit[.]exe'
https://www.malicious.org/legit.exe
```

You can also use it programmatically:
```python
In [1]: from defang import defang, refang

In [2]: defang('https://www.malicious.org/legit.exe')
Out[2]: 'hxxps[:]//www[.]malicious[.]org/legit[.]exe'

In [3]: refang('hxxps[:]//www[.]malicious[.]org/legit[.]exe')
Out[3]: 'https://www.malicious.org/legit.exe'

```


#### Bugs
Feel free to report issues, this 'utility' was build out of ease as I got frustrated with manual conversion of timestamps and strings the whole time.