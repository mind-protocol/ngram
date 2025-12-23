import { NextResponse } from "next/server";
import { spawnSync } from "child_process";

const runSearchWithPython = (
  query: string,
  threshold: number,
  hops: number,
  graph: string
) => {
  const host = process.env.NGRAM_FALKORDB_HOST ?? "localhost";
  const port = process.env.NGRAM_FALKORDB_PORT ?? "6379";
  const args = [
    "-m",
    "engine.physics.graph.connectome_read_cli",
    "--search",
    query,
    "--threshold",
    String(threshold),
    "--hops",
    String(hops),
    "--graph",
    graph,
    "--host",
    host,
    "--port",
    port,
  ];
  const result = spawnSync("python", args, {
    cwd: process.cwd(),
    encoding: "utf-8",
    timeout: 120000,
    maxBuffer: 10 * 1024 * 1024,
    env: {
      ...process.env,
      NGRAM_EMBEDDINGS_FALLBACK: "1",
      NGRAM_FALKORDB_TIMEOUT: "10.0",
    },
  });
  if (result.error && (result.error as NodeJS.ErrnoException).code === "ENOENT") {
    return spawnSync("python3", args, {
      cwd: process.cwd(),
      encoding: "utf-8",
      timeout: 120000,
      maxBuffer: 10 * 1024 * 1024,
      env: {
        ...process.env,
        NGRAM_EMBEDDINGS_FALLBACK: "1",
        NGRAM_FALKORDB_TIMEOUT: "10.0",
      },
    });
  }
  return result;
};

const runSearch = (
  query: string,
  threshold: number,
  hops: number,
  graph: string
) => {
  const result = runSearchWithPython(query, threshold, hops, graph);
  if (result.error) {
    throw result.error;
  }
  if (result.status !== 0) {
    const stderr = result.stderr?.trim();
    const stdout = result.stdout?.trim();
    if (stdout) {
      try {
        return { ok: false, payload: JSON.parse(stdout), stderr };
      } catch (error) {
        throw new Error(stderr || stdout || "connectome_read_cli failed");
      }
    }
    throw new Error(stderr || "connectome_read_cli failed");
  }
  try {
    return { ok: true, payload: JSON.parse(result.stdout) };
  } catch (error: any) {
    throw new Error(`connectome_read_cli returned invalid JSON: ${result.stdout}`);
  }
};

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q") ?? "";
  const threshold = Number(searchParams.get("threshold") ?? "0.3");
  const hops = Number(searchParams.get("hops") ?? "1");
  const graph = searchParams.get("graph") ?? "seed";

  if (!query.trim()) {
    return NextResponse.json({ error: "Query required." }, { status: 400 });
  }

  try {
    const result = runSearch(query, threshold, hops, graph);
    if (!result.ok) {
      return NextResponse.json(
        {
          error: result.payload?.error ?? "connectome_read_cli failed",
          detail: result.payload,
          stderr: result.stderr ?? null,
        },
        { status: 500 }
      );
    }
    return NextResponse.json(result.payload);
  } catch (error: any) {
    return NextResponse.json(
      { error: error?.message ?? "Search failed" },
      { status: 500 }
    );
  }
}
