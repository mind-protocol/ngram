#!/usr/bin/env python3
"""
Membrane MCP Server

Exposes the connectome/membrane structured dialogue system as MCP tools.

Tools:
  - membrane_start: Start a new membrane dialogue
  - membrane_continue: Continue with an answer
  - membrane_abort: Abort a session

Usage:
  Run as MCP server (stdio):
    python tools/mcp/membrane_server.py

  Configure in Claude Code settings:
    {
      "mcpServers": {
        "membrane": {
          "command": "python",
          "args": ["tools/mcp/membrane_server.py"],
          "cwd": "/path/to/ngram"
        }
      }
    }
"""

import asyncio
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from engine.connectome import ConnectomeRunner
from ngram.agent_graph import AgentGraph, ISSUE_TO_POSTURE, POSTURE_TO_AGENT_ID
from ngram.agent_spawn import spawn_work_agent, spawn_agent_for_issue
from ngram.doctor import run_doctor
from ngram.doctor_types import DoctorConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("membrane")

# =============================================================================
# MCP PROTOCOL IMPLEMENTATION
# =============================================================================

class MembraneServer:
    """MCP Server for Membrane tools."""

    def __init__(self, connectomes_dir: Optional[Path] = None):
        """Initialize server with optional connectomes directory."""
        self.connectomes_dir = connectomes_dir or (project_root / "protocols")
        self.target_dir = project_root

        # Try to get graph connections if available
        try:
            from engine.physics.graph import GraphOps, GraphQueries
            self.graph_ops = GraphOps(graph_name="ngram")
            self.graph_queries = GraphQueries(graph_name="ngram")
            logger.info("Connected to graph database")
        except Exception as e:
            logger.warning(f"No graph connection: {e}")
            self.graph_ops = None
            self.graph_queries = None

        # Initialize agent graph for work agent management
        try:
            self.agent_graph = AgentGraph(graph_name="ngram")
            self.agent_graph.ensure_agents_exist()
            logger.info("Agent graph initialized")
        except Exception as e:
            logger.warning(f"No agent graph: {e}")
            self.agent_graph = AgentGraph(graph_name="ngram")  # Fallback mode

        self.runner = ConnectomeRunner(
            graph_ops=self.graph_ops,
            graph_queries=self.graph_queries,
            connectomes_dir=self.connectomes_dir
        )

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a JSON-RPC request."""
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                result = self._handle_initialize(params)
            elif method == "tools/list":
                result = self._handle_list_tools()
            elif method == "tools/call":
                result = self._handle_call_tool(params)
            else:
                return self._error_response(request_id, -32601, f"Method not found: {method}")

            return self._success_response(request_id, result)
        except Exception as e:
            logger.exception(f"Error handling {method}")
            return self._error_response(request_id, -32000, str(e))

    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "membrane",
                "version": "0.1.0"
            }
        }

    def _handle_list_tools(self) -> Dict[str, Any]:
        """Return list of available tools."""
        return {
            "tools": [
                {
                    "name": "membrane_start",
                    "description": "Start a new membrane dialogue session. Returns the first step.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "membrane": {
                                "type": "string",
                                "description": "Name of the membrane/connectome to run (e.g., 'create_validation', 'document_progress')"
                            },
                            "context": {
                                "type": "object",
                                "description": "Optional initial context values (e.g., {\"actor_id\": \"actor_claude\"})"
                            }
                        },
                        "required": ["membrane"]
                    }
                },
                {
                    "name": "membrane_continue",
                    "description": "Continue a membrane session with an answer to the current step.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID from membrane_start"
                            },
                            "answer": {
                                "description": "Answer for the current step. Type depends on what the step expects."
                            }
                        },
                        "required": ["session_id", "answer"]
                    }
                },
                {
                    "name": "membrane_abort",
                    "description": "Abort a membrane session. No changes will be committed.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID to abort"
                            }
                        },
                        "required": ["session_id"]
                    }
                },
                {
                    "name": "membrane_list",
                    "description": "List available membrane definitions.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "doctor_check",
                    "description": "Run doctor health checks and return issues with assigned agents.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "depth": {
                                "type": "string",
                                "enum": ["links", "docs", "full"],
                                "description": "Check depth: links (fastest), docs, or full"
                            },
                            "path": {
                                "type": "string",
                                "description": "Optional path filter"
                            }
                        }
                    }
                },
                {
                    "name": "agent_list",
                    "description": "List all work agents and their status (ready/running).",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                },
                {
                    "name": "task_list",
                    "description": "List available tasks grouped by objective. Shows pending tasks agents can work on.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "module": {
                                "type": "string",
                                "description": "Filter by module name"
                            },
                            "objective": {
                                "type": "string",
                                "description": "Filter by objective type (documented, synced, maintainable, etc.)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Max tasks to return (default: 20)"
                            }
                        }
                    }
                },
                {
                    "name": "agent_spawn",
                    "description": "Spawn a work agent to fix an issue OR work on a task (narrative node).",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "Narrative node ID for the task (e.g., 'task_fix_physics_sync'). If provided, issue_type/path are ignored."
                            },
                            "issue_type": {
                                "type": "string",
                                "description": "Issue type (e.g., STALE_SYNC, UNDOCUMENTED). Used if task_id not provided."
                            },
                            "path": {
                                "type": "string",
                                "description": "Path of the issue to fix. Used if task_id not provided."
                            },
                            "agent_id": {
                                "type": "string",
                                "description": "Optional: specific agent to use (e.g., agent_witness). Auto-selected if not provided."
                            },
                            "provider": {
                                "type": "string",
                                "enum": ["claude", "gemini", "codex"],
                                "description": "LLM provider to use (default: claude)"
                            }
                        }
                    }
                },
                {
                    "name": "agent_status",
                    "description": "Get or set the status of a specific agent.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "agent_id": {
                                "type": "string",
                                "description": "Agent ID (e.g., agent_witness)"
                            },
                            "set_status": {
                                "type": "string",
                                "enum": ["ready", "running"],
                                "description": "Optional: set the agent status"
                            }
                        },
                        "required": ["agent_id"]
                    }
                }
            ]
        }

    def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a tool call."""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name == "membrane_start":
            return self._tool_start(arguments)
        elif tool_name == "membrane_continue":
            return self._tool_continue(arguments)
        elif tool_name == "membrane_abort":
            return self._tool_abort(arguments)
        elif tool_name == "membrane_list":
            return self._tool_list(arguments)
        elif tool_name == "doctor_check":
            return self._tool_doctor_check(arguments)
        elif tool_name == "agent_list":
            return self._tool_agent_list(arguments)
        elif tool_name == "task_list":
            return self._tool_task_list(arguments)
        elif tool_name == "agent_spawn":
            return self._tool_agent_spawn(arguments)
        elif tool_name == "agent_status":
            return self._tool_agent_status(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def _tool_start(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Start a membrane session."""
        membrane_name = args.get("membrane")
        context = args.get("context", {})

        if not membrane_name:
            return {"content": [{"type": "text", "text": "Error: 'membrane' is required"}]}

        response = self.runner.start(membrane_name, initial_context=context)
        return self._format_response(response)

    def _tool_continue(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Continue a membrane session."""
        session_id = args.get("session_id")
        answer = args.get("answer")

        if not session_id:
            return {"content": [{"type": "text", "text": "Error: 'session_id' is required"}]}

        response = self.runner.continue_session(session_id, answer)
        return self._format_response(response)

    def _tool_abort(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Abort a membrane session."""
        session_id = args.get("session_id")

        if not session_id:
            return {"content": [{"type": "text", "text": "Error: 'session_id' is required"}]}

        response = self.runner.abort(session_id)
        return self._format_response(response)

    def _tool_list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List available membranes."""
        membranes = []
        if self.connectomes_dir and self.connectomes_dir.exists():
            for path in self.connectomes_dir.glob("*.yaml"):
                membranes.append(path.stem)

        text = "Available membranes:\n"
        for m in membranes:
            text += f"  - {m}\n"

        return {"content": [{"type": "text", "text": text}]}

    def _tool_doctor_check(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Run doctor checks and return issues with assigned agents."""
        depth = args.get("depth", "docs")
        path_filter = args.get("path")

        try:
            config = DoctorConfig()
            result = run_doctor(self.target_dir, config)
            # Extract issues from all categories
            issues = []
            for category_issues in result.get("issues", {}).values():
                issues.extend(category_issues)

            # Filter by path if provided
            if path_filter:
                issues = [i for i in issues if path_filter in i.path]

            # Filter by depth
            from ngram.work_core import get_depth_types
            allowed_types = get_depth_types(depth)
            issues = [i for i in issues if i.issue_type in allowed_types]

            if not issues:
                return {"content": [{"type": "text", "text": "No issues found."}]}

            # Get available agents
            available_agents = {a.id: a for a in self.agent_graph.get_available_agents()}

            lines = [f"Found {len(issues)} issues:\n"]
            for idx, issue in enumerate(issues):
                # Determine assigned agent
                posture = ISSUE_TO_POSTURE.get(issue.issue_type, "fixer")
                agent_id = f"agent_{posture}"
                agent_status = "ready" if agent_id in available_agents else "busy"

                lines.append(f"{idx+1}. [{issue.severity.upper()}] {issue.issue_type}")
                lines.append(f"   Path: {issue.path}")
                lines.append(f"   Agent: {agent_id} ({agent_status})")
                lines.append(f"   Message: {issue.message[:80]}...")
                lines.append("")

            lines.append("\nUse agent_spawn to fix an issue.")
            return {"content": [{"type": "text", "text": "\n".join(lines)}]}

        except Exception as e:
            logger.exception("Doctor check failed")
            return {"content": [{"type": "text", "text": f"Error running doctor: {e}"}]}

    def _tool_agent_list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List all agents and their status."""
        agents = self.agent_graph.get_all_agents()

        lines = ["Work Agents:\n"]
        for agent in agents:
            status_icon = "🟢" if agent.status == "ready" else "🔴"
            lines.append(f"  {status_icon} {agent.id} ({agent.posture})")
            lines.append(f"     Status: {agent.status}")
            lines.append(f"     Energy: {agent.energy:.2f}")
            lines.append("")

        # Show posture mappings
        lines.append("\nPosture → Issue Types:")
        posture_issues: Dict[str, List[str]] = {}
        for issue_type, posture in ISSUE_TO_POSTURE.items():
            posture_issues.setdefault(posture, []).append(issue_type)

        for posture, issues in sorted(posture_issues.items()):
            lines.append(f"  {posture}: {', '.join(issues[:3])}{'...' if len(issues) > 3 else ''}")

        return {"content": [{"type": "text", "text": "\n".join(lines)}]}

    def _tool_task_list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List available tasks with linked issues."""
        module_filter = args.get("module")
        objective_filter = args.get("objective")
        limit = args.get("limit", 20)

        if not self.graph_queries:
            return {"content": [{"type": "text", "text": "Error: No graph connection"}]}

        try:
            # Query tasks with their linked issues and objectives
            cypher = """
            MATCH (t:Narrative)
            WHERE t.type = 'task' AND (t.status IS NULL OR t.status <> 'completed')
            OPTIONAL MATCH (t)-[r:relates]->(o:Narrative {type: 'objective'})
            RETURN t.id, t.name, t.task_type, t.module, t.skill, t.status,
                   collect(DISTINCT o.name) as objectives
            ORDER BY t.created_at_s DESC
            LIMIT $limit
            """
            result = self.graph_queries._query(cypher, {"limit": limit * 2})

            if not result:
                return {"content": [{"type": "text", "text": "No tasks found. Run `doctor` first to create tasks."}]}

            # Filter and format
            lines = ["Available Tasks:\n"]
            count = 0

            for row in result:
                task_id, name, task_type, module, skill, status, objectives = row

                # Apply filters
                if module_filter and module != module_filter:
                    continue
                if objective_filter and objective_filter not in str(objectives):
                    continue

                count += 1
                if count > limit:
                    break

                status_icon = "⏳" if status == "pending" else "🔄" if status == "in_progress" else "⏸️"
                lines.append(f"{status_icon} {name}")
                lines.append(f"   ID: {task_id}")
                lines.append(f"   Module: {module} | Skill: {skill}")
                if objectives:
                    lines.append(f"   Serves: {', '.join(objectives[:2])}")
                lines.append("")

            # Query issue count per task
            lines.append(f"\nTotal: {count} task(s)")
            lines.append("\nTo spawn an agent for a task:")
            lines.append("  agent_spawn(task_id='<task_id>')")

            return {"content": [{"type": "text", "text": "\n".join(lines)}]}

        except Exception as e:
            logger.exception("Task list failed")
            return {"content": [{"type": "text", "text": f"Error listing tasks: {e}"}]}

    def _tool_agent_spawn(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Spawn a work agent to fix an issue or work on a task. Actually executes the agent."""
        task_id = args.get("task_id")
        issue_type = args.get("issue_type")
        path = args.get("path")
        agent_id = args.get("agent_id")
        provider = args.get("provider", "claude")

        task_content = None
        task_type = None
        prompt = None

        # If task_id provided, fetch from graph with full context
        if task_id:
            if self.graph_queries:
                try:
                    # Query task with linked issues and objectives
                    cypher = """
                    MATCH (t:Narrative {id: $task_id})
                    OPTIONAL MATCH (t)-[:relates]->(o:Narrative {type: 'objective'})
                    OPTIONAL MATCH (i:Narrative {type: 'issue'})-[:relates]->(t)
                    RETURN t.id, t.name, t.content, t.type, t.module, t.skill, t.task_type,
                           collect(DISTINCT {id: o.id, name: o.name, type: o.objective_type}) as objectives,
                           collect(DISTINCT {id: i.id, type: i.issue_type, path: i.path, message: i.message, severity: i.severity}) as issues
                    """
                    result = self.graph_queries._query(cypher, {"task_id": task_id})
                    if result and len(result) > 0:
                        row = result[0]
                        task_name = row[1] if len(row) > 1 else task_id
                        task_content = row[2] if len(row) > 2 else None
                        task_type = row[3] if len(row) > 3 else "task"
                        task_module = row[4] if len(row) > 4 else ""
                        task_skill = row[5] if len(row) > 5 else ""
                        task_subtype = row[6] if len(row) > 6 else ""
                        objectives = row[7] if len(row) > 7 else []
                        issues = row[8] if len(row) > 8 else []

                        # Derive issue_type from first issue or task_type
                        if not issue_type and issues:
                            first_issue = issues[0] if isinstance(issues[0], dict) else {}
                            issue_type = first_issue.get("type", "TASK")
                        elif not issue_type:
                            issue_type = task_subtype.upper() if task_subtype else "TASK"

                        # Build rich prompt with full context
                        prompt_lines = [
                            f"# Task: {task_name}",
                            f"Module: {task_module}",
                            f"Skill: {task_skill}",
                            "",
                        ]

                        if objectives:
                            prompt_lines.append("## Objectives this serves:")
                            for obj in objectives[:3]:
                                if isinstance(obj, dict) and obj.get("name"):
                                    prompt_lines.append(f"- {obj.get('name')}")
                            prompt_lines.append("")

                        if issues:
                            prompt_lines.append("## Issues to fix:")
                            for issue in issues[:10]:  # Limit to 10 issues
                                if isinstance(issue, dict) and issue.get("path"):
                                    prompt_lines.append(f"- [{issue.get('severity', 'warning')}] {issue.get('type')}: {issue.get('path')}")
                                    if issue.get("message"):
                                        prompt_lines.append(f"  {issue.get('message')[:200]}")
                            prompt_lines.append("")

                        if task_content:
                            prompt_lines.append("## Task description:")
                            prompt_lines.append(task_content)

                        prompt_lines.append("\n## Instructions:")
                        prompt_lines.append("Fix all the issues listed above. Follow project conventions.")

                        prompt = "\n".join(prompt_lines)
                    else:
                        return {"content": [{"type": "text", "text": f"Error: Task '{task_id}' not found in graph"}]}
                except Exception as e:
                    logger.warning(f"Failed to fetch task {task_id}: {e}")
                    return {"content": [{"type": "text", "text": f"Error fetching task: {e}"}]}
            else:
                return {"content": [{"type": "text", "text": "Error: No graph connection for task lookup"}]}
        elif not issue_type or not path:
            return {"content": [{"type": "text", "text": "Error: Either task_id OR (issue_type + path) required"}]}

        # Select agent if not specified
        if not agent_id:
            posture = ISSUE_TO_POSTURE.get(issue_type, "fixer") if issue_type else "fixer"
            agent_id = f"agent_{posture}"

        # Check if agent is available
        agents = {a.id: a for a in self.agent_graph.get_all_agents()}
        if agent_id in agents and agents[agent_id].status == "running":
            return {"content": [{"type": "text", "text": f"Error: {agent_id} is already running. Choose another agent or wait."}]}

        posture = agent_id.replace("agent_", "")

        # Upsert issue/task narratives before linking
        issue_ids = None
        if issue_type and path:
            # Create/update issue narrative in graph
            issue_narrative_id = self.agent_graph.upsert_issue_narrative(
                issue_type=issue_type,
                path=path,
                message=f"Doctor issue: {issue_type} at {path}",
                severity="warning",
            )
            if issue_narrative_id:
                issue_ids = [issue_narrative_id]

            # Build prompt for issue-based spawn
            if not prompt:
                prompt = f"""Fix the doctor issue:
Issue Type: {issue_type}
Path: {path}

Please investigate and fix this issue. Follow the project's coding standards and documentation patterns."""

        # Use task_id for assignment, or create from issue
        assignment_task_id = task_id
        if not assignment_task_id and issue_type:
            # Create task narrative for this fix
            assignment_task_id = self.agent_graph.upsert_task_narrative(
                task_type=f"FIX_{issue_type}",
                content=f"Fix {issue_type} at {path}",
                name=f"Fix {issue_type}",
            )

        # Actually spawn and run the agent
        try:
            spawn_result = asyncio.get_event_loop().run_until_complete(
                spawn_work_agent(
                    agent_id=agent_id,
                    prompt=prompt,
                    target_dir=self.target_dir,
                    agent_provider=provider,
                    timeout=300.0,
                    use_continue=True,
                    task_id=assignment_task_id,
                    issue_ids=issue_ids,
                )
            )

            # Build response
            if task_id:
                lines = [
                    f"Agent Execution Complete (Task):",
                    f"  Agent: {agent_id}",
                    f"  Posture: {posture}",
                    f"  Task ID: {task_id}",
                    f"  Provider: {provider}",
                    f"  Success: {spawn_result.success}",
                    f"  Duration: {spawn_result.duration_seconds:.1f}s",
                ]
            else:
                lines = [
                    f"Agent Execution Complete (Issue):",
                    f"  Agent: {agent_id}",
                    f"  Posture: {posture}",
                    f"  Issue: {issue_type}",
                    f"  Path: {path}",
                    f"  Provider: {provider}",
                    f"  Success: {spawn_result.success}",
                    f"  Duration: {spawn_result.duration_seconds:.1f}s",
                ]

            if spawn_result.assignment_moment_id:
                lines.append(f"  Moment: {spawn_result.assignment_moment_id}")

            if spawn_result.retried_without_continue:
                lines.append(f"  Note: Retried without --continue")

            if spawn_result.error:
                lines.append(f"  Error: {spawn_result.error[:200]}")

            if spawn_result.output:
                lines.extend([
                    "",
                    "Agent Output:",
                    spawn_result.output[:1000] + ("..." if len(spawn_result.output) > 1000 else ""),
                ])

            return {"content": [{"type": "text", "text": "\n".join(lines)}]}

        except Exception as e:
            logger.exception("Agent spawn failed")
            return {"content": [{"type": "text", "text": f"Error executing agent: {e}"}]}

    def _tool_agent_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get or set agent status."""
        agent_id = args.get("agent_id")
        set_status = args.get("set_status")

        if not agent_id:
            return {"content": [{"type": "text", "text": "Error: agent_id is required"}]}

        if set_status:
            if set_status == "running":
                self.agent_graph.set_agent_running(agent_id)
            else:
                self.agent_graph.set_agent_ready(agent_id)
            return {"content": [{"type": "text", "text": f"Agent {agent_id} status set to {set_status}"}]}

        # Get current status
        agents = {a.id: a for a in self.agent_graph.get_all_agents()}
        if agent_id not in agents:
            return {"content": [{"type": "text", "text": f"Agent {agent_id} not found"}]}

        agent = agents[agent_id]
        lines = [
            f"Agent: {agent.id}",
            f"Posture: {agent.posture}",
            f"Status: {agent.status}",
            f"Energy: {agent.energy:.2f}",
            f"Weight: {agent.weight:.2f}",
        ]
        return {"content": [{"type": "text", "text": "\n".join(lines)}]}

    def _format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Format runner response as MCP tool result."""
        status = response.get("status", "unknown")

        lines = [f"Status: {status}"]

        if response.get("error"):
            lines.append(f"Error: {response['error']}")

        if response.get("session_id"):
            lines.append(f"Session: {response['session_id']}")

        step = response.get("step", {})
        if step:
            step_type = step.get("type", "")
            lines.append(f"Step Type: {step_type}")

            if step.get("question"):
                lines.append(f"\nQuestion: {step['question']}")

            if step.get("expects"):
                expects = step["expects"]
                lines.append(f"Expects: {expects.get('type', 'string')}")
                if expects.get("options"):
                    lines.append(f"Options: {expects['options']}")
                if expects.get("min_length"):
                    lines.append(f"Min Length: {expects['min_length']}")
                if expects.get("min") is not None:
                    lines.append(f"Min Items: {expects['min']}")

            if step.get("results"):
                lines.append(f"\nQuery Results: {len(step['results'])} items")
                for r in step["results"][:5]:
                    lines.append(f"  - {r}")

        if status == "complete":
            created = response.get("created", {})
            nodes = created.get("nodes", [])
            links = created.get("links", [])

            lines.append(f"\nCreated: {len(nodes)} nodes, {len(links)} links")

            if nodes:
                lines.append("\nNodes:")
                for n in nodes:
                    lines.append(f"  - [{n.get('type')}] {n.get('id')}")

            if links:
                lines.append("\nLinks:")
                for l in links:
                    lines.append(f"  - {l.get('type')}: {l.get('from')} -> {l.get('to')}")

        text = "\n".join(lines)
        return {"content": [{"type": "text", "text": text}]}

    def _success_response(self, request_id: Any, result: Any) -> Dict[str, Any]:
        """Build success response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }

    def _error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Build error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }


def main():
    """Run the MCP server on stdio."""
    server = MembraneServer()
    logger.info("Membrane MCP server started")

    # Read JSON-RPC messages from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
            response = server.handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {e}"
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()
