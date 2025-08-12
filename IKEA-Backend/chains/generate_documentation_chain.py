from tools.markdown_formatter_tool import MarkdownFormatterTool

class GenerateDocumentationChain:
    def run(self, structured_docs: list) -> str:
        formatter = MarkdownFormatterTool()
        
        full_documentation = ""
        for doc in structured_docs:
            full_documentation += f"# File: {doc['file_path']}\n\n"
            full_documentation += formatter.run(doc['structure'])
            full_documentation += "\n\n---\n\n"
            
        return full_documentation
