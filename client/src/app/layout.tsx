import type { Metadata } from "next";
import "@/app/globals.css";

export const metadata: Metadata = {
  title: "Price Comparison Engine",
  description: "Compare prices across multiple retailers",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
