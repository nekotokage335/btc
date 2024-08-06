import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import matplotlib.pyplot as plt
import math

#取得するデータをビットコインに指定
tickers=['BTC-JPY']
#取得終了日
end=datetime.date.today()
#取得開始日(5年前)
start= end-relativedelta(years=5)
#データの取得を実行 、結果を`data`に代入
data=yf.download(tickers,start=start,end=end)
print(data)
data_open=data['Open']

# トレンド除去して残差を算出(180日の移動平均をトレンドとする)
stl_r=(data_open-data_open.rolling(180).mean()).dropna()

#残差を標準化
stl_r_std=(stl_r-stl_r.mean())/stl_r.std(ddof=0)

# グラフを画像出力
plt.figure()
stl_r_std.plot()
plt.savefig(R"C:\Users\XXXX\Desktop\btc\btc.png")

# 今日の購入金額の計算(基準を250円とする)
amount_sale=math.ceil(stl_r_std.iloc[-1]*250)
if amount_sale > 0:
  print(str(amount_sale)+'円売ってください。')
else:
  amount_buy=amount_sale*-1
  print(str(amount_buy)+'円買ってください。')
