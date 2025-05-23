import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import os
import datetime

st.set_page_config(layout="wide")
st.title("セレン・マーケットモニター：IVクラッシュと債券トリガー可視化アプリ")

st.markdown("### リアルタイムチャート")

col1, col2 = st.columns(2)

# TLT Chart
with col1:
    st.subheader("米長期債ETF - TLT")
    tlt_widget = '''
    <div class="tradingview-widget-container">
      <div id="tradingview_tlt"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "width": "100%",
        "height": 400,
        "symbol": "NASDAQ:TLT",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "1",
        "locale": "ja",
        "toolbar_bg": "#f1f3f6",
        "container_id": "tradingview_tlt"
      });
      </script>
    </div>
    '''
    components.html(tlt_widget, height=430)

# USDJPY Chart
with col2:
    st.subheader("為替 - USD/JPY")
    usd_widget = '''
    <div class="tradingview-widget-container">
      <div id="tradingview_usdjpy"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({
        "width": "100%",
        "height": 400,
        "symbol": "FX:USDJPY",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "1",
        "locale": "ja",
        "toolbar_bg": "#f1f3f6",
        "container_id": "tradingview_usdjpy"
      });
      </script>
    </div>
    '''
    components.html(usd_widget, height=430)

st.markdown("---")

# =====================
# データ取得
# =====================

# USDJPY 取得
usdjpy = yf.Ticker("JPY=X").history(period="1d")
latest_usdjpy = float(usdjpy['Close'].iloc[-1])

# Nikkei225 現値と前日比
nikkei_hist = yf.Ticker("^N225").history(period="2d")
nikkei_today = float(nikkei_hist['Close'].iloc[-1])
nikkei_prev  = float(nikkei_hist['Close'].iloc[-2])
nikkei_change_pct = (nikkei_today - nikkei_prev) / nikkei_prev * 100

# JPVIX 取得トライ（なければ None）
try:
    jpvix = yf.Ticker("JPVIX").history(period="1d")
    latest_vix = float(jpvix['Close'].iloc[-1])
except Exception:
    latest_vix = None

# =====================
# アラートセクション
# =====================

st.markdown("### 🔔 トリガーアラート")

# 1) C44000 売り発動通知
if nikkei_today > 37500:
    st.warning(f"【要アクション】日経先物想定値が 37,500 を超過（指数終値 {nikkei_today:,.0f}） → 8月C44000 を1枚ショート検討！")
else:
    st.info(f"日経225 : {nikkei_today:,.0f}（終値基準 37,500 未満）")

# 2) プット利確通知
if latest_vix is not None:
    if latest_vix < 22:
        st.warning(f"【IVクラッシュ注意】日経VI 推定値 {latest_vix:.1f} < 22 → プット利確を検討！")
    else:
        st.success(f"日経VI 推定値 : {latest_vix:.1f}（22 以上／保有継続）")
else:
    st.info("日経VI データが取得できませんでした。手動でご確認ください。")

# 3) 再ヘッジ通知
if (latest_usdjpy < 140) and (nikkei_change_pct <= -2):
    st.error(f"【ヘッジ提案】USDJPY {latest_usdjpy:.2f} < 140 かつ 日経▲{abs(nikkei_change_pct):.1f}% → プット買い戻しを検討！")
else:
    st.success(f"USDJPY : {latest_usdjpy:.2f} ／ 日経変動 {nikkei_change_pct:+.2f}%")

st.markdown("---")

# Option logic placeholder
st.markdown("### ロングプット利確判定（参考メッセージ）")
vega_high = True
iv_decline_expected = latest_vix is not None and latest_vix < 22
if vega_high and not iv_decline_expected:
    st.info("現在はIVの高止まり状態です。Vegaの残高がある場合はまだ利確せずに継続保有することで、利益強化の可能性があります。")
elif vega_high and iv_decline_expected:
    st.warning("IVの低下が予想されます。Vegaによる利益の剥離が起こる前に、段階的な利確を検討してください。")
else:
    st.success("Vega効果は限定的です。デルタに注目した利確戦略への移行をおすすめします。")

# Stop button
st.markdown("---")
if st.button("アプリを停止"):
    os._exit(0)
