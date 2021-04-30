---
title: y manual
author: ryu-raptor
---

yは寄せ書き(yosegaki)を生成するプログラムです．
大量のお祝いのメッセージをきれいにレイアウトすることができます．
リモートでの寄せ書き制作に便利です．

# サンプル
<a href="sample/BASIC8.pdf"><img src="sample/BASIC8_thumbnail.png" /></a>
<a href="sample/BASIC.pdf"><img src="sample/BASIC_thumbnail.png" /></a>

# かんたんな使い方
同梱されている`Makefile`を利用して，

```
$ make
```

とすればカレントディレクトリに`BASIC.html`, `COBOL.html`, `i386 asm.html`が生成されます．
それぞれをお好きなブラウザで開き，必要の応じてpdfプリンタで印刷すれば完成です．

```
使い方: generator.py [-h] [-t TEMPLATE] [-v VARIATION_CONFIG] [-S SUFFIX] [-c CSS_VARIANT] [-V VARIATION_INDEX] [-i VARIATION_INDICES]
                    [-s VARIATION_SEQUENCE] [-l LIMIT]
                    [csv_file] variation_file

positional arguments:
  csv_file              入力するCSVファイル．指定しない場合はstdinから読みます．
  variation_file        枠の画像の一覧を定義したファイル．

optional arguments:
  -h, --help            このメッセージを表示して終了
  -t TEMPLATE, --template TEMPLATE
                        jinja2のhtmlテンプレートファイル（基本的に同梱されているものを改変して利用ください）
  -v VARIATION_CONFIG, --variation_config VARIATION_CONFIG
                        ランダムに枠を選ぶのではなく，JSONファイルで指定する．
  -S SUFFIX, --suffix SUFFIX
                        出力された色紙のHTMLファイルの名前の末尾に付ける文字を指定する．(-S _helloでname_hello.htmlとなる)
  -c CSS_VARIANT, --css_variant CSS_VARIANT
                        利用するCSSファイルを指定する．さもなくばy.cssが使われる．
  -l LIMIT, --limit LIMIT
                        一つのページあたりに配置するメッセージ数を指定する（使えません）．
```

# 準備
yは突発で作ったため設定がちょっと面倒です．
次の準備を行ってください

- 寄せ書きに用いるフォント
- 1枚に収めるメッセージの数およびレイアウト
- メッセージの含まれたCSVファイル

お好みで次の準備もしてください

- 枠用の画像の用意
- 枠をどう選ぶかの設定

## フォント
デフォルトでは'07やさしさゴシック'が指定されていますが，同梱はしていません．
別途ダウンロードして配置してください．

他のフォントが良い場合はy.cssの`@font-face`セレクタ内の`src: url('./07Yasashisa.ttf');`を当該のフォントを指定するように書き換えてください．
なお，`font-family`はそのままにしても問題ないと思われます．
気になる場合は`body`セレクタ内の`font-family`とともに任意の名前に書き換えてください．

また，CSSですので`body`セレクタ内の`font-family`をいじればシステムにインストールされているフォントを利用できます．

## レイアウト
デフォルト(`y.css`)では10人のメッセージを1枚に収めます．
`y8.css`は8人のメッセージを1枚に収めます．

寄せ書きは30cm四方の紙を想定しています（印刷するサイズに合わせて縮小，フィットページ等をご利用ください）．
また，原則左上から順に埋めていきます．

基本的に`div.wrapper`セレクタの`grid-template-columns`プロパティと`grid-template-rows`をうまく調整します．
たとえば8人のメッセージなら3x3の9ますにして，真ん中に相手の名前を入れるレイアウトが考えられます．
すると，ひとマス10cm x 10cmになりますので，
`grid-template-columns: repeat(3, 10cm);`
`grid-template-rows: 10cm;`
と書き換えます．
`grid-auto-columns`と`grid-auto-rows`についても同様に書き換えるといいです．

参考までに8, 10, 12, 14個の場合のひとマスの大きさを以下の表に示します．

| 個数 | 縦    | 横    |
|------|-------|-------|
| 8    | 10cm  | 10cm  |
| 10   | 10cm  | 7.5cm |
| 12   | 7.5cm | 7.5cm |
| 14   | 6cm   | 7.5cm |

