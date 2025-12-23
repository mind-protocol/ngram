"use client";

// DOCS: docs/connectome/flow_canvas/IMPLEMENTATION_Connectome_Flow_Canvas_Code_Structure_With_React_Flow_And_Zones.md

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useConnectomeStore } from "../lib/zustand_connectome_state_store_with_atomic_commit_actions";
import {
  CONNECTOME_EDGE_DEFINITIONS,
  CONNECTOME_NODE_DEFINITIONS,
  ConnectomeNodeType,
  ConnectomeZoneId,
} from "../lib/connectome_system_map_node_edge_manifest";
import {
  compute_node_positions,
  compute_zones,
} from "./deterministic_zone_and_node_layout_computation_helpers";
import { dispatch_runtime_command } from "../lib/next_step_gate_and_realtime_playback_runtime_engine";
import type { CallType, TriggerKind } from "../lib/flow_event_schema_and_normalization_contract";

const EDGE_COLOR_MAP: Record<string, string> = {
  graphLink: "#b7410e",
  graphQuery: "#493f64",
  llm: "#2f8a4f",
  moment: "#b8860b",
  code: "#5b6ee1",
};

const NODE_COLOR_MAP: Record<string, string> = {
  Player: "#b8860b",
  UI: "#8d8a80",
  Module: "#a9a9a9",
  GraphQueries: "#b7410e",
  Moment: "#b8860b",
  Agent: "#2f8a4f",
  TickCron: "#6f6a60",
};

const hex_to_rgb = (hex: string) => {
  const clean = hex.replace("#", "");
  const value = parseInt(clean, 16);
  return {
    r: ((value >> 16) & 255) / 255,
    g: ((value >> 8) & 255) / 255,
    b: (value & 255) / 255,
  };
};

const build_shader = (gl: WebGLRenderingContext, type: number, source: string) => {
  const shader = gl.createShader(type);
  if (!shader) {
    throw new Error("Unable to create shader");
  }
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const error = gl.getShaderInfoLog(shader);
    gl.deleteShader(shader);
    throw new Error(error || "Shader compile failed");
  }
  return shader;
};

const build_program = (gl: WebGLRenderingContext, vertex: string, fragment: string) => {
  const vs = build_shader(gl, gl.VERTEX_SHADER, vertex);
  const fs = build_shader(gl, gl.FRAGMENT_SHADER, fragment);
  const program = gl.createProgram();
  if (!program) {
    throw new Error("Unable to create program");
  }
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const error = gl.getProgramInfoLog(program);
    gl.deleteProgram(program);
    throw new Error(error || "Program link failed");
  }
  return program;
};

