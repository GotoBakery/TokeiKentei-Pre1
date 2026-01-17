import streamlit as st
from utils.display import get_notes
from utils.styles import PREMIUM_STYLE
from views.home import run_home_mode
from views.learning import run_learning_mode
from views.quiz import run_quiz_mode

def main():
    st.set_page_config(page_title="統計検定準一級 ノート & CBT演習", layout="wide", initial_sidebar_state="expanded")
    st.markdown(PREMIUM_STYLE, unsafe_allow_html=True)
    
    # セッションステートでのモード管理初期化
    if 'current_mode' not in st.session_state:
        # クエリパラメータからモードを取得、なければhome
        query_params = st.query_params
        initial_mode = query_params.get("mode", "home")
        
        # 正規のモードかチェック
        valid_modes = ["home", "quiz", "learning"]
        if initial_mode not in valid_modes:
            initial_mode = "home"
            
        st.session_state.current_mode = initial_mode

    st.sidebar.title("📊 統計検定準一級対策")
    
    # ナビゲーションメニュー
    # buttonだとステートが消えやすいため、radioボタンとsession_stateを同期させる工夫が必要だが、
    # ここではシンプルに「サイドバーでの選択」が「session_state」を上書きする形をとる。
    
    # マッピング: 表示名 -> 内部モード名
    mode_map = {
        "🏠 ホーム": "home",
        "💪 実践CBT演習": "quiz",
        "📖 学習ノート閲覧": "learning"
    }
    # 逆マッピング
    reverse_map = {v: k for k, v in mode_map.items()}
    
    # 現在のモードに対応するインデックスを取得
    current_label = reverse_map.get(st.session_state.current_mode, "🏠 ホーム")
    options = list(mode_map.keys())
    
    try:
        index = options.index(current_label)
    except ValueError:
        index = 0

    selected_label = st.sidebar.radio("メニュー", options, index=index)
    st.sidebar.markdown("---")

    # サイドバーの変更を検知して更新
    selected_mode = mode_map[selected_label]
    if selected_mode != st.session_state.current_mode:
        st.session_state.current_mode = selected_mode
        st.query_params["mode"] = selected_mode
        st.rerun()

    # ルーティング実行
    if st.session_state.current_mode == "home":
        run_home_mode()
    elif st.session_state.current_mode == "quiz":
        run_quiz_mode()
    elif st.session_state.current_mode == "learning":
        notes = get_notes()
        run_learning_mode(notes)

if __name__ == "__main__":
    main()