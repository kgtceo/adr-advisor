"use client";

import { useState } from "react";
import { advise, getExample } from "../lib/api";
import type { AdrResult } from "../lib/types";

export default function Home() {
  const [decision, setDecision] = useState("");
  const [options, setOptions] = useState<string[]>(["", ""]);
  const [result, setResult] = useState<AdrResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function setOption(i: number, v: string) {
    setOptions((o) => o.map((x, j) => (j === i ? v : x)));
  }

  async function run() {
    const opts = options.map((o) => o.trim()).filter(Boolean);
    if (!decision.trim() || opts.length < 2) {
      setError("Add a decision and at least two options.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      setResult(await advise(decision, opts));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  async function loadExample() {
    try {
      const ex = await getExample();
      setDecision(ex.decision);
      setOptions(ex.options);
      setResult(null);
    } catch {
      /* ignore */
    }
  }

  const a = result?.advice;

  return (
    <div className="container">
      <header>
        <h1>adr-advisor</h1>
        <p>
          Describe an architecture decision and the options you&rsquo;re weighing. It analyses each
          across the trade-off axes and recommends one of <em>your</em> options — never an invented one.
        </p>
      </header>

      <label htmlFor="d">Decision &amp; constraints</label>
      <textarea
        id="d"
        value={decision}
        placeholder="e.g. Queue between order service and email sender. Per-user ordering matters; small team; ~1k msg/s; AWS serverless."
        onChange={(e) => setDecision(e.target.value)}
      />

      <label>Options to compare</label>
      {options.map((o, i) => (
        <div className="opt-row" key={i}>
          <input
            type="text"
            value={o}
            placeholder={`Option ${i + 1}`}
            onChange={(e) => setOption(i, e.target.value)}
          />
          {options.length > 2 && (
            <button className="ghost" onClick={() => setOptions((os) => os.filter((_, j) => j !== i))}>✕</button>
          )}
        </div>
      ))}
      <button className="ghost" onClick={() => setOptions((o) => [...o, ""])}>+ Add option</button>

      <div className="actions">
        <button onClick={run} disabled={loading}>{loading ? "Weighing…" : "Advise"}</button>
        <button className="ghost" onClick={loadExample} disabled={loading}>Load example</button>
      </div>

      {error && <div className="error">{error}</div>}

      {a && (
        <>
          <div className="panel">
            <h2>Decision</h2>
            <p style={{ margin: 0 }}>{a.context_summary}</p>
          </div>

          <div className="panel">
            <h2>Trade-offs</h2>
            <table>
              <thead><tr><th>Axis</th><th>Favoured</th><th>Note</th></tr></thead>
              <tbody>
                {a.trade_offs.map((t, i) => (
                  <tr key={i}><td>{t.axis}</td><td className="fav">{t.favoured_option}</td><td>{t.note}</td></tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="panel">
            <h2>Options</h2>
            {a.option_analyses.map((o, i) => (
              <div className="opt" key={i}>
                <h3>{o.option}</h3>
                <div className="nf">{o.notable_for}</div>
                {o.pros.map((p, j) => <div className="pro" key={j}>+ {p}</div>)}
                {o.cons.map((c, j) => <div className="con" key={j}>− {c}</div>)}
              </div>
            ))}
          </div>

          <div className="rec">
            <div className="pick">
              → {a.recommendation.option}
              {!result!.recommendation_valid && <span className="warn"> (⚠ not one of your options)</span>}
            </div>
            <p style={{ margin: "8px 0" }}>{a.recommendation.rationale}</p>
            <div className="meta"><strong>Risks accepted:</strong> {a.recommendation.key_risks.join("; ") || "—"}</div>
            <div className="meta"><strong>Revisit when:</strong> {a.recommendation.revisit_when}</div>
          </div>
        </>
      )}
    </div>
  );
}
