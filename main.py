#!/usr/bin/env python
import os
import shutil
import sys
import warnings
from src.multi_crew_agent.crew import MultiCrewAgent
from datetime import datetime
import streamlit as st

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def delete_old_files():
  
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
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

def create_downloadable_text_file():
    # Sample text content
    text_content = "This is the content of the downloadable text file.\nYou can add multiple lines of text here."
    
    # Create a download button
    st.download_button(
        label="Download Text File",
        data=text_content,
        file_name="downloaded_text.txt",
        mime="text/plain"
    )

def run(topic:str):
    """
    クルーを実行します。
    """
    inputs = {
        'topic': topic,
    }
    try:
        result = MultiCrewAgent().crew().kickoff(inputs=inputs)
        # print(f"Raw Output: {result.raw}")
        return result
    except Exception as e:
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
                    file_name="report.md",
                    mime="text/plain"
                )
            else:
                st.warning("レポートが生成されませんでした。")

    except Exception as e:
        print('An error occurred while running the crew: {e}')
        st.error(str(e))
        exit()
        

if __name__ == "__main__":
    main()