import { Deadline, Match } from "../api";

function formatDate(s: string) {
  const d = new Date(s);
  return d.toLocaleDateString("en-BD", { day: "numeric", month: "short", year: "numeric" });
}

function statusClass(status: string) {
  return status;
}

export default function Timeline({
  deadlines,
  matches,
}: {
  deadlines: Deadline[];
  matches: Match[];
}) {
  const all = deadlines.map((d) => {
    const m = matches.find((x) => x.program_id === d.program_id);
    return { ...d, fit_score: m?.fit_score ?? 0 };
  });
  all.sort((a, b) => new Date(a.application_deadline).getTime() - new Date(b.application_deadline).getTime());

  return (
    <div className="card">
      <div className="card-title">Application Timeline</div>
      <div className="card-subtitle">
        Deadlines for your top matches. Act before they close.
      </div>

      <div className="timeline">
        {all.map((d) => (
          <div key={d.program_id} className={`timeline-item ${statusClass(d.status)}`}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <div className="timeline-date">
                  Opens {formatDate(d.application_start)} → Closes {formatDate(d.application_deadline)}
                </div>
                <div className="timeline-title">
                  {d.university} — {d.program_name}
                </div>
                <div className="meta-item" style={{ marginTop: 6 }}>
                  Exam: <strong>{formatDate(d.exam_date)}</strong> • Fit: <strong>{d.fit_score}/100</strong>
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <span className={`badge badge-${d.status}`}>
                  {d.status === "urgent" ? "Urgent" : d.status === "approaching" ? "Approaching" : d.status === "closed" ? "Closed" : "Open"}
                </span>
                <div style={{ marginTop: 8, fontSize: 13, color: "var(--text-muted)" }}>
                  {d.status === "closed" ? "Passed" : `${d.days_remaining} days left`}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
