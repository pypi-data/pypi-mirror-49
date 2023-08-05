# wfdload

## 概要
wavetoneの独自フォーマットであるwfdをpythonで使える形にします。

## インストール
```sh
$ pip install wfdload
```


## 使い方
### スペクトラムステレオ
```python
>>> from wfdload import WFD
>>> w = WFD("filepath")
>>> w.spectrumStereo
```
