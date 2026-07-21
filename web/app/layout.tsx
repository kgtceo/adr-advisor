import type { Metadata } from "next";
import "./globals.css";

const url = "https://adr-advisor.kareemghazal.com";
const title = "adr-advisor — architecture-decision trade-off advisor";
const description =
  "Give it a decision and candidate options; it weighs each across scalability, reliability, cost, operability and maintainability, and recommends one of your options (never an invented one) — with an eval harness.";

export const metadata: Metadata = {
  metadataBase: new URL(url),
  title,
  description,
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url,
    siteName: "adr-advisor",
    title,
    description,
    locale: "en_GB",
    images: [{ url: "/og.jpg", width: 1200, height: 630, alt: "adr-advisor — architecture-decision trade-off advisor" }],
  },
  twitter: { card: "summary_large_image", title, description, images: ["/og.jpg"] },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
