import base64
import re
from pathlib import Path

def get_notes(notes_dir_str="notes"):
    """notesディレクトリ内のMarkdownファイルを取得してソートする"""
    notes_dir = Path(notes_dir_str)
    if not notes_dir.exists():
        return []
    files = sorted(list(notes_dir.glob("*.md")))
    return files

def render_links(content):
    """リンクを同じタブで開くHTMLに変換する便利関数"""
    pattern = r'\[(.*?)\]\(\/\?note=(.*?)\)'
    replacement = r'<a href="/?note=\2" target="_self" style="text-decoration:underline;">\1</a>'
    return re.sub(pattern, replacement, content)

def embed_images_base64(content, base_path):
    """Markdown内のローカル画像をBase64に変換して埋め込む"""
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        if not image_path.startswith(('http://', 'https://')):
            full_path = base_path / image_path
            if full_path.exists():
                try:
                    with open(full_path, "rb") as img_file:
                        b64_string = base64.b64encode(img_file.read()).decode()
                        ext = full_path.suffix.lower().replace('.', '')
                        mime_type = f"image/{ext}"
                        if ext == 'svg':
                            mime_type = "image/svg+xml"
                        return f'<img src="data:{mime_type};base64,{b64_string}" alt="{alt_text}" style="max-width: 60%; display: block; margin: 10px auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                except Exception as e:
                    return f'[画像読み込みエラー: {e}]'
        return match.group(0)

    pattern = r'!\[(.*?)\]\((.*?)\)'
    content = re.sub(pattern, replace_image, content)
    return content

def format_math_text(text):
    """
    数式と思われるテキスト（LaTeXコマンド含む）を$で囲む。
    すでに$で囲まれている部分は変更しない。
    """
    if not text:
        return ""
    
    # 簡易的なヒューリスティック: 
    # \frac, \sum, \int, _, ^ などが含まれていて、かつ $ がない場合に $...$ で囲む
    # (より厳密なパースは複雑になるため、CBT用としてはこの程度で実用十分と想定)
    
    latex_triggers = [r'\\frac', r'\\sum', r'\\int', r'\\times', r'\\lambda', r'\\mu', r'\\sigma', r'E\[', r'V\[']
    
    # すでに$が含まれていれば、製作者が意図してフォーマットしているとみなして何もしない
    if '$' in text:
        return text
        
    # 日本語が含まれている場合は、文章全体を数式化すると表示崩れ（コードブロック化など）の原因になるため何もしない
    # ひらがな、カタカナ、漢字の範囲
    if re.search(r'[ぁ-んァ-ン一-龥]', text):
        return text

    for trigger in latex_triggers:
        if re.search(trigger, text):
            return f"$ {text} $"
            
    return text
