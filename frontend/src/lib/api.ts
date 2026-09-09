export type DashboardMetrics = {
  open_cases: number;
  possible_matches: number;
  pending_claims: number;
  recovery_rate: number;
  category_breakdown: Array<{ category: string; total: number }>;
};

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export async function getDashboardMetrics(organizationId: number, signal?: AbortSignal): Promise<DashboardMetrics> {
  const response = await fetch(`${apiUrl}/organizations/${organizationId}/dashboard/`, {
    credentials: "include",
    signal,
    headers: { Accept: "application/json" },
  });
  if (!response.ok) throw new Error("Unable to load dashboard metrics.");
  return response.json() as Promise<DashboardMetrics>;
}
