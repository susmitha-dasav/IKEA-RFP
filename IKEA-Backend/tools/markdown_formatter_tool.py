from langchain.tools import BaseTool

class MarkdownFormatterTool(BaseTool):
    name: str = "MarkdownFormatterTool"
    description: str = "Formats structured data into Markdown."

    def _run(self, structured_data: str) -> str:
        """Formats the structured data into Markdown."""
        # This tool can be expanded to perform more complex formatting.
        # For now, it will just ensure the input is treated as a string.
        return str(structured_data)

    async def _arun(self, structured_data: str) -> str:
        return self._run(structured_data)
