from tools.code_loader_tool import CodeLoaderTool
from tools.plsql_structure_extractor_tool import PLSQLStructureExtractorTool

class ParsePLSQLChain:
    def run(self, directory_path: str):
        code_loader = CodeLoaderTool()
        structure_extractor = PLSQLStructureExtractorTool()

        loaded_files = code_loader.run(directory_path)
        
        structured_docs = []
        for file_info in loaded_files:
            # Here, we assume the tool can be run directly.
            # In a more complex scenario, you might use an agent or a more complex chain.
            structure = structure_extractor.run(file_info["content"])
            structured_docs.append({
                "file_path": file_info["file_path"],
                "structure": structure
            })
            
        return structured_docs
