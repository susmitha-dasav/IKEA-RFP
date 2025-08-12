from tools.summary_inferer_tool import SummaryInfererTool
from tools.code_loader_tool import CodeLoaderTool

class GenerateCodebaseSummaryChain:
    def run(self, directory_path: str) -> str:
        code_loader = CodeLoaderTool()
        summary_inferer = SummaryInfererTool()

        loaded_files = code_loader.run(directory_path)
        
        summaries = []
        for file_info in loaded_files:
            summary = summary_inferer.run(file_info["content"])
            summaries.append(f"## Summary for {file_info['file_path']}\n\n{summary}")
            
        return "\n\n".join(summaries)

