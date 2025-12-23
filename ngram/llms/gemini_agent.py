"""
Gemini LLM agent subprocess for the ngram CLI.

DOCS: docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from google import genai
from dotenv import dotenv_values

def main():
    parser = argparse.ArgumentParser(description="Gemini LLM agent for ngram CLI.")
    parser.add_argument("-p", "--prompt", required=True, help="User prompt.")
    parser.add_argument("--system-prompt", default="", help="System prompt.")
    parser.add_argument("--output-format", default="stream-json", help="Output format (stream-json or text).")
    parser.add_argument("--allowed-tools", help="Comma-separated list of allowed tools.")
    parser.add_argument("--api-key", help="Gemini API key.")
    parser.add_argument("--model-name", default=None, help="Override default Gemini model (e.g., gemini-3-flash-preview).")
    parser.add_argument("--project-dir", default=".", help="Project root directory for tool execution.")

    args = parser.parse_args()

    # Base path for relative path resolution
    project_root = Path(args.project_dir).resolve()

    # Load from .env file
    config = dotenv_values()

    # Get API key
    api_key = args.api_key or config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    google_search_base_url = (
        config.get("NGRAM_GOOGLE_SEARCH_URL")
        or os.getenv("NGRAM_GOOGLE_SEARCH_URL")
        or "https://www.google.com/search"
    )

    if not api_key:
        print(json.dumps({"error": "GEMINI_API_KEY not found. Please set it in a .env file, as an environment variable, or pass it with --api-key."}), flush=True)
        sys.exit(1)

    # Create the genai client with API key
    client = genai.Client(api_key=api_key)

    # --- Tool Definitions ---
    def run_shell_command(command: str, description: str = ""):
        """Execute a bash command in the project directory."""
        try:
            print(json.dumps({"type": "tool_code", "name": "run_shell_command", "args": {"command": command, "description": description}}), flush=True)
            # Execute in project root
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=project_root)
            return {"stdout": result.stdout, "stderr": result.stderr, "exit_code": result.returncode}
        except Exception as e:
            return {"error": str(e)}

    def read_file(file_path: str):
        """Read a file's content."""
        try:
            print(json.dumps({"type": "tool_code", "name": "read_file", "args": {"file_path": file_path}}), flush=True)
            # Resolve relative to project root
            full_path = project_root / file_path
            content = full_path.read_text(encoding="utf-8")
            return {"content": content}
        except Exception as e:
            return {"error": str(e)}

    def list_directory(dir_path: str = "."):
        """List files and directories."""
        try:
            print(json.dumps({"type": "tool_code", "name": "list_directory", "args": {"dir_path": dir_path}}), flush=True)
            # Resolve relative to project root
            full_path = project_root / dir_path
            entries = []
            for entry in sorted(full_path.iterdir()):
                entries.append({"name": entry.name, "type": "dir" if entry.is_dir() else "file"})
            return {"entries": entries, "count": len(entries)}
        except Exception as e:
            return {"error": str(e)}

    def search_file_content(pattern: str, dir_path: str = "."):
        """Search for pattern in files (grep)."""
        try:
            print(json.dumps({"type": "tool_code", "name": "search_file_content", "args": {"pattern": pattern, "dir_path": dir_path}}), flush=True)
            regex = re.compile(pattern)
            matches = []
            # Resolve relative to project root
            search_base = project_root / dir_path
            for root, _, files in os.walk(search_base):
                if ".git" in root or "__pycache__" in root: continue
                for filename in files:
                    p = Path(root) / filename
                    try:
                        content = p.read_text(encoding="utf-8", errors="ignore")
                        for i, line in enumerate(content.splitlines(), 1):
                            if regex.search(line):
                                rel_path = p.relative_to(project_root)
                                matches.append({"path": str(rel_path), "line": i, "text": line.strip()})
                                if len(matches) >= 50: break
                    except: continue
                if len(matches) >= 50: break
            return {"matches": matches, "count": len(matches)}
        except Exception as e:
            return {"error": str(e)}

    def glob_files(pattern: str, dir_path: str = "."):
        """Find files matching glob pattern."""
        try:
            print(json.dumps({"type": "tool_code", "name": "glob", "args": {"pattern": pattern, "dir_path": dir_path}}), flush=True)
            # Resolve relative to project root
            search_base = project_root / dir_path
            p = str(search_base / pattern)
            matches = []
            for match in sorted(glob.glob(p, recursive=True)):
                try:
                    rel_path = Path(match).relative_to(project_root)
                    matches.append(str(rel_path))
                except ValueError:
                    matches.append(match)
            return {"matches": matches, "count": len(matches)}
        except Exception as e:
            return {"error": str(e)}

    def replace_text(file_path: str, old_string: str, new_string: str, instruction: str = ""):
        """Replace text in a file."""
        try:
            print(json.dumps({"type": "tool_code", "name": "replace", "args": {"file_path": file_path, "old_string": old_string, "new_string": new_string, "instruction": instruction}}), flush=True)
            # Resolve relative to project root
            full_path = project_root / file_path
            content = full_path.read_text(encoding="utf-8")
            if old_string not in content:
                return {"error": f"String not found in {file_path}"}
            new_content = content.replace(old_string, new_string)
            full_path.write_text(new_content, encoding="utf-8")
            return {"path": file_path, "success": True}
        except Exception as e:
            return {"error": str(e)}

    def write_file(file_path: str, content: str):
        """Write content to a file."""
        try:
            print(json.dumps({"type": "tool_code", "name": "write_file", "args": {"file_path": file_path, "content": content}}), flush=True)
            # Resolve relative to project root
            full_path = project_root / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            return {"path": file_path, "bytes": len(content)}
        except Exception as e:
            return {"error": str(e)}

    def google_web_search(query: str):
        """Perform a Google search."""
        try:
            print(json.dumps({"type": "tool_code", "name": "google_web_search", "args": {"query": query}}), flush=True)
            url = f"{google_search_base_url}?q={urllib.parse.quote(query)}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = resp.read(100000).decode("utf-8", "ignore")
            links = re.findall(r'href="/url\?q=([^&"]+)', body)
            results = [{"url": urllib.parse.unquote(l)} for l in links if l.startswith("http")][:5]
            return {"results": results}
        except Exception as e:
            return {"error": str(e)}

    def web_fetch(prompt: str):
        """Fetch content from a URL found in the prompt."""
        try:
            print(json.dumps({"type": "tool_code", "name": "web_fetch", "args": {"prompt": prompt}}), flush=True)
            url = re.search(r"https?://\S+", prompt).group(0)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                content = resp.read(100000).decode("utf-8", "ignore")
            return {"url": url, "content": content}
        except Exception as e:
            return {"error": str(e)}

    def codebase_investigator(objective: str):
        """Explore the codebase to understand architecture or find symbols."""
        try:
            print(json.dumps({"type": "tool_code", "name": "codebase_investigator", "args": {"objective": objective}}), flush=True)
            keywords = objective.split()
            results = []
            for root, _, files in os.walk("."):
                if ".git" in root or "__pycache__" in root: continue
                for filename in files:
                    if any(k.lower() in filename.lower() for k in keywords):
                        results.append(str(Path(root) / filename))
                    if len(results) >= 10: break
                if len(results) >= 10: break
            return {"relevant_files": results}
        except Exception as e:
            return {"error": str(e)}

    # Map tool functions for the model
    tools = [
        run_shell_command, read_file, list_directory, search_file_content,
        glob_files, replace_text, write_file, google_web_search, web_fetch,
        codebase_investigator
    ]
    
    tool_map = {t.__name__: t for t in tools}

    # Model configuration
    gemini_model = args.model_name or config.get("GEMINI_MODEL") or os.getenv("GEMINI_MODEL") or "gemini-3-flash-preview"
    
    history = []
    if args.system_prompt:
        history.append({"role": "user", "parts": [{"text": args.system_prompt}]})
        history.append({"role": "model", "parts": [{"text": "OK. I will follow the protocol."}]})

    try:
        # Start chat
        chat = client.chats.create(model=gemini_model, config={"tools": tools}, history=history)
        
        # Send initial message
        response = chat.send_message(args.prompt)

        while True:
            # Process response parts
            for part in response.candidates[0].content.parts:
                if part.text:
                    if args.output_format == "stream-json":
                        print(json.dumps({
                            "type": "assistant",
                            "message": {"content": [{"type": "text", "text": part.text}]}
                        }), flush=True)
                    else:
                        print(part.text, end="", flush=True)
                
                if part.function_call:
                    tc = part.function_call
                    tool_name = tc.name
                    tool_args = tc.args
                    
                    if tool_name in tool_map:
                        result = tool_map[tool_name](**tool_args)
                        
                        if args.output_format == "stream-json":
                            print(json.dumps({"type": "tool_result", "name": tool_name, "result": result}), flush=True)
                        
                        # Send result back to model using correct function_response schema
                        response = chat.send_message(
                            [genai.types.Part.from_function_response(
                                name=tool_name,
                                response=result
                            )]
                        )
                        break 
            else:
                break

        if not args.output_format == "stream-json":
            print() 
            
        sys.exit(0)

    except Exception as e:
        error_msg = str(e)
        # Identify rate limit / quota exceeded errors
        is_rate_limit = any(indicator in error_msg for indicator in ["429", "ResourceExhausted", "Rate limit", "quota", "Quota"])
        
        if args.output_format == "stream-json":
            print(json.dumps({
                "type": "error",
                "code": "RATE_LIMIT_EXCEEDED" if is_rate_limit else "AGENT_ERROR",
                "message": error_msg
            }), flush=True)
        else:
            print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()