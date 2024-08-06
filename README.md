# btc
ビットコインの買い時/売り時を計算するスクリプト
# 1.概要
投資の方法で毎日/毎月の間隔で少額ずつ購入するドルコスト平均法があると思います。しかし、購入するだけでなく、たまに売却する日を混ぜれば、最終的な利益が少しだけ増えるのではないかと思いました。そして、今日は買うor売るのどちらかを計算するスクリプトをPythonで書いてみました。
# 2.前提となる環境
以下の環境でスクリプトが動作することを確認できました。
|名前|バージョン| 
|:-----------|------------:|
|OS|Windows11| 
|Python|3.11.9|
|yfinance|0.2.41|
|matplotlib|3.9.1|
# 3.スクリプト
まず、モジュールをインポートします。
```python:モジュールインポート
import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import matplotlib.pyplot as plt
import math
```
Yahoo!ファイナンスのライブラリを利用し、ビットコインのデータを過去5年分取得します。（tickersの値を変えることで、ビットコイン以外にも色々データを取れそうですね）
```python:5年分のデータ取得
#取得するデータをビットコインに指定
tickers=['BTC-JPY']
#取得終了日
end=datetime.date.today()
#取得開始日(5年前)
start= end-relativedelta(years=5)
#データの取得を実行 、結果を`data`に代入
data=yf.download(tickers,start=start,end=end)
print(data_open)
data_open=data['Open']
```
```python:実行結果
[*********************100%%**********************]  1 of 1 completed
                    Open          High          Low        Close    Adj Close         Volume
Date
2019-08-06  1.247252e+06  1.305750e+06  1201471.625  1220457.250  1220457.250  2513086948730
2019-08-07  1.220363e+06  1.273278e+06  1213538.250  1267570.375  1267570.375  2355868749360
2019-08-08  1.268554e+06  1.271016e+06  1225245.625  1267048.375  1267048.375  2062784431110
2019-08-09  1.265621e+06  1.267788e+06  1238607.625  1253619.250  1253619.250  1938083790030
2019-08-10  1.253474e+06  1.259190e+06  1196656.250  1199839.875  1199839.875  1915402225300
...                  ...           ...          ...          ...          ...            ...
2024-08-01  1.010573e+07  1.003280e+07  9681904.000  9679317.000  9679317.000  4687346413992
2024-08-02  9.680305e+06  9.793203e+06  9317203.000  9751151.000  9751151.000  6113434681910
2024-08-03  9.750554e+06  9.762359e+06  8969399.000  9003141.000  9003141.000  6312509077270
2024-08-04  9.003104e+06  9.110641e+06  8771736.000  8895398.000  8895398.000  4654835519247
2024-08-05  8.894812e+06  8.951529e+06  8386817.500  8461222.000  8461222.000  4623764878482

[1827 rows x 6 columns]
```
短期的な売り買いでの利益が目的なので、長期的なトレンドを除去します。ここでは180日(約半年)の移動平均をトレンドと見なすこととし、それを元データから引きます。
```python:トレンド除去
# トレンド除去して残差を算出(180日の移動平均をトレンドとする)
stl_r=(data_open-data_open.rolling(180).mean()).dropna()
```
トレンドを除去した残差を標準化します。これによりデータの大体が-3～3くらいの範囲に収まります。そして、「当日のデータが正なら売りor負なら買い」といったように、どちらのアクションを取ればよいかわかりやすくします。
```python:標準化
#残差を標準化
stl_r_std=(stl_r-stl_r.mean())/stl_r.std(ddof=0)
```
ここまでの結果を折れ線グラフとして画像出力して見ます。(画像の保存先は適当なパスを指定します。)
```python:グラフを画像出力
# グラフを画像出力
plt.figure()
stl_r_std.plot()
plt.savefig(R"C:\Users\XXXX\Desktop\btc\btc.png")
```
グラフは以下のような感じです。(右端がこのスクリプトを書いた2024/8です。暴落して-1くらいになってるので買い時みたいですね)
![btc.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3836959/7a212d2a-f8d5-8c05-50d5-7a2c67d545a0.png)

最後に基準額（その日、取引したい大体の額）に標準化したデータをかけ「XXX円売るor買う」の結果を出力します。
```python:「XXX円売るor買う」の結果
# 今日の購入金額の計算(基準を250円とする)
amount_sale=math.ceil(stl_r_std.iloc[-1]*250)
if amount_sale > 0:
  print(str(amount_sale)+'円売ってください。')
else:
  amount_buy=amount_sale*-1
  print(str(amount_buy)+'円買ってください。')
```
```python:出力
279円買ってください。
```
この結果に従って、毎日「XXX円売るor買う」を繰り返していれば、最終的な利益は多少増えるのではないかと思います。
