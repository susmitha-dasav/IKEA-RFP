from langchain.tools import BaseTool
from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class SummaryInfererTool(BaseTool):
    name: str = "SummaryInfererTool"
    description: str = "Generates a high-level summary of PL/SQL code."

    def _run(self, code_content: str) -> str:
        """Generates a summary of the given PL/SQL code."""
        
        model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
        llm = ChatBedrock(
            credentials_profile_name="381492050009_LZ-Account-Users-AWS", # Use your AWS credentials profile
            model_id=model_id, 
            region_name="us-east-1"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at understanding and summarizing complex code. Your task is to provide a high-level summary of the given PL/SQL code. Focus on the overall purpose and business logic, not on the technical details."),
            ("human", """Please analyze the following PL/SQL code and provide a concise summary of its purpose and logic:

```sql
{code}
```

The summary should be easy for a non-technical stakeholder to understand.""")
        ])
        
        chain = prompt | llm | StrOutputParser()
        
        return chain.invoke({"code": code_content})

    async def _arun(self, code_content: str) -> str:
        return self._run(code_content)
