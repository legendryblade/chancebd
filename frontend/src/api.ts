export interface Program {
  id: string;
  university: string;
  program_name: string;
  degree_level: string;
  required_group: string | null;
  min_hsc_gpa: number | null;
  min_ssc_gpa: number | null;
  application_start: string;
  application_deadline: string;
  exam_date: string;
  total_seats: number;
  tuition_fee_bdt: number;
  location: string;
  campus: string;
  required_documents: string;
  notes: string | null;
  official_website: string | null;
}

export interface Match {
  program_id: string;
  university: string;
  program_name: string;
  degree_level: string;
  location: string;
  tuition_fee_bdt: number;
  total_seats: number;
  fit_score: number;
  reasons: string[];
}

export interface Eligibility {
  program_id: string;
  university: string;
  program_name: string;
  eligible: boolean;
  reasons: string[];
  required_group: string | null;
  min_hsc_gpa: number | null;
  min_ssc_gpa: number | null;
}

export interface Deadline {
  program_id: string;
  university: string;
  program_name: string;
  application_start: string;
  application_deadline: string;
  exam_date: string;
  status: string;
  days_remaining: number;
}

export interface Draft {
  program_id: string;
  university: string;
  program_name: string;
  draft_text: string;
  required_documents: string[];
}

export interface InvestigationResult {
  investigation_id: number;
  profile: Record<string, unknown>;
  matches: Match[];
  eligibility: Eligibility[];
  deadlines: Deadline[];
  drafts: Draft[];
  steps: { tool: string; input: unknown; output: unknown }[];
  mode: string;
}

export interface Profile {
  name: string;
  hsc_gpa: number;
  hsc_board: string;
  hsc_group: string;
  hsc_year: number;
  ssc_gpa: number;
  ssc_board: string;
  ssc_group: string;
  ssc_year: number;
  preferred_location?: string;
  preferred_degree_level?: string;
}

const BASE = "/api";

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json();
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json();
}

export const api = {
  health: () => get<{ status: string; programs: number }>("/health"),
  programs: () => get<Program[]>("/programs"),
  createProfile: (profile: Profile) => post<{ profile_id: number }>("/profile", profile),
  investigate: (profileId: number, programIds?: string[]) =>
    post<InvestigationResult>("/investigate", { profile_id: profileId, program_ids: programIds }),
};
