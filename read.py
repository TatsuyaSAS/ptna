file = open(
    "dics/random.txt",          # ソースファイルと同じフォルダーにある
                                        # discフォルダーのrandom.txtを開く
    "r",                                # 読み取りモード
    encoding = "utf_8"          # テキストファイルのエンコーディング方式を指定
)
data = file.read()              # ファイル終端までのすべてのデータを取得
file.close()                        # ファイルオブジェクトをクローズ
lines = data.split("\n")        # 改行で区切った文字列リストを取得
for line in lines:                  # リストから要素を1つずつ取り出す
    print(line)
