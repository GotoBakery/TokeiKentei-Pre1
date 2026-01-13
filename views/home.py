import streamlit as st
import random
from utils.data_manager import DataManager

def run_home_mode():
    """ホーム画面（ダッシュボード）"""
    
    # データマネージャーのインスタンス化（初回ロード時に学習日数更新）
    manager = DataManager()
    stats = manager.get_stats()

    # ヘッダー
    st.markdown("## 👋 Welcome Back!")
    st.caption("統計検定準1級 合格を目指して、今日も学習を進めましょう。")

    # スタッツ表示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 学習日数", f"{stats['learning_days']}日")
    with col2:
        st.metric("✍️ 総回答数", f"{stats['total_questions']}問")
    with col3:
        st.metric("🎯 正答率", f"{stats['accuracy']:.1f}%")

    st.markdown("---")

    # Today's Keyword
    keywords = [
        {"term": "十分統計量", "desc": "未知パラメータの情報を取りこぼさない統計量。情報損失がない。"},
        {"term": "最尤推定量", "desc": "尤度関数を最大化するパラメータの値。一致性や漸近正規性を持つことが多い。"},
        {"term": "フィッシャー情報量", "desc": "パラメータに関する情報の量。分散の下限（クラメール・ラオの不等式）に関係する。"},
        {"term": "検出力 (Power)", "desc": "対立仮説が正しいときに、正しく帰無仮説を棄却できる確率（1-β）。"},
        {"term": "p値", "desc": "帰無仮説のもとで、得られたデータ以上に極端な値が得られる確率。"},
        {"term": "中心極限定理", "desc": "標本サイズが大きくなると、標本平均の分布は正規分布に近づく定理。"},
        {"term": "不偏推定量", "desc": "期待値が真のパラメータ値と一致する推定量。"},
        {"term": "一致推定量", "desc": "サンプルサイズを無限大にすると、真のパラメータ値に確率収束する推定量。"},
        {"term": "マルコフ連鎖", "desc": "将来の状態が現在の状態のみに依存し、過去の状態には依存しない確率過程。"},
        {"term": "ベイズの定理", "desc": "事後確率は尤度と事前確率の積に比例するという定理。"}
    ]
    # 日替わり感演出のため、セッションステートに保存してリロードまで維持するか、毎回ランダムか。
    # ここではシンプルにランダム表示（リロードで変わるのも学習に良い）
    todays_keyword = random.choice(keywords)

    with st.container(border=True):
        st.subheader(f"💡 Today's Keyword: {todays_keyword['term']}")
        st.write(todays_keyword['desc'])
    
    st.markdown("---")
    st.markdown("### 🚀 Start Learning")

    # ナビゲーションカード
    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        with st.container(border=True):
            st.markdown("### 💪 実践CBT演習")
            st.caption("本番形式の問題演習を行います。")
            if st.button("演習を始める", key="nav_quiz", type="primary", use_container_width=True):
                st.session_state.current_mode = "quiz"
                st.rerun()

    with nav_col2:
        with st.container(border=True):
            st.markdown("### 📖 学習ノート閲覧")
            st.caption("重要項目の解説を確認します。")
            if st.button("ノートを開く", key="nav_notes", use_container_width=True):
                st.session_state.current_mode = "learning"
                st.rerun()
