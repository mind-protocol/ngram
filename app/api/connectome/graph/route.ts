import { NextResponse } from "next/server";
import { spawnSync } from "child_process";

const runGraphFetch = (graph: string) => {
  const host = process.env.NGRAM_FALKORDB_HOST ?? "localhost";
  const port = process.env.NGRAM_FALKORDB_PORT ?? "6379";
  const args = [
    "-m",
    "engine.physics.graph.connectome_read_cli",
    "--graph",
    graph,
    "--host",
    host,
    "--port",
    port,
  ];
  const baseEnv = {
    ...process.env,
    NGRAM_EMBEDDINGS_FALLBACK: "1",
    NGRAM_FALKORDB_TIMEOUT: "10.0",
  };
  const result = spawnSync("python", args, {
    cwd: process.cwd(),
    encoding: "utf-8",
    timeout: 120000,
    maxBuffer: 10 * 1024 * 1024,
    env: baseEnv,
  });
  if (result.error && (result.error as NodeJS.ErrnoException).code === "ENOENT") {
    return spawnSync("python3", args, {
      cwd: process.cwd(),
      encoding: "utf-8",
      timeout: 120000,
      maxBuffer: 10 * 1024 * 1024,
      env: baseEnv,
    });
  }
  return result;
};

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const graph = searchParams.get("graph") ?? "seed";
  const result = runGraphFetch(graph);
  if (result.error) {
    return NextResponse.json(
      { error: result.error.message ?? "Graph fetch failed" },
      { status: 500 }
    );
  }
  if (result.status !== 0) {
    return NextResponse.json(
      { error: result.stderr || result.stdout || "Graph fetch failed" },
      { status: 500 }
    );
  }
  try {
    return NextResponse.json(JSON.parse(result.stdout));
  } catch {
    return NextResponse.json(
      { error: "Graph fetch returned invalid JSON", raw: result.stdout },
      { status: 500 }
    );
  }
}
