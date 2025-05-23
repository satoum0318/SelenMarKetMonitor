import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import os

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

# Alert logic: USDJPY under 139
st.markdown("### トリガーアラート")
usdjpy = yf.Ticker("JPY=X").history(period="1d")
latest_usdjpy = usdjpy['Close'].iloc[-1]
if latest_usdjpy < 139:
    st.error(f"警告：USD/JPY が 139 を割りました → {latest_usdjpy:.2f}")
else:
    st.success(f"USD/JPY 現在値：{latest_usdjpy:.2f}（正常範囲内）")

st.markdown("---")

# Option logic placeholder
st.markdown("### ロングプット利確判定")
vega_high = True
iv_decline_expected = False
if vega_high and not iv_decline_expected:
    st.info("現在はIVの高止まり状態です。Vegaの残高がある場合はまだ利確せずに継続保有することで、利益強化の可能性があります。")
elif vega_high and iv_decline_expected:
    st.warning("IVの低下が予想されます。Vegaによる利益の剥離が起こる前に、段階的な利確を検討してください。")
else:
    st.success("Vega効果は限定的です。デルタに注目した利確戦略への移行をおすすめします。")

# Stop button to allow shutdown
st.markdown("---")
if st.button("アプリを停止"):
    os._exit(0)
