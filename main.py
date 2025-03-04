#!/usr/bin/env python
import os
import shutil
import sys
import warnings
from src.multi_crew_agent.crew import MultiCrewAgent
from datetime import datetime
import streamlit as st
import logging

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def delete_old_files():
    # ディレクトリ内の既存のファイルを削除
    result_dir = "./result"
    knowledge_dir = "./knowledge"

    for dir in [result_dir, knowledge_dir]:
        if os.path.exists(dir):
            for filename in os.listdir(dir):
                file_path = os.path.join(dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
                    st.error(f"クルーの実行中にエラーが発生しました: {e}")
                    st.write(f"Failed to delete {file_path}. Reason: {e}")  
                               
                    
def run(topic: str):
    """
    クルーを実行します。
    """
    inputs = {
        'topic': topic,  # 調査対象の企業名
    }
    try:
        # MultiCrewAgentのインスタンスを作成し、クルーを実行
        result = MultiCrewAgent().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        # エラーが発生した場合、例外をraise
        raise Exception(f"クルーの実行中にエラーが発生しました: {e}")

def main():
    st.title("企業経営戦略調査エージェント")
    topic:str = st.text_input("会社名を入力してください:")
    st.write("レポートダウンロード：")
    btn = st.button("送信")
    try:
        if btn:
            delete_old_files()
            if not topic:
                raise ValueError("会社名を入力してください。")

            result=run(topic)
            if result.raw:
                st.download_button(
                    label="レポートダウンロード",
                    data=result.raw,
                    file_name=f"{topic}_report.md",
                    mime="text/plain"
                )
            else:
                st.warning("レポートが生成されませんでした。")

    except Exception as e:
        print('An error occurred while running the crew: {e}')
        st.error("クルーの実行中にエラーが発生しました: {e}")
        st.write(f"Exception details: {e}")        

if __name__ == "__main__":
    main()