const CanvasInner = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const labelCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [size, setSize] = useState({ width: 0, height: 0 });
  const [renderTick, setRenderTick] = useState(0);
  const [hoverNodeId, setHoverNodeId] = useState<string | null>(null);

  const activeNodeId = useConnectomeStore(
    (state) => state.active_focus.active_node_id
  );
  const activeEdgeId = useConnectomeStore(
    (state) => state.active_focus.active_edge_id
  );
  const revealedNodeIds = useConnectomeStore((state) => state.revealed_node_ids);
  const revealedEdgeIds = useConnectomeStore((state) => state.revealed_edge_ids);
  const searchResults = useConnectomeStore((state) => state.search_results);

  const zones = useMemo(() => compute_zones(1400), []);

  const nodePositions = useMemo(() => {
    const searchNodes = (searchResults?.nodes ?? []).map((node, index) => ({
      node_id: node.id,
      zone_id: "GRAPH" as ConnectomeZoneId,
      node_type: "Module" as ConnectomeNodeType,
      language: "GRAPH" as const,
      title: node.name ?? node.id,
      file_path: "seed",
      slot: { row: index % 6, col: Math.floor(index / 6) },
    }));
    const mergedNodes = [
      ...CONNECTOME_NODE_DEFINITIONS,
      ...searchNodes.filter(
        (node) =>
          !CONNECTOME_NODE_DEFINITIONS.some(
            (base) => base.node_id === node.node_id
          )
      ),
    ];
    const searchEdges = (searchResults?.links ?? [])
      .filter((edge) => edge.from_id && edge.to_id)
      .map((edge, index) => ({
        edge_id: `search-${edge.type ?? "link"}-${index}`,
        from_node_id: edge.from_id ?? "?",
        to_node_id: edge.to_id ?? "?",
        label: edge.type ?? "LINK",
        trigger: "direct" as TriggerKind,
        call_type: "graphLink" as CallType,
      }));
    const mergedEdges = [...CONNECTOME_EDGE_DEFINITIONS, ...searchEdges];
    return compute_node_positions(mergedNodes, zones, mergedEdges);
  }, [zones, searchResults]);

  const nodePositionMap = useMemo(() => {
    return new Map(nodePositions.map((item) => [item.node_id, item]));
  }, [nodePositions]);

  const searchNodes = useMemo(() => {
    if (!searchResults?.nodes?.length) {
      return [];
    }
    return searchResults.nodes.map((node, index) => ({
      node_id: node.id,
      zone_id: "GRAPH" as ConnectomeZoneId,
      node_type: (node.type?.toLowerCase() === "narrative" ? "Moment" : "Module") as ConnectomeNodeType,
      language: "GRAPH" as const,
      title: node.name ?? node.id,
      file_path: "seed",
      slot: { row: index % 6, col: Math.floor(index / 6) },
    }));
  }, [searchResults]);

  const nodes = useMemo(() => {
    const mergedNodes = new Map(
      CONNECTOME_NODE_DEFINITIONS.map((node) => [node.node_id, node])
    );
    for (const node of searchNodes) {
      mergedNodes.set(node.node_id, node);
    }
    return Array.from(mergedNodes.values())
      .filter((node) => revealedNodeIds.includes(node.node_id))
      .map((node) => {
        const layout = nodePositionMap.get(node.node_id);
        return {
          id: node.node_id,
          title: node.title,
          node_type: node.node_type,
          x: layout?.x ?? 0,
          y: layout?.y ?? 0,
          energy: node.energy_value ?? 0.4,
        };
      });
  }, [nodePositionMap, revealedNodeIds, searchNodes]);

  const edges = useMemo(() => {
    const searchEdges = (searchResults?.links ?? [])
      .filter((edge) => edge.from_id && edge.to_id)
      .map((edge, index) => ({
        edge_id: `search-${edge.type ?? "link"}-${index}`,
        from_node_id: edge.from_id ?? "?",
        to_node_id: edge.to_id ?? "?",
        label: edge.type ?? "LINK",
        trigger: "direct" as TriggerKind,
        call_type: "graphLink" as CallType,
      }));
    const mergedEdges = [...CONNECTOME_EDGE_DEFINITIONS, ...searchEdges];
    return mergedEdges
      .filter((edge) => revealedEdgeIds.includes(edge.edge_id))
      .filter((edge) => nodePositionMap.has(edge.from_node_id) && nodePositionMap.has(edge.to_node_id))
      .map((edge) => ({
        id: edge.edge_id,
        from: edge.from_node_id,
        to: edge.to_node_id,
        call_type: edge.call_type,
        active: edge.edge_id === activeEdgeId,
      }));
  }, [activeEdgeId, nodePositionMap, revealedEdgeIds, searchResults]);

  const transformRef = useRef({ x: 0, y: 0, scale: 1 });
  const nodesRef = useRef(nodes);

  useEffect(() => {
    nodesRef.current = nodes;
  }, [nodes]);

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const rect = entry.contentRect;
        setSize({ width: rect.width, height: rect.height });
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    const labels = labelCanvasRef.current;
    if (!canvas || !labels) {
      return;
    }
    canvas.width = size.width;
    canvas.height = size.height;
    labels.width = size.width;
    labels.height = size.height;
  }, [size]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }
    const gl = canvas.getContext("webgl", { antialias: true, alpha: true });
    if (!gl) {
      return;
    }
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    const vertexLines = `
      attribute vec2 a_position;
      attribute vec3 a_color;
      uniform vec2 u_resolution;
      uniform vec2 u_offset;
      uniform float u_scale;
      varying vec3 v_color;
      void main() {
        vec2 scaled = (a_position + u_offset) * u_scale;
        vec2 zeroToOne = scaled / u_resolution;
        vec2 clip = zeroToOne * 2.0 - 1.0;
        gl_Position = vec4(clip * vec2(1.0, -1.0), 0.0, 1.0);
        v_color = a_color;
      }
    `;
    const fragmentLines = `
      precision mediump float;
      varying vec3 v_color;
      void main() {
        gl_FragColor = vec4(v_color, 1.0);
      }
    `;
    const vertexPoints = `
      attribute vec2 a_position;
      attribute vec3 a_color;
      attribute float a_size;
      uniform vec2 u_resolution;
      uniform vec2 u_offset;
      uniform float u_scale;
      varying vec3 v_color;
      void main() {
        vec2 scaled = (a_position + u_offset) * u_scale;
        vec2 zeroToOne = scaled / u_resolution;
        vec2 clip = zeroToOne * 2.0 - 1.0;
        gl_Position = vec4(clip * vec2(1.0, -1.0), 0.0, 1.0);
        gl_PointSize = a_size * u_scale;
        v_color = a_color;
      }
    `;
    const fragmentPoints = `
      precision mediump float;
      varying vec3 v_color;
      void main() {
        vec2 coord = gl_PointCoord - vec2(0.5);
        float dist = length(coord);
        if (dist > 0.5) {
          discard;
        }
        float edge = 0.5 - 0.05;
        float alpha = smoothstep(0.5, edge, dist);
        gl_FragColor = vec4(v_color, 0.95 * alpha);
      }
    `;

    const lineProgram = build_program(gl, vertexLines, fragmentLines);
    const pointProgram = build_program(gl, vertexPoints, fragmentPoints);

    const render = () => {
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);

      const { x, y, scale } = transformRef.current;

      // Edges
      const edgePositions: number[] = [];
      const edgeColors: number[] = [];
      edges.forEach((edge) => {
        const from = nodePositionMap.get(edge.from);
        const to = nodePositionMap.get(edge.to);
        if (!from || !to) {
          return;
        }
        edgePositions.push(from.x, from.y, to.x, to.y);
        const color = hex_to_rgb(EDGE_COLOR_MAP[edge.call_type] || "#b7410e");
        if (edge.active) {
          edgeColors.push(1.0, 0.9, 0.4, 1.0, 0.9, 0.4);
        } else {
          edgeColors.push(color.r, color.g, color.b, color.r, color.g, color.b);
        }
      });

      gl.useProgram(lineProgram);
      const edgePositionBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, edgePositionBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(edgePositions), gl.STATIC_DRAW);
      const edgeColorBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, edgeColorBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(edgeColors), gl.STATIC_DRAW);

      const aPosLine = gl.getAttribLocation(lineProgram, "a_position");
      gl.bindBuffer(gl.ARRAY_BUFFER, edgePositionBuffer);
      gl.enableVertexAttribArray(aPosLine);
      gl.vertexAttribPointer(aPosLine, 2, gl.FLOAT, false, 0, 0);

      const aColorLine = gl.getAttribLocation(lineProgram, "a_color");
      gl.bindBuffer(gl.ARRAY_BUFFER, edgeColorBuffer);
      gl.enableVertexAttribArray(aColorLine);
      gl.vertexAttribPointer(aColorLine, 3, gl.FLOAT, false, 0, 0);

      const uResolutionLine = gl.getUniformLocation(lineProgram, "u_resolution");
      const uOffsetLine = gl.getUniformLocation(lineProgram, "u_offset");
      const uScaleLine = gl.getUniformLocation(lineProgram, "u_scale");
      gl.uniform2f(uResolutionLine, canvas.width, canvas.height);
      gl.uniform2f(uOffsetLine, x, y);
      gl.uniform1f(uScaleLine, scale);
      gl.drawArrays(gl.LINES, 0, edgePositions.length / 2);

      // Nodes
      const nodePositionsFlat: number[] = [];
      const nodeColors: number[] = [];
      const nodeSizes: number[] = [];
      nodes.forEach((node) => {
        nodePositionsFlat.push(node.x, node.y);
        const baseColor = hex_to_rgb(NODE_COLOR_MAP[node.node_type] || "#a9a9a9");
        if (node.id === activeNodeId) {
          nodeColors.push(1.0, 0.8, 0.2);
        } else if (node.id === hoverNodeId) {
          nodeColors.push(1.0, 1.0, 1.0);
        } else {
          nodeColors.push(baseColor.r, baseColor.g, baseColor.b);
        }
        const baseSize = 40 + node.energy * 40;
        let finalSize = baseSize;
        if (node.id === activeNodeId) {
          finalSize += 20;
        }
        if (node.id === hoverNodeId) {
          finalSize += 10;
        }
        nodeSizes.push(finalSize);
      });

      gl.useProgram(pointProgram);
      const nodePositionBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, nodePositionBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(nodePositionsFlat), gl.STATIC_DRAW);
      const nodeColorBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, nodeColorBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(nodeColors), gl.STATIC_DRAW);
      const nodeSizeBuffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, nodeSizeBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(nodeSizes), gl.STATIC_DRAW);

      const aPosPoint = gl.getAttribLocation(pointProgram, "a_position");
      gl.bindBuffer(gl.ARRAY_BUFFER, nodePositionBuffer);
      gl.enableVertexAttribArray(aPosPoint);
      gl.vertexAttribPointer(aPosPoint, 2, gl.FLOAT, false, 0, 0);

      const aColorPoint = gl.getAttribLocation(pointProgram, "a_color");
      gl.bindBuffer(gl.ARRAY_BUFFER, nodeColorBuffer);
      gl.enableVertexAttribArray(aColorPoint);
      gl.vertexAttribPointer(aColorPoint, 3, gl.FLOAT, false, 0, 0);

      const aSizePoint = gl.getAttribLocation(pointProgram, "a_size");
      gl.bindBuffer(gl.ARRAY_BUFFER, nodeSizeBuffer);
      gl.enableVertexAttribArray(aSizePoint);
      gl.vertexAttribPointer(aSizePoint, 1, gl.FLOAT, false, 0, 0);

      const uResolutionPoint = gl.getUniformLocation(pointProgram, "u_resolution");
      const uOffsetPoint = gl.getUniformLocation(pointProgram, "u_offset");
      const uScalePoint = gl.getUniformLocation(pointProgram, "u_scale");
      gl.uniform2f(uResolutionPoint, canvas.width, canvas.height);
      gl.uniform2f(uOffsetPoint, x, y);
      gl.uniform1f(uScalePoint, scale);
      gl.drawArrays(gl.POINTS, 0, nodePositionsFlat.length / 2);

      const labelCanvas = labelCanvasRef.current;
      if (labelCanvas) {
        const ctx = labelCanvas.getContext("2d");
        if (ctx) {
          ctx.clearRect(0, 0, labelCanvas.width, labelCanvas.height);
          if (scale >= 0.3) {
            ctx.font = "bold 14px IBM Plex Sans, system-ui, sans-serif";
            ctx.textAlign = "center";
            nodes.forEach((node) => {
              const sx = (node.x + x) * scale;
              const sy = (node.y + y) * scale;
              const baseSize = 40 + node.energy * 40;
              const pixelSize = baseSize * scale;
              ctx.fillStyle = node.id === hoverNodeId ? "#ffffff" : "rgba(242, 237, 225, 0.9)";
              ctx.fillText(node.title, sx, sy + (pixelSize / 2) + 20);
            });
          }
        }
      }
    };

    render();
  }, [edges, nodes, activeNodeId, hoverNodeId, size, renderTick, nodePositionMap]);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) {
      return;
    }
    let dragging = false;
    let didDrag = false;
    let lastX = 0;
    let lastY = 0;

    const handleWheel = (event: WheelEvent) => {
      event.preventDefault();
      const delta = -event.deltaY * 0.001;
      const nextScale = Math.min(3.0, Math.max(0.1, transformRef.current.scale + delta));
      transformRef.current.scale = nextScale;
      setRenderTick((tick) => tick + 1);
    };

    const handleMouseDown = (event: MouseEvent) => {
      dragging = true;
      didDrag = false;
      lastX = event.clientX;
      lastY = event.clientY;
    };

    const handleMouseMove = (event: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const { x, y, scale } = transformRef.current;
      const worldX = (event.clientX - rect.left) / scale - x;
      const worldY = (event.clientY - rect.top) / scale - y;

      let found: string | null = null;
      for (const node of nodesRef.current) {
        const baseSize = 40 + node.energy * 40;
        const dx = worldX - node.x;
        const dy = worldY - node.y;
        if (Math.hypot(dx, dy) <= baseSize / 2) {
          found = node.id;
          break;
        }
      }
      setHoverNodeId(found);

      if (!dragging) {
        return;
      }
      const dx = event.clientX - lastX;
      const dy = event.clientY - lastY;
      lastX = event.clientX;
      lastY = event.clientY;
      if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
        didDrag = true;
      }
      transformRef.current.x += dx / transformRef.current.scale;
      transformRef.current.y += dy / transformRef.current.scale;
      setRenderTick((tick) => tick + 1);
    };

    const handleMouseUp = (event: MouseEvent) => {
      if (!didDrag) {
        const rect = container.getBoundingClientRect();
        const { x, y, scale } = transformRef.current;
        const worldX = (event.clientX - rect.left) / scale - x;
        const worldY = (event.clientY - rect.top) / scale - y;

        let clickedNodeId: string | null = null;
        for (const node of nodesRef.current) {
          const baseSize = 40 + node.energy * 40;
          const dx = worldX - node.x;
          const dy = worldY - node.y;
          if (Math.hypot(dx, dy) <= baseSize / 2) {
            clickedNodeId = node.id;
            break;
          }
        }

        if (clickedNodeId) {
          if (clickedNodeId === "player") {
            const content = window.prompt("Send a player message", "advance") ?? "";
            dispatch_runtime_command({ kind: "player_message", payload: { content } });
          } else {
            console.log("Clicked node:", clickedNodeId);
          }
        }
      }
      dragging = false;
    };

    container.addEventListener("wheel", handleWheel, { passive: false });
    container.addEventListener("mousedown", handleMouseDown);
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {
      container.removeEventListener("wheel", handleWheel);
      container.removeEventListener("mousedown", handleMouseDown);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, []);

  const handleFitView = useCallback(() => {
    transformRef.current = { x: 0, y: 0, scale: 1 };
    setRenderTick((tick) => tick + 1);
  }, []);

  return (
    <div className="connectome-canvas connectome-canvas-webgl" ref={containerRef}>
      <div className="connectome-zone-layer">
        {zones.map((zone) => (
          <div
            key={zone.zone_id}
            className="connectome-zone"
            style={{
              left: zone.x,
              top: zone.y,
              width: zone.width,
              height: zone.height,
            }}
          >
            {zone.title}
          </div>
        ))}
      </div>
      <canvas ref={canvasRef} className="connectome-webgl-canvas" />
      <canvas ref={labelCanvasRef} className="connectome-label-canvas" />
      <div className="canvas-overlay">
        <button className="btn btn-ghost" onClick={handleFitView}>
          Fit View
        </button>
      </div>
    </div>
  );
};

export default function FlowCanvas() {
  return <CanvasInner />;
}