## メッセージファイル
メッセージファイルはCSVの形式で入力します．
次のようなフォーマットで準備してください．

| (空白ます) | 相手1         | 相手2         | 相手3         | ... |
|------------|---------------|---------------|---------------|-----|
| 送り主1    | メッセージ1,1 | メッセージ1,2 | メッセージ1,3 | ... |
| 送り主2    | メッセージ2,1 | メッセージ2,2 | メッセージ2,3 | ... |
| ...        | ...           | ...           | ..            | ... |

サンプル(`sample.csv`)が同梱されていますのでご覧ください．

## 枠の画像
サイズに特に指定はありませんが，現状PNG画像を想定しています．
用意するのは次の3つです．

- メッセージ用の枠（見た目にバリエーションを持たせるために複数個用意することを推奨）
- 贈り相手の名前の枠（メッセージ用の枠とデザインを合わせることを推奨）
- 贈り相手の名前の枠の上下の飾り（`b1.png`（上）と`b1_r.png`（下）である必要がある．`template.html.jinja`のみで利用する．`template8.html.jinja`では利用しない）

3番めの飾りを除いて，ファイル名は自由ですが，拡張子は`.png`である必要があります．

用意した画像を利用するには任意のCSVファイルにファイル名の拡張子を除いたものを記述する必要があります（これをバリエーションファイルと呼びます）．
フォーマットは以下のとおりです．
枠の定義ファイルは，行があるテーマを表し，列がそのテーマのバリエーションといえます．

```
(贈り相手の名前の枠_1),(メッセージ用の枠_1,1),(メッセージ用の枠_1,2),...
(贈り相手の名前の枠_2),(メッセージ用の枠_2,1),(メッセージ用の枠_2,2),...
...
```

なお，各行のコンマの数は揃える必要はありますが，各テーマの画像の数は揃ってないくて良いです．
左詰めでデータを入れてください．つまり，以下のようになります．

```
c1,f1_1,f1_2,f1_3
c2,f2_1,,
c3,f3_1,f3_2,
```

サンプル（`variation.csv`）では1種類のみ定義されています．

同じ画像を使いまわしたい場合は，同じ名前を複数ヶ所に記載してください．

## 枠選択の設定
枠を定義したCSVファイルのどの情報を利用するかをJSONファイルで定義できます．
0スタートであることに注意してください．
以下はサンプルファイルの中身です．

```
{
    "page": [
        {
            "variation": 0,
            "sequence": [ 0 ]
        }
    ]
}
```

`page`プロパティにページごとの設定を記述します．
なお，配列の末尾に付いた場合は先頭に戻るため全員分を定義する必要はありません．
サンプルでは，どの人に宛てても共通のデザインを使うことを定義しています．

`variation`プロパティはバリエーションファイルの行を表しています．ここでは先頭行のテーマを使うということです．
`sequence`プロパティはバリエーションファイルの先頭列を除いた列を表しています．ここでは最初のメッセージ枠を常に使うことを指定しています．

宛先用の枠はページに一つしか存在しないため`variation`で指定できていますのでご注意ください．

# Q&A
## `sensei`ってなに
`Makefile`の`multipage_sample`にある`sensei`には特に意味はありません．
もともと先生に贈る色紙を想定していただけです．

## なぜメッセージはエスケープしないの？
現状各メッセージごとの細かいレイアウト調整をするために，メッセージに直にHTMLを書き込めるようにしているため，代替機能が実装されればエスケープします．

このため，このシステムを不特定多数が利用するサービスには使わないでください．

# ライセンス
テキスト（ソースコード，テンプレート，メッセージ，`README.md`，サンプルHTML等）はMITライセンスで公開します．
`LICENSE`をご覧ください．

サンプル用の枠画像はCC-BY-SA 4.0でライセンスされます．

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="クリエイティブ・コモンズ・ライセンス" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/ryu-raptor/y" property="cc:attributionName" rel="cc:attributionURL">ryu-raptor</a> 作『<span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/StillImage" property="dct:title" rel="dct:type">y sample frame set</span>』は<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">クリエイティブ・コモンズ 表示 - 継承 4.0 国際 ライセンス</a>で提供されています。

追加で画像ファイルが増える場合は適切なライセンスを必ず付与してください．さもなくば，当該ファイルを削除することになります．
