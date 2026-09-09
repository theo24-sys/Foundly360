import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Foundry360",
    short_name: "Foundry360",
    description: "Institutional lost-property operations for Kenya.",
    start_url: "/",
    display: "standalone",
    background_color: "#f8faf7",
    theme_color: "#126b57",
    icons: [],
  };
}
