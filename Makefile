default:
	python generator.py -t template.html.jinja -v variation_config.json sample.csv variation.csv

y8:
	python generator.py -t template8.html.jinja -c y8.css -v variation_config.json sample.csv variation.csv

multipage_sample:
	# 8 + 7 にファイルを分割
	# 9 なのはヘッダ分
	split -l 9 -d long_sample.csv sensei_message-
	# ２番めに１番目のヘッダをくっつける
	head -n 1 sensei_message-00 | cat - sensei_message-01 | sponge sensei_message-01
	# 2回出力
	# メッセージを8個単位で一時ファイルに書き出して，それぞれで生成して，suffixで区別を付ける
	# メッセージの個数がはっきりしているのでベタうち
	cat sensei_message-00 | python generator.py -t template8.html.jinja -v variation_config.json -c y8.css -S "-1" variation.csv
	cat sensei_message-01 | python generator.py -t template8.html.jinja -v variation_config.json -c y8.css -S "-2" variation.csv

clean:
	rm *.html
