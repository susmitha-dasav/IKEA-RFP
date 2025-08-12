import os
from typing import List
from langchain.tools import BaseTool

class CodeLoaderTool(BaseTool):
    name: str = "CodeLoaderTool"
    description: str = "Loads the content of .sql, .pks, and .pkb files from a specified directory."

    def _run(self, directory_path: str) -> List[dict]:
        """Loads the code from the specified directory."""
        loaded_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith((".sql", ".pks", ".pkb")):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    loaded_files.append({"file_path": file_path, "content": content})
        return loaded_files

    async def _arun(self, directory_path: str) -> List[dict]:
        # For now, we don't have a true async implementation
        return self._run(directory_path)
