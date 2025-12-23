// frontend/components/ConnectomeHealthPanel.tsx (stub)

import React from "react";

type HealthEvent = any;

function Badge({ state }: { state: string }) {
  const cls =
    state === "OK"
      ? "bg-green-100 text-green-800"
      : state === "WARN"
      ? "bg-yellow-100 text-yellow-800"
      : "bg-red-100 text-red-800";
  return <span className={`px-2 py-1 rounded text-xs font-semibold ${cls}`}>{state}</span>;
}

export function ConnectomeHealthPanel({ ev }: { ev: HealthEvent | null }) {
  if (!ev) return <div className="p-3 rounded border text-sm">Waiting for health stream…</div>;

  const { status, runner, counters, attention, pressure } = ev;

  return (
    <div className="p-3 rounded border space-y-2 text-sm">
      <div className="flex items-center justify-between">
        <div className="font-semibold">Connectome Health</div>
        <div className="flex items-center gap-2">
          <Badge state={status?.state ?? "UNKNOWN"} />
          <span className="text-xs opacity-70">score {Number(status?.score ?? 0).toFixed(2)}</span>
        </div>
      </div>

      {status?.notes?.length ? (
        <div className="text-xs opacity-80">
          {status.notes.map((n: string, i: number) => (
            <div key={i}>• {n}</div>
          ))}
        </div>
      ) : null}

      <div className="grid grid-cols-2 gap-2">
        <div className="rounded border p-2">
          <div className="text-xs opacity-70">Runner</div>
          <div className="flex items-center justify-between">
            <div>speed <b>{runner?.speed ?? "?"}</b></div>
            <div>tick <b>{runner?.tick ?? "?"}</b></div>
          </div>
          <div className="text-xs mt-1 opacity-80">
            last interrupt: <b>{runner?.last_interrupt?.reason ?? "none"}</b>
          </div>
        </div>

        <div className="rounded border p-2">
          <div className="text-xs opacity-70">Attention</div>
          <div className="flex items-center justify-between">
            <div>sinks p50 <b>{Number(attention?.sink_set_size_p50 ?? 0).toFixed(0)}</b></div>
            <div>p95 <b>{Number(attention?.sink_set_size_p95 ?? 0).toFixed(0)}</b></div>
          </div>
          <div className="text-xs mt-1 opacity-80">
            reconfig/min <b>{Number(attention?.focus_reconfig_rate_per_min ?? 0).toFixed(1)}</b>
            {" · "}
            plateau <b>{Number(attention?.plateau_seconds ?? 0).toFixed(0)}s</b>
          </div>
        </div>

        <div className="rounded border p-2">
          <div className="text-xs opacity-70">Pressure</div>
          <div>contradiction <b>{Number(pressure?.contradiction ?? 0).toFixed(2)}</b></div>
          <div className="text-xs opacity-80 mt-1">(local, bounded)</div>
        </div>

        <div className="rounded border p-2">
          <div className="text-xs opacity-70">Hard counters</div>
          <div className="flex items-center justify-between">
            <div>query writes <b>{counters?.query_write_attempts ?? 0}</b></div>
            <div>DMZ <b>{counters?.dmz_violation_attempts ?? 0}</b></div>
          </div>
          <div className="text-xs opacity-80 mt-1">
            async mismatch <b>{counters?.async_epoch_mismatch ?? 0}</b>
          </div>
        </div>
      </div>
    </div>
  );
}
