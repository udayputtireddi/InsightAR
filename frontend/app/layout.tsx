import "./globals.css";
import Link from "next/link";

export const metadata = {
  title: "InsightAR",
  description: "AI-powered multimodal document and image analyzer",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen">
        {/* NAVIGATION BAR */}
        <nav className="w-full bg-white shadow-sm border-b px-8 py-4 flex items-center gap-8 sticky top-0 z-50">
          <Link href="/" className="text-lg font-semibold hover:text-blue-600">
            🖼 Image Analyzer
          </Link>
          <Link href="/document" className="text-lg font-semibold hover:text-blue-600">
            📄 Document Analyzer
          </Link>
        </nav>

        <main className="p-8">{children}</main>
      </body>
    </html>
  );
}
