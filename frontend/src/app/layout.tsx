import type { Metadata } from "next";
import "./globals.css";
import React from "react";
import SmoothScroll from "../components/hooks/SmoothScroll";
import Preloader from "../components/Preloader";
import CustomCursor from "../components/CustomCursor";

export const metadata: Metadata = {
  title: "NexCore Studio | Next-Gen Web & AI Strategy",
  description: "Excellence in digital transformation through motion and performance.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-background text-primary antialiased selection:bg-accent selection:text-background grain overflow-x-hidden">
        <Preloader />
        <CustomCursor />
        <SmoothScroll>
          {children}
        </SmoothScroll>
      </body>
    </html>
  );
}
