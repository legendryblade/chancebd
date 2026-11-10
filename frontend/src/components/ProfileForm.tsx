import { useState } from "react";
import { Profile } from "../api";

const BOARDS = ["Dhaka", "Chittagong", "Rajshahi", "Khulna", "Barisal", "Sylhet", "Comilla", "Jessore", "Dinajpur", "Mymensingh", "Madrasah", "Technical"];
const GROUPS = ["Science", "Humanities", "Business"];
const LOCATIONS = ["Dhaka", "Chittagong", "Rajshahi", "Sylhet", "Khulna", "Barisal", "Rangpur", "Mymensingh"];

export default function ProfileForm({
  onSubmit,
  programCount,
}: {
  onSubmit: (p: Profile) => void;
  programCount: number;
}) {
  const [form, setForm] = useState<Profile>({
    name: "Rahim Ahmed",
    hsc_gpa: 4.5,
    hsc_board: "Dhaka",
    hsc_group: "Science",
    hsc_year: 2024,
    ssc_gpa: 4.8,
    ssc_board: "Dhaka",
    ssc_group: "Science",
    ssc_year: 2022,
    preferred_location: "",
    preferred_degree_level: "",
  });

  function set<K extends keyof Profile>(key: K, value: Profile[K]) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  return (
    <div>
      <div className="card">
        <div className="card-title">Your Academic Profile</div>
        <div className="card-subtitle">
          Enter your HSC and SSC results. The agent will match you against {programCount} programs
          across Bangladesh's top universities.
        </div>

        <div className="form-grid">
          <div className="form-group">
            <label>Full Name</label>
            <input value={form.name} onChange={(e) => set("name", e.target.value)} />
          </div>
          <div className="form-group">
            <label>HSC GPA (out of 5)</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="5"
              value={form.hsc_gpa}
              onChange={(e) => set("hsc_gpa", parseFloat(e.target.value))}
            />
          </div>
          <div className="form-group">
            <label>HSC Group</label>
            <select value={form.hsc_group} onChange={(e) => set("hsc_group", e.target.value)}>
              {GROUPS.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>HSC Board</label>
            <select value={form.hsc_board} onChange={(e) => set("hsc_board", e.target.value)}>
              {BOARDS.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>HSC Year</label>
            <input
              type="number"
              value={form.hsc_year}
              onChange={(e) => set("hsc_year", parseInt(e.target.value))}
            />
          </div>
          <div className="form-group">
            <label>SSC GPA (out of 5)</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="5"
              value={form.ssc_gpa}
              onChange={(e) => set("ssc_gpa", parseFloat(e.target.value))}
            />
          </div>
          <div className="form-group">
            <label>SSC Group</label>
            <select value={form.ssc_group} onChange={(e) => set("ssc_group", e.target.value)}>
              {GROUPS.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>SSC Board</label>
            <select value={form.ssc_board} onChange={(e) => set("ssc_board", e.target.value)}>
              {BOARDS.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>SSC Year</label>
            <input
              type="number"
              value={form.ssc_year}
              onChange={(e) => set("ssc_year", parseInt(e.target.value))}
            />
          </div>
          <div className="form-group">
            <label>Preferred Location (optional)</label>
            <select
              value={form.preferred_location}
              onChange={(e) => set("preferred_location", e.target.value)}
            >
              <option value="">Any</option>
              {LOCATIONS.map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Degree Level (optional)</label>
            <select
              value={form.preferred_degree_level}
              onChange={(e) => set("preferred_degree_level", e.target.value)}
            >
              <option value="">Any</option>
              <option value="HSC">HSC</option>
              <option value="SSC">SSC</option>
            </select>
          </div>
        </div>

        <div style={{ marginTop: 28 }}>
          <button className="btn btn-primary" onClick={() => onSubmit(form)}>
            🔍 Run Investigation Agent
          </button>
        </div>
      </div>

      <div className="card">
        <div className="card-title" style={{ fontSize: 18 }}>
          How the agent works
        </div>
        <div className="agent-steps">
          <div className="agent-step">
            <div className="step-num">1</div>
            <div>
              <span className="step-tool">match_programs</span>
              <span className="step-arrow"> → </span>
              <span className="step-desc">Scores all {programCount} programs against your GPA, group, and preferences</span>
            </div>
          </div>
          <div className="agent-step">
            <div className="step-num">2</div>
            <div>
              <span className="step-tool">check_eligibility</span>
              <span className="step-arrow"> → </span>
              <span className="step-desc">Verifies you meet minimum GPA and group requirements</span>
            </div>
          </div>
          <div className="agent-step">
            <div className="step-num">3</div>
            <div>
              <span className="step-tool">track_deadline</span>
              <span className="step-arrow"> → </span>
              <span className="step-desc">Flags urgent deadlines and days remaining</span>
            </div>
          </div>
          <div className="agent-step">
            <div className="step-num">4</div>
            <div>
              <span className="step-tool">draft_application</span>
              <span className="step-arrow"> → </span>
              <span className="step-desc">Generates a ready-to-review application draft</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
