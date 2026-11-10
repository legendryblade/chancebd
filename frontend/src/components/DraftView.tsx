import { useState } from "react";
import { Draft, Match } from "../api";

export default function DraftView({ drafts, matches }: { drafts: Draft[]; matches: Match[] }) {
  const [selected, setSelected] = useState(0);
  const [copied, setCopied] = useState(false);

  if (drafts.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">📄</div>
        <h2>No drafts</h2>
        <p>Run an investigation first.</p>
      </div>
    );
  }

  const draft = drafts[selected];
  const match = matches.find((m) => m.program_id === draft.program_id);

  function copy() {
    navigator.clipboard.writeText(draft.draft_text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div>
      <div className="tabs">
        {drafts.map((d, i) => (
          <button
            key={d.program_id}
            className={`tab ${i === selected ? "active" : ""}`}
            onClick={() => setSelected(i)}
          >
            {d.university.split(" ")[0]} — {d.program_name.split(" ").slice(0, 3).join(" ")}
          </button>
        ))}
      </div>

      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <div>
            <div className="card-title">{draft.program_name}</div>
            <div className="card-subtitle">
              {draft.university}
              {match ? ` • Fit ${match.fit_score}/100` : ""}
            </div>
          </div>
          <button className="btn btn-primary" onClick={copy}>
            {copied ? "✓ Copied" : "📋 Copy Draft"}
          </button>
        </div>

        <div className="draft-box">{draft.draft_text}</div>

        <div style={{ marginTop: 24 }}>
          <div className="card-title" style={{ fontSize: 16 }}>
            Required Documents
          </div>
          <div className="reasons" style={{ marginTop: 12 }}>
            {draft.required_documents.map((doc, i) => (
              <span key={i} className="reason reason-info">
                {doc}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
