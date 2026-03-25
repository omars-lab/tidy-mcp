"""
Tools for interacting with the local knowledge-agents API container.

This module provides MCP tools to call the knowledge-agents API running
in local Docker containers with proper API key authentication.
"""

import os
from pathlib import Path
from typing import Annotated, Dict, Any, Optional
from pydantic import Field
import requests


def _get_api_key(api_key_path: Optional[str] = None) -> str:
    """
    Get API key from file or environment variable.
    
    Priority order:
    1. Explicit api_key_path parameter
    2. KNOWLEDGE_AGENTS_API_KEY environment variable
    3. Default path: ../knowledge-agents/secrets/openai_api_key.txt
    4. Default path: ~/Workspace/git/knowledge-agents/secrets/openai_api_key.txt
    
    Args:
        api_key_path: Optional explicit path to API key file
        
    Returns:
        API key string
        
    Raises:
        FileNotFoundError: If API key file cannot be found
        ValueError: If API key is empty
    """
    # Try explicit path first
    if api_key_path:
        key_path = Path(api_key_path)
        if key_path.exists():
            with open(key_path, 'r') as f:
                key = f.read().strip()
                if key:
                    return key
            raise ValueError(f"API key file {api_key_path} is empty")
        raise FileNotFoundError(f"API key file not found: {api_key_path}")
    
    # Try environment variable
    env_key = os.environ.get("KNOWLEDGE_AGENTS_API_KEY")
    if env_key:
        return env_key.strip()
    
    # Try default paths
    default_paths = [
        Path(__file__).parent.parent.parent.parent / "knowledge-agents" / "secrets" / "openai_api_key.txt",
        Path.home() / "Workspace" / "git" / "knowledge-agents" / "secrets" / "openai_api_key.txt",
    ]
    
    for key_path in default_paths:
        if key_path.exists():
            with open(key_path, 'r') as f:
                key = f.read().strip()
                if key:
                    return key
    
    raise FileNotFoundError(
        f"API key not found. Please set KNOWLEDGE_AGENTS_API_KEY environment variable "
        f"or ensure API key file exists at one of: {[str(p) for p in default_paths]}"
    )


def _get_api_base_url(base_url: Optional[str] = None) -> str:
    """
    Get API base URL from parameter or environment variable.
    
    Args:
        base_url: Optional explicit base URL
        
    Returns:
        API base URL string
    """
    if base_url:
        return base_url.rstrip('/')
    
    env_url = os.environ.get("KNOWLEDGE_AGENTS_API_URL")
    if env_url:
        return env_url.rstrip('/')
    
    # Default to localhost:8001 (mapped from container port 8000)
    return "http://localhost:8001"


def tool_query_notes(
    question: Annotated[str, Field(description="The question to ask about your notes")],
    api_key: Annotated[
        Optional[str], 
        Field(description="API key for authentication. If not provided, will try to read from file or environment variable.")
    ] = None,
    api_key_path: Annotated[
        Optional[str],
        Field(description="Path to API key file. If not provided, will use default locations.")
    ] = None,
    base_url: Annotated[
        Optional[str],
        Field(description="Base URL for the knowledge-agents API. Defaults to http://localhost:8001")
    ] = None,
) -> Dict[str, Any]:
    """
    Query your notes using the local knowledge-agents API.
    
    This tool calls the knowledge-agents API running in a local Docker container
    to answer questions about your notes using semantic search and AI.
    
    Returns:
        Dictionary containing the query response with answer, relevant files, and metadata.
    """
    try:
        # Get API key
        if api_key:
            token = api_key.strip()
        else:
            token = _get_api_key(api_key_path)
        
        # Get base URL
        url = _get_api_base_url(base_url)
        endpoint = f"{url}/api/v1/notes/query"
        
        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        payload = {
            "query": question
        }
        
        # Make request
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=60  # Allow time for AI processing
        )
        
        # Check response
        response.raise_for_status()
        result = response.json()
        
        return {
            "success": True,
            "request_id": result.get("request_id"),
            "answer": result.get("answer"),
            "relevant_files": result.get("relevant_files", []),
            "query_answered": result.get("query_answered", False),
            "reasoning": result.get("reasoning"),
            "guardrails_tripped": result.get("guardrails_tripped", []),
        }
        
    except FileNotFoundError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "api_key_not_found"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "api_request_failed",
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "unknown_error"
        }


def tool_check_api_health(
    base_url: Annotated[
        Optional[str],
        Field(description="Base URL for the knowledge-agents API. Defaults to http://localhost:8001")
    ] = None,
) -> Dict[str, Any]:
    """
    Check the health status of the local knowledge-agents API.
    
    This tool calls the health check endpoint to verify the API is running
    and accessible.
    
    Returns:
        Dictionary containing health status information.
    """
    try:
        # Get base URL
        url = _get_api_base_url(base_url)
        endpoint = f"{url}/health"
        
        # Make request
        response = requests.get(endpoint, timeout=10)
        
        # Check response
        response.raise_for_status()
        result = response.json()
        
        return {
            "success": True,
            "status": result.get("status"),
            "version": result.get("version"),
            "api_url": endpoint
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "api_request_failed",
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
            "api_url": endpoint if 'endpoint' in locals() else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "unknown_error"
        }

