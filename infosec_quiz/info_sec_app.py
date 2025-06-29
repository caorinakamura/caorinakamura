import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 日本語フォント設定（Windows用）
plt.rcParams['font.family'] = 'MS Gothic'

st.title("クイズ・情報セキュリティ")
st.markdown("以下の質問に答えてください。")

CSV_FILE = 'qa_data.csv'  # 保存するCSVファイル名
df = pd.read_csv(CSV_FILE)

#選択肢リスト
choices = ["はい", "いいえ", "わからない"]

# モード選択
mode = st.sidebar.radio("モードを選択", ["問題を作成する", "クイズに挑戦する"])

# ========================
# 問題を作成するモード
# ========================
if mode == "問題を作成する":
    st.title("社内教育Q&A登録モード")

    with st.form("qa_form"):
        question = st.text_input("質問", placeholder="例：パスワードは定期的に変更すべき？")
        answer = st.selectbox("正解", choices)  # 選択式にする
        submitted = st.form_submit_button("登録する")

        if submitted and question and answer:
            new_data = pd.DataFrame([{"質問": question, "回答": answer}])

            if os.path.exists(CSV_FILE):
                existing = pd.read_csv(CSV_FILE)
                updated = pd.concat([existing, new_data], ignore_index=True)
            else:
                updated = new_data

            updated.to_csv(CSV_FILE, index=False, encoding='utf-8-sig')
            st.success("Q&Aを登録しました！")

# ========================
# クイズに挑戦するモード
# ========================
elif mode == "クイズに挑戦する":
    st.title("社内教育クイズ")

    if not os.path.exists(CSV_FILE):
        st.warning("まだ登録された問題がありません。先に『問題を作成する』から追加してください。")
    else:
        df = pd.read_csv(CSV_FILE)
        user_answers = []

        with st.form("quiz_form"):
            for idx, row in df.iterrows():
                q = row["質問"]
                correct = row["回答"]
                user_choice = st.radio(f"{idx+1}. {q}", choices, key=f"q{idx}")
                user_answers.append((correct, user_choice))

            submitted = st.form_submit_button("採点する")

        # 採点結果表示
if submitted:
    correct_count = 0
    incorrect_count = 0
    unknown_count = 0

    st.subheader("📝 採点結果")

    for i, (correct_ans, user_ans) in enumerate(user_answers):
        if user_ans == "わからない":
            st.warning(f"Q{i+1}：わからない（正解：{correct_ans}）")
            unknown_count += 1
        elif user_ans == correct_ans:
            st.success(f"Q{i+1}：正解！")
            correct_count += 1
        else:
            st.error(f"Q{i+1}：不正解（正解：{correct_ans}）")
            incorrect_count += 1

    # 結果の集計
    total = len(user_answers)
    st.write(f"正解：{correct_count} / {total}")
    st.write(f"不正解：{incorrect_count}")
    st.write(f"わからない：{unknown_count}")

    # 結果を円グラフに
    labels = ["正解", "不正解", "わからない"]
    sizes = [correct_count, incorrect_count, unknown_count]
    colors = ["green", "red", "gray"]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors)
    ax.set_title("回答の内訳")
    ax.axis('equal')
    st.pyplot(fig)