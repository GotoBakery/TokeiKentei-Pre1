import json
import random
from pathlib import Path
import streamlit as st

class QuizGenerator:
    def __init__(self, base_path="exercises/questions"):
        self.base_path = Path(base_path)
    
    def get_available_chapters(self):
        """利用可能な問題ファイルの章リストを返す"""
        if not self.base_path.exists():
            return []
        # ファイル名 "15_prob_process.json" -> "15" という章IDを抽出
        files = list(self.base_path.glob("*.json"))
        chapters = sorted(list(set(f.stem.split('_')[0] for f in files)))
        return chapters

    def load_questions(self, chapter_ids=None):
        """指定された章（リスト）の問題を読み込む。Noneなら全章"""
        questions = []
        if not self.base_path.exists():
            return []
            
        files = list(self.base_path.glob("*.json"))
        
        for file_path in files:
            # 章IDフィルタリング
            file_chapter = file_path.stem.split('_')[0]
            if chapter_ids and file_chapter not in chapter_ids:
                continue
                
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        # どのファイルから来たか（章情報）を付与しておくと便利かも
                        for q in data:
                            q['chapter'] = file_chapter
                        questions.extend(data)
            except Exception as e:
                st.error(f"Error loading {file_path}: {e}")
                
        return questions

    def get_random_questions(self, count=10, chapter_ids=None):
        all_questions = self.load_questions(chapter_ids)
        if not all_questions:
            return []
        
        random.shuffle(all_questions)
        return all_questions[:count]
