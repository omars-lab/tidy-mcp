#!/usr/bin/env python3
"""
Test script for the MCP server functionality using FastMCP Client.
"""

import asyncio
import sys
from pathlib import Path
import json

# Add the notes_mcp directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "notes_mcp"))

from fastmcp import Client
from server import mcp


async def test_resources(client):
    """Test the resources functionality."""
    print("Testing Resources...")
    
    # List resources
    resources = await client.list_resources()
    print(f"Available resources: {resources}")

    # Test note templates resource
    templates = await client.read_resource("data://note_templates")
    # Handle both direct list and text-wrapped JSON
    if templates and hasattr(templates[0], "text"):
        try:
            template_list = json.loads(templates[0].text)
        except Exception:
            template_list = templates
    else:
        template_list = templates
    print(f"Found {len(template_list)} templates:")
    for template in template_list:
        if isinstance(template, dict):
            print(f"  - {template['name']} ({template['category']})")
        else:
            print(template)
    print()


async def test_tools(client):
    """Test the tools functionality."""
    print("Testing Tools...")
    
    # List tools
    tools = await client.list_tools()
    print(f"Available tools: {tools}")

    # Test note analysis tool
    test_content = "Meeting notes: Discuss project timeline. TODO: Follow up with team. Action items: Review proposal by Friday."
    request = {
        "content": test_content,
        "analysis_type": "action_items"
    }
    
    result = await client.call_tool("analyze_note", request)
    print(f"Analysis result: {result['analysis']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Metadata: {result['metadata']}")
    print()


async def test_prompts(client):
    """Test the prompts functionality."""
    print("Testing Prompts...")
    
    # List prompts
    prompts = await client.list_prompts()
    print(f"Available prompts: {prompts}")

    # Test note generation prompt
    request = {
        "topic": "Weekly Planning",
        "style": "bullet_points",
        "length": "medium"
    }
    
    result = await client.call_prompt("generate_note", request)
    print(f"Generated note template:")
    print(result['content'])
    print(f"Template used: {result['template_used']}")
    print()


async def main():
    """Run all tests using FastMCP Client."""
    print("MCP Server Test Suite (Client)")
    print("=" * 50)
    
    try:
        async with Client(mcp) as client:
            await test_resources(client)
            await test_tools(client)
            await test_prompts(client)
        print("✅ All tests passed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 


    