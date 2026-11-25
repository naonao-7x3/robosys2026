# rangefilter

[![test](https://github.com/naonao-7x3/robosys2026/actions/workflows/test.yml/badge.svg)](https://github.com/naonao-7x3/robosys2026/actions/workflows/test.yml)

`rangefilter` は、測定値などの数値データから、指定した許容範囲を外れた値だけを取り出すコマンドです。センサーの測定ログから異常値の候補を抽出するときなどに利用できます。

## 必要な環境

- Linux
- Python 3.10 以上

追加のPythonライブラリは必要ありません。

## インストール

ターミナルで次のコマンドを実行します。

```console
$ git clone https://github.com/naonao-7x3/robosys2026.git
$ cd robosys2026
```

## 使い方

次の形式で実行します。

```console
$ ./rangefilter 下限 上限
```

測定値は標準入力から渡します。範囲の下限と上限は引数で指定してください。範囲の端の値は範囲内として扱い、範囲外の値だけを標準出力へ1行ずつ表示します。

例えば、測定値が `12.5`、`15.0`、`8.4` の場合、許容範囲を `10` から `20` にすると、`8.4` だけが出力されます。

```console
$ printf '12.5\n15.0\n8.4\n' | ./rangefilter 10 20
8.4
```

複数の値は空白またはカンマで区切れます。行内の `#` 以降はコメントとして無視します。

```console
$ printf '10, 12, 25 # sensor A\n15\n' | ./rangefilter 10 20
25
```

他のコマンドと組み合わせることもできます。

```console
$ seq -2 12 | ./rangefilter 0 10
-2
11
12
```

## 入力とエラー

- 数値以外の文字や `nan`、`inf` などの値が入力された場合は、エラーメッセージを標準エラー出力へ表示して終了します。
- 下限または上限が数値でない場合、下限が上限より大きい場合もエラーになります。
- 数値が1つもない入力は、正常終了して何も出力しません。
- 正常終了時の標準出力には、範囲外の数値だけが出力されます。

終了ステータスは、正常終了が `0`、入力値のエラーが `1`、引数のエラーが `2` です。

## テスト

次のコマンドでテストを実行できます。

```console
$ python3 -m unittest discover -s tests -v
```

GitHub Actionsでは、pushおよびpull request時にUbuntu環境でPython 3.10〜3.14のテストを実行します。

## ライセンス

BSD 3-Clause Licenseで公開しています。詳細は [LICENSE](LICENSE) を参照してください。

Copyright 2026 Naomi Miura
