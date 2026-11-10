import { Eligibility, Match } from "../api";

function fitClass(score: number) {
  if (score >= 70) return "fit-high";
  if (score >= 40) return "fit-medium";
  return "fit-low";
}

function fitLabel(score: number) {
  if (score >= 70) return "Strong";
  if (score >= 40) return "Possible";
  return "Weak";
}

export default function MatchList({
  matches,
  eligibility,
  onRerun,
  onViewTimeline,
  onViewDraft,
}: {
  matches: Match[];
  eligibility: Eligibility[];
  onRerun: (ids?: string[]) => void;
  onViewTimeline: () => void;
  onViewDraft: () => void;
}) {
  const eligibleCount = eligibility.filter((e) => e.eligible).length;

  return (
    <div>
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-value">{matches.length}</div>
          <div className="stat-label">Matches</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: "var(--green)" }}>
            {eligibleCount}
          </div>
          <div className="stat-label">Eligible</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: "var(--amber)" }}>
            {matches.filter((m) => m.fit_score >= 70).length}
          </div>
          <div className="stat-label">Strong Fit</div>
        </div>
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 24 }}>
        <button className="btn btn-secondary" onClick={() => onRerun()}>
          🔄 Re-run Agent
        </button>
        <button className="btn btn-secondary" onClick={onViewTimeline}>
          📅 View Timeline
        </button>
        <button className="btn btn-primary" onClick={onViewDraft}>
          📄 View Drafts
        </button>
      </div>

      {matches.map((m) => {
        const elig = eligibility.find((e) => e.program_id === m.program_id);
        return (
          <div key={m.program_id} className="match-card">
            <div className="match-header">
              <div>
                <div className="match-title">{m.program_name}</div>
                <div className="match-uni">
                  {m.university} • {m.location}
                </div>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                {elig && (
                  <span className={`badge ${elig.eligible ? "badge-eligible" : "badge-ineligible"}`}>
                    {elig.eligible ? "Eligible" : "Not Eligible"}
                  </span>
                )}
                <div className={`fit-score ${fitClass(m.fit_score)}`}>{m.fit_score}</div>
              </div>
            </div>

            <div className="match-meta">
              <div className="meta-item">
                <strong>{fitLabel(m.fit_score)}</strong> fit
              </div>
              <div className="meta-item">
                Seats: <strong>{m.total_seats}</strong>
              </div>
              <div className="meta-item">
                Fee: <strong>BDT {m.tuition_fee_bdt.toLocaleString()}</strong>
              </div>
              <div className="meta-item">
                Level: <strong>{m.degree_level}</strong>
              </div>
            </div>

            <div className="reasons">
              {m.reasons.map((r, i) => (
                <span
                  key={i}
                  className={`reason ${
                    r.includes("meets") || r.includes("matches") || r.includes("Open")
                      ? "reason-pass"
                      : r.includes("below") || r.includes("does not")
                      ? "reason-fail"
                      : "reason-info"
                  }`}
                >
                  {r}
                </span>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
