import streamlit as st
import time
from utils.quiz_generator import QuizGenerator
from utils.display import format_math_text

def run_quiz_mode():
    """CBT実践演習モード"""
    # Header Card
    with st.container(border=True):
        st.markdown("## 💪 実践CBT演習")
        st.markdown("本番形式の計算・理解問題に挑戦します。")

    generator = QuizGenerator()
    chapters = generator.get_available_chapters()
    
    if not chapters:
        st.warning("問題データが見つかりません。")
        return

    # 全範囲オプションを追加
    all_chapters_label = "全範囲 (All Chapters)"
    chapter_options = [all_chapters_label] + chapters

    selected_option = st.selectbox("学習する章を選んでください", chapter_options)
    
    # 選択が変更されたらリセット
    if 'current_chapter_option' not in st.session_state or st.session_state.current_chapter_option != selected_option:
        st.session_state.current_chapter_option = selected_option
        
        # 全範囲か特定章かを判定
        target_chapters = None
        if selected_option != all_chapters_label:
            target_chapters = [selected_option]
            
        st.session_state.quiz_questions = generator.get_random_questions(count=5, chapter_ids=target_chapters)
        st.session_state.current_question_idx = 0
        st.session_state.score = 0
        st.session_state.quiz_state = "question"
        st.session_state.last_is_correct = False
        st.session_state.user_choice = None
        st.session_state.history = [] # 履歴の初期化
        st.session_state.question_start_time = None # タイマー初期化

    if not st.session_state.quiz_questions:
        st.info("この章にはまだ問題がありません。")
        return

    total_q = len(st.session_state.quiz_questions)
    
    # 終了判定
    if st.session_state.current_question_idx >= total_q:
        st.balloons()
        score_percent = (st.session_state.score / total_q) * 100
        
        # タイマー統計
        total_time = sum([log.get('duration', 0) for log in st.session_state.history])
        avg_time = total_time / total_q if total_q > 0 else 0
        
        result_title = "Finish!"
        result_msg = ""
        result_color = ""
        
        if score_percent == 100:
            result_title = "🏆 Perfect!!"
            result_msg = "素晴らしい理解度です！"
            result_color = "#d4edda"
        elif score_percent >= 80:
            result_title = "👏 Good Job!"
            result_msg = "合格圏内です！"
            result_color = "#e2e3e5"
        else:
            result_title = "💪 Keep Going!"
            result_msg = "復習してもう一度挑戦しましょう。"
            result_color = "#f8d7da"

        with st.container(border=True):
            st.markdown(f"""
            <div style="text-align: center; background-color: {result_color}; padding: 20px; border-radius: 8px;">
                <h1 style="font-size: 3em; margin-bottom: 0;">{st.session_state.score} / {total_q}</h1>
                <p>正解数</p>
                <h2>{result_title}</h2>
                <p>{result_msg}</p>
                <div style="margin-top: 15px; font-size: 0.9em; color: #555;">
                    <p>🕒 総解答時間: <b>{total_time:.1f}秒</b> （平均: {avg_time:.1f}秒/問）</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # --- 振り返りエリア ---
        st.markdown("### 📝 振り返り")
        if 'history' in st.session_state and st.session_state.history:
            for i, log in enumerate(st.session_state.history):
                status_icon = "✅" if log['is_correct'] else "❌"
                duration_str = f"{log.get('duration', 0):.1f}s"
                expander_label = f"Q{i+1}: {status_icon} (⏱️ {duration_str}) - あなたの回答: {log['user_choice']}"
                
                with st.expander(expander_label, expanded=not log['is_correct']):
                    st.markdown(f"**問題**: {format_math_text(log['question'])}")
                    if not log['is_correct']:
                        st.markdown(f"**正解**: {log['correct_answer']}")
                        st.markdown(f"**解説**:")
                        st.markdown(format_math_text(log['explanation']))
                    else:
                        st.caption("正解です！")

        # --- アクションボタン ---
        col1, col2 = st.columns(2)
        
        # 間違えた問題のみリトライ
        incorrect_indices = [i for i, log in enumerate(st.session_state.history) if not log['is_correct']]
        
        if incorrect_indices:
            with col1:
                if st.button("❌ 間違えた問題のみリトライ", type="primary", use_container_width=True):
                    # 間違えた問題だけを抽出してセット
                    incorrect_questions = [st.session_state.quiz_questions[i] for i in incorrect_indices]
                    st.session_state.quiz_questions = incorrect_questions
                    
                    # 状態リセット
                    st.session_state.current_question_idx = 0
                    st.session_state.score = 0
                    st.session_state.history = []
                    st.session_state.question_start_time = None
                    st.session_state.quiz_state = "question"
                    st.rerun()
        
        with col2:
            if st.button("🔄 新しい問題に挑戦", use_container_width=True):
                del st.session_state['current_chapter_option']
                st.rerun()
        return

    # 現在の問題
    q_data = st.session_state.quiz_questions[st.session_state.current_question_idx]
    q_idx = st.session_state.current_question_idx

    # Initialize timer for current question
    if st.session_state.quiz_state == "question" and st.session_state.question_start_time is None:
        st.session_state.question_start_time = time.time()

    # プログレス
    progress = q_idx / total_q
    st.progress(progress, text=f"Question {q_idx + 1} / {total_q}")

    # 問題表示エリア
    with st.container(border=True):
        # 問題文とメタデータ
        q_type = q_data.get('type', 'general')
        type_map = {'calculation': '🧮 計算問題', 'conceptual': '💡 概念理解'}
        badge = type_map.get(q_type, q_type)
        
        st.caption(f"ジャンル: {badge}")
        st.markdown(f"### Q{q_idx + 1}.")
        
        question_text = format_math_text(q_data['question'])
        st.markdown(question_text) # Native Markdown rendering for LaTeX support

    # 選択肢の数式処理
    formatted_options = [format_math_text(opt) for opt in q_data['options']]

    if st.session_state.quiz_state == "question":
        with st.form(key=f"quiz_form_{q_idx}"):
            choice = st.radio("選択肢:", formatted_options, index=None)
            submit_btn = st.form_submit_button("回答する", use_container_width=True)
        
        if submit_btn:
            if choice:
                # Calculate duration
                end_time = time.time()
                start_time = st.session_state.question_start_time if st.session_state.question_start_time else end_time
                duration = end_time - start_time
                
                raw_choice_idx = formatted_options.index(choice)
                formatted_answer = format_math_text(q_data['answer'])
                is_correct = (choice == formatted_answer)
                
                # データを保存
                manager = DataManager()
                manager.add_quiz_result(is_correct)
                
                st.session_state.last_is_correct = is_correct
                if is_correct:
                    st.session_state.score += 1
                
                # 履歴保存
                if 'history' not in st.session_state:
                    st.session_state.history = []
                
                st.session_state.history.append({
                    "question": q_data['question'],
                    "user_choice": choice,
                    "correct_answer": formatted_answer,
                    "is_correct": is_correct,
                    "explanation": q_data.get('explanation', ''),
                    "duration": duration
                })
                
                st.session_state.user_choice = choice
                
                # タイマーリセットと状態更新
                st.session_state.question_start_time = None
                st.session_state.quiz_state = "result"
                st.rerun()
            else:
                st.warning("選択肢を選んでください。")
    
    elif st.session_state.quiz_state == "result":
        # タイマーリセット（念のため）
        st.session_state.question_start_time = None
        
        # 結果表示
        is_correct = st.session_state.last_is_correct
        result_class = "result-correct" if is_correct else "result-incorrect"
        result_text = "正解！ 🙆‍♂️" if is_correct else "不正解... 🙅‍♂️"
        
        st.markdown(f'<div class="result-box {result_class}">{result_text}</div>', unsafe_allow_html=True)
        
        # 直前の回答の時間を表示
        if st.session_state.history:
            last_duration = st.session_state.history[-1].get('duration', 0)
            st.caption(f"⏱️ 解答時間: {last_duration:.1f}秒")
        
        st.write(f"あなたの回答: **{st.session_state.user_choice}**")
        if not is_correct:
            formatted_ans = format_math_text(q_data['answer'])
            st.write(f"正解は: **{formatted_ans}**")

        # 解説エリア
        exp_text = format_math_text(q_data.get('explanation', ''))
        with st.container(border=True):
            st.markdown("#### 📝 解説")
            st.markdown(exp_text)
            
        if st.button("次の問題へ", type="primary", use_container_width=True):
            st.session_state.current_question_idx += 1
            st.session_state.quiz_state = "question"
            st.rerun()
