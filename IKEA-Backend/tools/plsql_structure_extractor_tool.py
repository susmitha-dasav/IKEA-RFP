from langchain.tools import BaseTool
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class PLSQLStructureExtractorTool(BaseTool):
    name: str = "PLSQLStructureExtractorTool"
    description: str = "Extracts the structure (packages, procedures, functions, triggers) from PL/SQL code."

    def _run(self, code_content: str) -> str:
        """Extracts the structure from the given PL/SQL code."""
        
        # As per the reference implementation
        model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
        llm = ChatBedrock(
            # credentials_profile_name is best configured in the environment
            credentials_profile_name="381492050009_LZ-Account-Users-AWS", # Use your AWS credentials profile
            model_id=model_id, 
            region_name="us-east-1" # As per reference
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at analyzing PL/SQL code. Your task is to identify and list all major components in the provided code. Extract the names of all packages, procedures, functions, and triggers. Pay attention to dependencies between them. Format the output clearly in Markdown."),
            ("human", """Please analyze the following PL/SQL code and extract its structure:

```sql
{code}
```

Identify the following:
- Packages
- Procedures (both standalone and within packages)
- Functions (both standalone and within packages)
- Triggers
- Dependencies (e.g., procedure X calls function Y)

Present the result in a structured Markdown format.""")
        ])
        
        chain = prompt | llm | StrOutputParser()
        
        return chain.invoke({"code": code_content})

    async def _arun(self, code_content: str) -> str:
        # This would require an async version of the chain invocation
        # For now, we call the sync version
        return self._run(code_content)
