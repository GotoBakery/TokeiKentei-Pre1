PREMIUM_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Roboto:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Roboto', 'Noto Sans JP', sans-serif;
    }
    
    /* ヘッダーなどはStreamlitのテーマに従うが、カード内は別途黒文字を強制する */

    /* カードデザイン：Streamlit純正container(border=True)をカスタマイズ */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        padding: 24px !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 24px;
    }
    
    /* カード内の文字色を黒に強制 (Dark Mode対策) */
    div[data-testid="stVerticalBlockBorderWrapper"] * {
        color: #333333 !important;
    }

    /* ボタン */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* アクセントカラー */
    .highlight {
        color: #d4af37;
        font-weight: bold;
    }
    
    /* 正解・不正解表示 */
    .result-box {
        padding: 16px;
        border-radius: 8px;
        margin-top: 16px;
        font-weight: bold;
        text-align: center;
        color: #333 !important; /* 結果ボックス内の文字色も強制 */
    }
    .result-correct {
        background-color: #d4edda;
        color: #155724 !important;
        border: 1px solid #c3e6cb;
    }
    .result-incorrect {
        background-color: #f8d7da;
        color: #721c24 !important;
        border: 1px solid #f5c6cb;
    }

    /* Markdown内の数式フォント調整 */
    .katex {
        font-size: 1.1em !important;
    }
    
    /* 学習ノート用：太字をGoldにする（元のスタイル復元） */
    strong {
        font-weight: 900 !important;
        color: #d4af37;
    }
</style>
"""
