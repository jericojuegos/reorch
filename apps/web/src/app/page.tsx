export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950 text-white">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center min-h-screen px-6 text-center">
        {/* Logo / Brand */}
        <div className="mb-8">
          <span className="inline-block px-4 py-2 text-sm font-medium text-purple-400 bg-purple-500/10 rounded-full border border-purple-500/20">
            🎵 Phase 0 — Foundation
          </span>
        </div>

        {/* Main Heading */}
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent">
          REORCH
        </h1>

        {/* Tagline */}
        <p className="text-xl md:text-2xl text-zinc-400 max-w-2xl mb-12 leading-relaxed">
          The premier AI-assisted platform for professional music{" "}
          <span className="text-purple-400 font-medium">re-orchestration</span>{" "}
          and{" "}
          <span className="text-purple-400 font-medium">genre transformation</span>.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button className="px-8 py-4 bg-purple-600 hover:bg-purple-500 text-white font-semibold rounded-xl transition-all duration-200 shadow-lg shadow-purple-600/25 hover:shadow-purple-500/40 hover:scale-105">
            Get Started
          </button>
          <button className="px-8 py-4 bg-zinc-800 hover:bg-zinc-700 text-white font-semibold rounded-xl transition-all duration-200 border border-zinc-700 hover:border-zinc-600">
            Learn More
          </button>
        </div>

        {/* Status Indicator */}
        <div className="mt-16 flex items-center gap-3 text-sm text-zinc-500">
          <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          <span>Development in progress — Monorepo initialized</span>
        </div>
      </div>

      {/* Footer */}
      <footer className="absolute bottom-0 w-full py-6 text-center text-zinc-600 text-sm">
        <p>Built with Next.js, Tailwind CSS, FastAPI, and ❤️</p>
      </footer>
    </div>
  );
}
