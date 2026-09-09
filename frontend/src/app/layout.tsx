import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Foundry360 | Lost property operations",
  description: "Institutional lost-property operations for Kenya.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
