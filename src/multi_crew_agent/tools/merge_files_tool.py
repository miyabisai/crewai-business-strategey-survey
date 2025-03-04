from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import glob



class MergeFilesToolInput(BaseModel):
    """
    マージ対象のMarkdownファイルがあるディレクトリのパスを入力として受け取るためのクラス。
    """
    file_path: str = Field(..., description="Markdownファイルが格納されているディレクトリへのパス。")


class MergeFilesTool(BaseTool):
    
    """複数のMarkdownファイルを1つのファイルにマージするツール。"""
    
    name: str = "Merge MD Files Tool"
    description: str = "Merge MD Files Tool"
    input_schema: Type[BaseModel] = MergeFilesToolInput

    def _run(self, input: MergeFilesToolInput):
        
        try:
            file_path = './search'
            output_file_path = './result'
            # globを使用してすべての.mdファイルを見つける
            md_files = glob.glob(os.path.join(file_path, "*.md"))

            if not md_files:
                raise FileNotFoundError(f"No markdown files found in the {file_path} directory.")
            merged_content = ""
            for filepath in md_files:
                with open(filepath, "r") as f:
                    content = f.read()
                    # 見やすくするために2つの改行を追加する
                    merged_content += content + "\n\n"
             # マージされたコンテンツをファイルに保存する
            output_path = os.path.join(output_file_path, "search_result.md") # Changed to use input file_path

            with open(output_path, "w") as f:
                f.write(merged_content)
            return f"{output_path} にファイルを正常にマージして保存しました"

        except Exception as e:
            return f"エラーが発生しました: {e}"