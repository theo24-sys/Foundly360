export type DashboardMetrics = {
  open_cases: number;
  possible_matches: number;
  pending_claims: number;
  recovery_rate: number;
  category_breakdown: Array<{ category: string; total: number }>;
};

export type ReceivingPoint = { id: number; name: string; kind: string; address: string; opening_hours: string; contact_phone: string };
export type PublicOrganization = { id: number; name: string; slug: string; receiving_points: ReceivingPoint[] };
const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, { ...init, headers: { Accept: "application/json", "Content-Type": "application/json", ...init?.headers } });
  if (!response.ok) { const body = await response.json().catch(() => null) as { detail?: string } | null; throw new Error(body?.detail ?? "The request could not be completed."); }
  return response.json() as Promise<T>;
}

export function getDashboardMetrics(organizationId: number, signal?: AbortSignal): Promise<DashboardMetrics> { return request<DashboardMetrics>(`/organizations/${organizationId}/dashboard/`, { credentials: "include", signal }); }
export function getPublicOrganizations(signal?: AbortSignal): Promise<PublicOrganization[]> { return request<PublicOrganization[]>("/public/organizations/", { signal }); }
export function submitLostReport(payload: { organization: number; claimant_name: string; claimant_phone: string; category: string; description: string; last_seen_location: string }): Promise<{ reference: string }> { return request<{ reference: string }>("/public/lost-reports/", { method: "POST", body: JSON.stringify(payload) }); }
export function submitFoundItem(payload: { organization: number; location: number; category: string; title: string; private_description: string }): Promise<{ reference: string }> { return request<{ reference: string }>("/public/found-items/", { method: "POST", body: JSON.stringify(payload) }); }
