export default function AgentSteps() {
  return (
    <div className="card">
      <div className="card-title">Agent Execution Log</div>
      <div className="card-subtitle">
        The bounded tool loop that produced your results.
      </div>
      <div className="agent-steps">
        <div className="agent-step">
          <div className="step-num">1</div>
          <div>
            <span className="step-tool">match_programs</span>
            <span className="step-desc"> — Scored all programs against profile</span>
          </div>
        </div>
        <div className="agent-step">
          <div className="step-num">2</div>
          <div>
            <span className="step-tool">check_eligibility</span>
            <span className="step-desc"> — Verified GPA and group requirements</span>
          </div>
        </div>
        <div className="agent-step">
          <div className="step-num">3</div>
          <div>
            <span className="step-tool">track_deadline</span>
            <span className="step-desc"> — Checked application windows</span>
          </div>
        </div>
        <div className="agent-step">
          <div className="step-num">4</div>
          <div>
            <span className="step-tool">draft_application</span>
            <span className="step-desc"> — Generated application drafts</span>
          </div>
        </div>
      </div>
    </div>
  );
}
