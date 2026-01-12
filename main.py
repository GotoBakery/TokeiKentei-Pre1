import streamlit as st
import os
from pathlib import Path
import base64
import re

def get_notes():
    """notesディレクトリ内のMarkdownファイルを取得してソートする"""
    notes_dir = Path("notes")
    if not notes_dir.exists():
        return []
    files = sorted(list(notes_dir.glob("*.md")))
    return files

def render_links(content):
    """リンクを同じタブで開くHTMLに変換する便利関数"""
    # [表示名](/?note=ファイル名) -> <a href...>
    pattern = r'\[(.*?)\]\(\/\?note=(.*?)\)'
    replacement = r'<a href="/?note=\2" target="_self" style="text-decoration:underline;">\1</a>'
    return re.sub(pattern, replacement, content)

def embed_images_base64(content, base_path):
    """Markdown内のローカル画像をBase64に変換して埋め込む"""
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        # ローカルファイルパスかどうか簡易チェック（http等で始まらない）
        if not image_path.startswith(('http://', 'https://')):
            # base_path (notesディレクトリ) からの相対パスとして解決
            full_path = base_path / image_path
            if full_path.exists():
                try:
                    with open(full_path, "rb") as img_file:
                        b64_string = base64.b64encode(img_file.read()).decode()
                        # 拡張子からMIMEタイプを推定
                        ext = full_path.suffix.lower().replace('.', '')
                        
                        # Fix for SVG extension mapping if needed (though usually svg works)
                        mime_type = f"image/{ext}"
                        if ext == 'svg':
                            mime_type = "image/svg+xml"
                        
                        # User requested smaller images (approx 60%)
                        # Center alignment
                        return f'<img src="data:{mime_type};base64,{b64_string}" alt="{alt_text}" style="max-width: 60%; display: block; margin: 10px auto;">'
                except Exception as e:
                    return f'[画像読み込みエラー: {e}]'
        
        return match.group(0) # そのまま返す

    # ![alt](path) の形式を置換
    pattern = r'!\[(.*?)\]\((.*?)\)'
    content = re.sub(pattern, replace_image, content)
    return content

def main():
    st.set_page_config(page_title="統計検定準一級 ノート", layout="wide")
    
    # --- 追加コード開始: 太字(strongタグ)のデザインを上書き ---
    st.markdown("""
    <style>
    /* 太字をより太く、少し目立つ色にする */
    strong {
        font-weight: 900 !important; /* 最大級に太く */
        color: gold;             /* ダークモードなのでゴールド */
        /* background-color: #333;  /* 背景色をつけることも可能 */
    }
    </style>
    """, unsafe_allow_html=True)
    # --- 追加コード終了 ---
    st.title("📊 統計検定準一級 学習ノート")

    notes = get_notes()
    if not notes:
        st.error("notesディレクトリにファイルがありません。")
        return

    # 拡張子なしのファイル名リスト
    note_names = [f.stem for f in notes]

    # --- ナビゲーション処理 ---
    
    # 1. URLから指定されたノート名を取得
    query_params = st.query_params
    url_note = query_params.get("note", None)

    # 2. 初期選択位置(index)を決定
    # URLの指定がリストにあればそこを、なければ先頭(0)を
    default_index = 0
    if url_note and url_note in note_names:
        default_index = note_names.index(url_note)

    # 3. サイドバー表示 (indexを指定して描画)
    selected_note_name = st.sidebar.radio(
        "学習項目",
        note_names,
        index=default_index
    )

    # 4. サイドバーを手動で変えたらURLも更新しておく
    # (次回のリロードやブックマーク用)
    if selected_note_name != url_note:
        st.query_params["note"] = selected_note_name

    # ------------------------

    # コンテンツ表示
    if selected_note_name:
        # 名前から元のファイルパスを逆引き
        selected_file = next((f for f in notes if f.stem == selected_note_name), None)
        
        if selected_file:
            with open(selected_file, "r", encoding="utf-8") as f:
                raw_content = f.read()
            
            # リンク変換
            content = render_links(raw_content)
            # 画像埋め込み (notesディレクトリを基準とする)
            content = embed_images_base64(content, Path("notes"))

            st.header(selected_note_name)
            st.markdown("---")
            st.markdown(content, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("---")
        st.caption(f"全 {len(notes)} ページ")

if __name__ == "__main__":
    main()