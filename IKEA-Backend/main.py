from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from typing import Dict
import logging

from chains.parse_plsql_chain import ParsePLSQLChain
from chains.generate_documentation_chain import GenerateDocumentationChain
from chains.generate_codebase_summary_chain import GenerateCodebaseSummaryChain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LangChain PL/SQL Analyzer",
    description="An API for reverse-engineering PL/SQL codebases using LangChain.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# In-memory storage for tasks
tasks: Dict[str, Dict] = {}

class AnalysisRequest(BaseModel):
    codebase_path: str

class Task(BaseModel):
    task_id: str
    status: str
    details: str

def run_analysis_pipeline(task_id: str, codebase_path: str):
    """
    The main analysis pipeline that runs in the background.
    """
    try:
        logger.info(f"Starting analysis for task {task_id}...")
        tasks[task_id]["status"] = "parsing"
        tasks[task_id]["details"] = "Parsing PL/SQL files..."
        
        # 1. Parse PL/SQL files
        parse_chain = ParsePLSQLChain()
        structured_docs = parse_chain.run(codebase_path)
        
        logger.info(f"Task {task_id}: Parsing complete. Generating documentation...")
        tasks[task_id]["status"] = "generating_docs"
        tasks[task_id]["details"] = "Generating file-level documentation..."
        
        # 2. Generate file-level documentation
        doc_chain = GenerateDocumentationChain()
        documentation = doc_chain.run(structured_docs)
        
        logger.info(f"Task {task_id}: Documentation complete. Generating summary...")
        tasks[task_id]["status"] = "generating_summary"
        tasks[task_id]["details"] = "Generating codebase summary..."
        
        # 3. Generate codebase summary
        summary_chain = GenerateCodebaseSummaryChain()
        summary = summary_chain.run(codebase_path)
        
        logger.info(f"Task {task_id}: Analysis complete.")
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["details"] = "Analysis successfully completed."
        tasks[task_id]["results"] = {
            "documentation": documentation,
            "summary": summary
        }
        
    except Exception as e:
        logger.error(f"Error during analysis for task {task_id}: {e}", exc_info=True)
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["details"] = f"An error occurred: {e}"


@app.post("/analyze", response_model=Task, status_code=202)
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Starts a new analysis task for a given codebase path.
    """
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending", "details": "Analysis has been queued."}
    
    background_tasks.add_task(run_analysis_pipeline, task_id, request.codebase_path)
    
    logger.info(f"Task {task_id} created for path: {request.codebase_path}")
    
    return Task(task_id=task_id, status="pending", details="Analysis has been queued.")

@app.get("/status/{task_id}", response_model=Task)
async def get_status(task_id: str):
    """
    Retrieves the status of a specific analysis task.
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(task_id=task_id, **task)

@app.get("/results/{task_id}")
async def get_results(task_id: str):
    """
    Retrieves the results of a completed analysis task.
    """
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.get("status") != "completed":
        raise HTTPException(status_code=400, detail=f"Task is not yet complete. Current status: {task.get('status')}")
    return {"task_id": task_id, "results": task.get("results")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
