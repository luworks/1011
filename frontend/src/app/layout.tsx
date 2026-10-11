import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Policy Agent Console",
  description: "Evidence-bounded billing agent demo (local simulation, no real account actions)",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
