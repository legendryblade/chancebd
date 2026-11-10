import { useEffect, useState } from "react";
import { api, InvestigationResult, Profile, Program } from "./api";
import ProfileForm from "./components/ProfileForm";
import MatchList from "./components/MatchList";
import Timeline from "./components/Timeline";
import DraftView from "./components/DraftView";
import AgentSteps from "./components/AgentSteps";

type Step = "profile" | "matches" | "timeline" | "draft";

function describeStep(tool: string, output: unknown): string {
  if (Array.isArray(output)) {
    const n = output.length;
    return `Processed ${n} item${n === 1 ? "" : "s"}`;
  }
  if (output && typeof output === "object") {
    const o = output as Record<string, unknown>;
    if (typeof o.count === "number") {
      return `Scored ${o.count} programs against your profile`;
    }
  }
  return "Completed";
}

export default function App() {
  const [step, setStep] = useState<Step>("profile");
  const [profile, setProfile] = useState<Profile | null>(null);
  const [result, setResult] = useState<InvestigationResult | null>(null);
  const [programs, setPrograms] = useState<Program[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [health, setHealth] = useState<{ status: string; programs: number } | null>(null);

  useEffect(() => {
    api.health().then(setHealth).catch((e) => setError(String(e)));
    api.programs().then(setPrograms).catch(() => {});
  }, []);

  async function handleProfileSubmit(p: Profile) {
    setLoading(true);
    setError(null);
    try {
      const { profile_id } = await api.createProfile(p);
      const inv = await api.investigate(profile_id);
      setProfile(p);
      setResult(inv);
      setStep("matches");
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  async function handleRerun(programIds?: string[]) {
    if (!profile) return;
    setLoading(true);
    setError(null);
    try {
      const { profile_id } = await api.createProfile(profile);
      const inv = await api.investigate(profile_id, programIds);
      setResult(inv);
      setStep("matches");
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  const steps: { key: Step; label: string }[] = [
    { key: "profile", label: "Profile" },
    { key: "matches", label: "Matches" },
    { key: "timeline", label: "Timeline" },
    { key: "draft", label: "Draft" },
  ];

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <div className="logo-icon">C</div>
          <div className="logo-text">
            Chance<span>BD</span>
          </div>
        </div>
        <div className="header-badge">
          {health ? `${health.programs} programs • Agent ready` : "Connecting..."}
        </div>
      </header>

      <main className="main">
        <div className="steps">
          {steps.map((s, i) => {
            const order = steps.findIndex((x) => x.key === step);
            const cls = i < order ? "done" : i === order ? "active" : "";
            return (
              <div key={s.key} className={`step ${cls}`} onClick={() => setStep(s.key)}>
                {i + 1}. {s.label}
              </div>
            );
          })}
        </div>

        {error && (
          <div className="card" style={{ borderColor: "rgba(239,68,68,0.4)", background: "rgba(239,68,68,0.08)" }}>
            <strong style={{ color: "var(--red)" }}>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner" />
            Running investigation agent...
          </div>
        )}

        {!loading && step === "profile" && (
          <ProfileForm onSubmit={handleProfileSubmit} programCount={programs.length} />
        )}

        {!loading && step === "matches" && result && (
          <>
            <div className="card">
              <div className="card-title" style={{ fontSize: 18 }}>
                Agent Execution Log
              </div>
              <div className="card-subtitle">
                Bounded tool loop — {result.steps.length} steps, deterministic mode
              </div>
              <div className="agent-steps">
                {result.steps.map((s, i) => (
                  <div key={i} className="agent-step">
                    <div className="step-num">{i + 1}</div>
                    <div>
                      <span className="step-tool">{s.tool}</span>
                      <span className="step-desc">
                        {" "}
                        — {describeStep(s.tool, s.output)}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <MatchList
              matches={result.matches}
              eligibility={result.eligibility}
              onRerun={handleRerun}
              onViewTimeline={() => setStep("timeline")}
              onViewDraft={() => setStep("draft")}
            />
          </>
        )}

        {!loading && step === "timeline" && result && (
          <Timeline deadlines={result.deadlines} matches={result.matches} />
        )}

        {!loading && step === "draft" && result && (
          <DraftView drafts={result.drafts} matches={result.matches} />
        )}

        {!loading && step === "matches" && !result && (
          <div className="empty-state">
            <div className="empty-icon">🎓</div>
            <h2>No investigation yet</h2>
            <p>Fill your profile to get matched with programs.</p>
          </div>
        )}
      </main>
    </div>
  );
}
