import type { Metadata, Viewport } from "next";
import { Inter_Tight, IBM_Plex_Mono } from "next/font/google";
import "@/styles/jw-deck.css";

const interTight = Inter_Tight({ subsets: ["latin"], weight: ["400", "500", "600", "700", "800"], variable: "--font-inter-tight", display: "swap" });
const plexMono = IBM_Plex_Mono({ subsets: ["latin"], weight: ["400", "500", "600"], variable: "--font-plex-mono", display: "swap" });

export const metadata: Metadata = {
  title: "jouleWise · Decarbonisation stack",
  description: "Green power, green heat, ergOS and esgOS — one provider for industrial decarbonisation.",
};

export const viewport: Viewport = { width: "device-width", initialScale: 1, viewportFit: "cover", themeColor: "#090a0b" };

/* If this section is merged into an existing site, drop this file and add the two font
   variables + the CSS import to the site's own root layout instead. */
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${interTight.variable} ${plexMono.variable}`}>
      <body style={{ margin: 0, background: "#090a0b" }}>{children}</body>
    </html>
  );
}
