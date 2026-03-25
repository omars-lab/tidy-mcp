"""
HTTP server wrapper for tidy-mcp MCP tools.

This module exposes MCP tools as HTTP endpoints so they can be called
from other services over HTTP.
"""

import logging
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .noteplan import derive_xcallback_url_from_noteplan_file

logger = logging.getLogger(__name__)

app = FastAPI(title="Tidy MCP HTTP Server", version="0.1.0")


class DeriveXCallbackURLRequest(BaseModel):
    file_path: str
    heading: Optional[str] = None


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "tidy-mcp"}


@app.post("/tools/derive_xcallback_url_from_noteplan_file")
async def derive_xcallback_url(request: DeriveXCallbackURLRequest):
    """
    Derive an x-callback-url link from a NotePlan file path.
    
    This endpoint wraps the derive_xcallback_url_from_noteplan_file tool
    to make it accessible via HTTP.
    """
    try:
        result = derive_xcallback_url_from_noteplan_file(
            file_path=request.file_path,
            heading=request.heading
        )
        return result
    except Exception as e:
        logger.error(f"Error in derive_xcallback_url_from_noteplan_file: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

