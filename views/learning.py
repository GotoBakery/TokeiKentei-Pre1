import streamlit as st
import re
from pathlib import Path
from utils.display import render_links, embed_images_base64
from streamlit_mermaid import st_mermaid

def run_learning_mode(notes):
    """学習ノート閲覧モード"""
    st.header("📖 学習ノート閲覧")
    st.caption("知識の定着を確認しましょう。")
    
    if not notes:
        st.error("notesディレクトリにファイルがありません。")
        return

    note_names = [f.stem for f in notes]
    query_params = st.query_params
    url_note = query_params.get("note", None)

    default_index = 0
    if url_note and url_note in note_names:
        default_index = note_names.index(url_note)

    selected_note_name = st.sidebar.radio(
        "学習項目を選択",
        note_names,
        index=default_index
    )

    if selected_note_name != url_note:
        st.query_params["note"] = selected_note_name

    if selected_note_name:
        selected_file = next((f for f in notes if f.stem == selected_note_name), None)
        
        if selected_file:
            with open(selected_file, "r", encoding="utf-8") as f:
                raw_content = f.read()
            
            content = render_links(raw_content)
            content = embed_images_base64(content, Path("notes"))

            # シンプルなMarkdown表示
            st.markdown(f"# {selected_note_name}")
            st.markdown("---")
            
            # Mermaid対応のための分割レンダリング
            parts = re.split(r'```mermaid\n(.*?)\n```', content, flags=re.DOTALL)
            
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # 通常のMarkdownテキスト
                    if part: # 空文字列でなければ表示
                         st.markdown(part, unsafe_allow_html=True)
                else:
                    # Mermaidブロック
                    # st_mermaidはデフォルトで高さが自動ではないため、必要に応じて調整
                    st_mermaid(part, height=300)
    
    with st.sidebar:
        st.markdown("---")
        st.caption(f"全 {len(notes)} ページ")
