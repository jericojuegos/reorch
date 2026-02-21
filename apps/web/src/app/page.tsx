export default function Home() {
  return (
    <div className="bg-background-dark text-creamy-white/70 font-sans selection:bg-primary/30">
      <header className="fixed top-0 left-0 right-0 z-50 bg-background-dark/80 backdrop-blur-md border-b border-creamy-white/5">
        <nav className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <a className="flex items-center gap-2 group" href="#">
              <div className="w-8 h-8 bg-primary rounded flex items-center justify-center text-creamy-white font-bold text-xl shadow-lg shadow-primary/20">
                R
              </div>
              <span className="font-display font-bold text-xl tracking-tight text-creamy-white group-hover:text-accent transition-colors">
                REORCH
              </span>
            </a>
            <div className="hidden md:flex items-center gap-6 text-sm font-medium text-creamy-white/50">
              <a className="hover:text-accent transition-colors" href="#features">
                Features
              </a>
              <a
                className="hover:text-accent transition-colors"
                href="#how-it-works"
              >
                How It Works
              </a>
              <a className="hover:text-accent transition-colors" href="#use-cases">
                Use Cases
              </a>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-sm font-medium hover:text-accent transition-colors text-creamy-white/70 cursor-pointer">
              Sign In
            </button>
            <button className="bg-primary hover:bg-primary/90 text-creamy-white px-5 py-2.5 rounded text-sm font-semibold transition-all shadow-lg shadow-primary/30 cursor-pointer">
              Try REORCH
            </button>
          </div>
        </nav>
      </header>
      <main>
        <section className="relative min-h-screen flex items-center justify-center pt-20 pb-20 overflow-hidden hero-gradient">
          <div className="absolute inset-0 waveform-bg pointer-events-none"></div>
          <div className="max-w-7xl mx-auto px-6 text-center relative z-10">
            <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-1.5 rounded-full text-xs font-mono tracking-wider text-creamy-white/50 mb-8">
              <span className="w-2 h-2 bg-accent rounded-full animate-pulse"></span>
              AI-POWERED ARRANGEMENT ENGINE
            </div>
            <h1 className="text-5xl md:text-7xl font-display font-extrabold text-creamy-white leading-[1.1] mb-6">
              Rebuild Your Music.<br />
              <span className="bg-gradient-to-r from-accent to-primary bg-clip-text text-transparent">
                Transform Every Layer.
              </span>
            </h1>
            <p className="max-w-2xl mx-auto text-lg text-creamy-white/50 mb-10 leading-relaxed">
              REORCH is an AI re-orchestration platform that transforms existing
              songs into new genres and generates original compositions—with
              full arrangement-level control.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-creamy-white px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 group transition-all shadow-xl shadow-primary/20 cursor-pointer">
                Transform a Song{" "}
                <span className="material-symbols-outlined text-sm group-hover:translate-x-1 transition-transform">
                  arrow_forward
                </span>
              </button>
              <button className="w-full sm:w-auto glass-card text-creamy-white px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 hover:bg-creamy-white/10 transition-all cursor-pointer">
                <span className="material-symbols-outlined text-xl">
                  play_circle
                </span>{" "}
                See How It Works
              </button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-24 max-w-4xl mx-auto border-t border-creamy-white/5 pt-12">
              <div>
                <div className="text-3xl font-display font-bold text-creamy-white">
                  50+
                </div>
                <div className="text-xs font-mono uppercase tracking-widest text-creamy-white/40 mt-1">
                  Genre Presets
                </div>
              </div>
              <div>
                <div className="text-3xl font-display font-bold text-creamy-white">
                  Pro
                </div>
                <div className="text-xs font-mono uppercase tracking-widest text-creamy-white/40 mt-1">
                  Audio Quality
                </div>
              </div>
              <div>
                <div className="text-3xl font-display font-bold text-creamy-white">
                  Real
                </div>
                <div className="text-xs font-mono uppercase tracking-widest text-creamy-white/40 mt-1">
                  Audio Processing
                </div>
              </div>
              <div>
                <div className="text-3xl font-display font-bold text-creamy-white">
                  Full
                </div>
                <div className="text-xs font-mono uppercase tracking-widest text-creamy-white/40 mt-1">
                  Arrangement Control
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="py-24 bg-background-dark border-y border-creamy-white/5">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-20">
              <div className="text-accent font-mono text-sm tracking-widest uppercase mb-3">
                {"// CAPABILITIES"}
              </div>
              <h2 className="text-3xl md:text-4xl font-display font-bold text-creamy-white mb-4">
                What REORCH Does
              </h2>
              <p className="text-creamy-white/50">
                More than generation—this is transformation at the arrangement
                level.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="glass-card p-8 rounded-xl group hover:border-primary/50 transition-all">
                <div className="w-12 h-12 rounded bg-primary/10 flex items-center justify-center mb-6 text-primary group-hover:text-accent transition-colors">
                  <span className="material-symbols-outlined">upload_file</span>
                </div>
                <div className="text-xs font-mono text-creamy-white/30 mb-2">
                  01
                </div>
                <h3 className="text-xl font-bold text-creamy-white mb-4">
                  Upload & Re-orchestrate
                </h3>
                <p className="text-sm leading-relaxed text-creamy-white/50">
                  Drop an existing track and transform it into an entirely new
                  genre. Turn your ballad into rock, your acoustic into
                  electronic—without losing the soul of the original.
                </p>
              </div>
              <div className="glass-card p-8 rounded-xl group hover:border-primary/50 transition-all">
                <div className="w-12 h-12 rounded bg-primary/10 flex items-center justify-center mb-6 text-primary group-hover:text-accent transition-colors">
                  <span className="material-symbols-outlined">
                    auto_fix_high
                  </span>
                </div>
                <div className="text-xs font-mono text-creamy-white/30 mb-2">
                  02
                </div>
                <h3 className="text-xl font-bold text-creamy-white mb-4">
                  Generate & Refine
                </h3>
                <p className="text-sm leading-relaxed text-creamy-white/50">
                  Start from scratch with AI-assisted composition, then shape
                  and re-orchestrate the output until it matches your creative
                  vision perfectly.
                </p>
              </div>
              <div className="glass-card p-8 rounded-xl group hover:border-primary/50 transition-all">
                <div className="w-12 h-12 rounded bg-primary/10 flex items-center justify-center mb-6 text-primary group-hover:text-accent transition-colors">
                  <span className="material-symbols-outlined">sync</span>
                </div>
                <div className="text-xs font-mono text-creamy-white/30 mb-2">
                  03
                </div>
                <h3 className="text-xl font-bold text-creamy-white mb-4">
                  Iterate & Perfect
                </h3>
                <p className="text-sm leading-relaxed text-creamy-white/50">
                  Every transformation can be further refined. Stack
                  re-orchestrations, adjust arrangements, and push your music in
                  entirely new creative directions.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section className="py-24 bg-background-dark" id="how-it-works">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-20">
              <div className="text-primary font-mono text-sm tracking-widest uppercase mb-3">
                {"// PIPELINE"}
              </div>
              <h2 className="text-3xl md:text-4xl font-display font-bold text-creamy-white mb-4">
                How It Works
              </h2>
              <p className="text-creamy-white/50">
                A production-grade pipeline from input to final output.
              </p>
            </div>
            <div className="relative max-w-5xl mx-auto">
              <div className="hidden md:block absolute top-10 left-0 right-0 h-px bg-creamy-white/10 z-0"></div>
              <div className="grid md:grid-cols-3 gap-12 relative z-10">
                <div className="text-center">
                  <div className="w-20 h-20 bg-background-dark border-2 border-primary text-primary mx-auto flex items-center justify-center font-mono font-bold text-xl mb-6 shadow-[0_0_20px_rgba(46,125,50,0.3)]">
                    01
                  </div>
                  <h3 className="font-bold text-creamy-white mb-3">Analyze</h3>
                  <p className="text-sm text-creamy-white/50 px-4">
                    Your audio is parsed into stems, structure, and musical
                    elements. We identify melodies, harmonies, and dynamics.
                  </p>
                </div>
                <div className="text-center">
                  <div className="w-20 h-20 bg-background-dark border-2 border-accent text-accent mx-auto flex items-center justify-center font-mono font-bold text-xl mb-6 shadow-[0_0_20px_rgba(255,193,7,0.3)]">
                    02
                  </div>
                  <h3 className="font-bold text-creamy-white mb-3">
                    Re-orchestrate
                  </h3>
                  <p className="text-sm text-creamy-white/50 px-4">
                    The AI rebuilds your arrangement in the target genre,
                    replacing instruments and adjusting voicings.
                  </p>
                </div>
                <div className="text-center">
                  <div className="w-20 h-20 bg-background-dark border-2 border-primary/40 text-primary/60 mx-auto flex items-center justify-center font-mono font-bold text-xl mb-6">
                    03
                  </div>
                  <h3 className="font-bold text-creamy-white mb-3">
                    Mix & Master
                  </h3>
                  <p className="text-sm text-creamy-white/50 px-4">
                    Professional-grade processing ensures your transformed track
                    is production-ready with balanced levels.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="py-24 bg-surface/30 overflow-hidden">
          <div className="max-w-7xl mx-auto px-6">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              <div>
                <div className="text-accent font-mono text-sm tracking-widest uppercase mb-3">
                  {"// DIFFERENTIATORS"}
                </div>
                <h2 className="text-3xl md:text-5xl font-display font-bold text-creamy-white mb-6">
                  Why REORCH Is Different
                </h2>
                <p className="text-creamy-white/50 mb-12 text-lg">
                  Most AI music tools generate from scratch or apply
                  surface-level changes. REORCH goes deeper—rebuilding
                  arrangements at the structural level while respecting the
                  integrity of your work.
                </p>
                <div className="space-y-8">
                  <div className="flex gap-4">
                    <div className="shrink-0 w-10 h-10 glass-card rounded flex items-center justify-center text-primary">
                      <span className="material-symbols-outlined">layers</span>
                    </div>
                    <div>
                      <h4 className="font-bold text-creamy-white mb-1">
                        Arrangement-Level Control
                      </h4>
                      <p className="text-sm text-creamy-white/50">
                        Unlike simple AI generators, REORCH operates on the
                        structure of your music—transforming how instruments
                        interact, not just adding effects.
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="shrink-0 w-10 h-10 glass-card rounded flex items-center justify-center text-accent">
                      <span className="material-symbols-outlined">
                        equalizer
                      </span>
                    </div>
                    <div>
                      <h4 className="font-bold text-creamy-white mb-1">
                        Real Audio Processing
                      </h4>
                      <p className="text-sm text-creamy-white/50">
                        This isn&apos;t text-to-audio guesswork. We analyze and
                        rebuild actual audio signals, preserving musical intent
                        while reshaping the arrangement.
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="shrink-0 w-10 h-10 glass-card rounded flex items-center justify-center text-primary/70">
                      <span className="material-symbols-outlined">
                        precision_manufacturing
                      </span>
                    </div>
                    <div>
                      <h4 className="font-bold text-creamy-white mb-1">
                        Production-Grade Pipeline
                      </h4>
                      <p className="text-sm text-creamy-white/50">
                        Built for professionals. Our processing chain maintains
                        audio fidelity throughout, delivering results ready for
                        release.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="glass-card rounded-2xl p-10 border-creamy-white/5 relative">
                <div className="flex items-center justify-between mb-10">
                  <span className="text-[10px] font-mono tracking-widest text-creamy-white/30 uppercase">
                    REORCH.ENGINE
                  </span>
                  <span className="text-[10px] font-mono tracking-widest text-creamy-white/30 uppercase">
                    V2.4.1
                  </span>
                </div>
                <div className="space-y-8">
                  <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-mono text-creamy-white/40">
                      <span>MELODY</span>
                      <span>84%</span>
                    </div>
                    <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-primary w-[84%] rounded-full shadow-[0_0_10px_rgba(46,125,50,0.5)]"></div>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-mono text-creamy-white/40">
                      <span>HARMONY</span>
                      <span>92%</span>
                    </div>
                    <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-accent w-[92%] rounded-full shadow-[0_0_10px_rgba(255,193,7,0.5)]"></div>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-mono text-creamy-white/40">
                      <span>RHYTHM</span>
                      <span>65%</span>
                    </div>
                    <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-primary/60 w-[65%] rounded-full"></div>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-mono text-creamy-white/40">
                      <span>DYNAMICS</span>
                      <span>78%</span>
                    </div>
                    <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-accent/60 w-[78%] rounded-full"></div>
                    </div>
                  </div>
                </div>
                <div className="mt-12 flex justify-between items-end">
                  <div className="flex gap-2">
                    <div className="w-1 h-8 bg-primary/20"></div>
                    <div className="w-1 h-12 bg-primary/40"></div>
                    <div className="w-1 h-6 bg-primary/30"></div>
                    <div className="w-1 h-10 bg-primary/60"></div>
                    <div className="w-1 h-4 bg-primary/20"></div>
                  </div>
                  <span className="text-[10px] font-mono text-accent animate-pulse">
                    PROCESSING...
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="py-24 bg-background-dark" id="use-cases">
          <div className="max-w-7xl mx-auto px-6 text-center">
            <div className="text-primary font-mono text-sm tracking-widest uppercase mb-3">
              {"// USE CASES"}
            </div>
            <h2 className="text-3xl md:text-4xl font-display font-bold text-creamy-white mb-4">
              Built For Creators
            </h2>
            <p className="text-creamy-white/50 mb-16">
              Whether you&apos;re composing, producing, or exploring—REORCH adapts to
              your workflow.
            </p>
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div className="glass-card p-10 rounded-xl hover:translate-y-[-4px] transition-all">
                <span className="material-symbols-outlined text-accent text-3xl mb-6">
                  music_note
                </span>
                <div className="text-[10px] font-mono text-creamy-white/30 mb-2 uppercase tracking-widest">
                  Musicians
                </div>
                <h4 className="text-xl font-bold text-creamy-white mb-4">
                  Explore New Arrangements
                </h4>
                <p className="text-sm text-creamy-white/50 leading-relaxed">
                  Hear your compositions reimagined in genres you&apos;d never
                  attempt manually. Discover what your ballad sounds like as
                  rock, or your folk tune as electronic.
                </p>
              </div>
              <div className="glass-card p-10 rounded-xl hover:translate-y-[-4px] transition-all">
                <span className="material-symbols-outlined text-primary text-3xl mb-6">
                  album
                </span>
                <div className="text-[10px] font-mono text-creamy-white/30 mb-2 uppercase tracking-widest">
                  Producers
                </div>
                <h4 className="text-xl font-bold text-creamy-white mb-4">
                  Create Alternate Versions
                </h4>
                <p className="text-sm text-creamy-white/50 leading-relaxed">
                  Generate radio edits, remix stems, or entirely new takes on
                  existing productions without starting from scratch.
                </p>
              </div>
              <div className="glass-card p-10 rounded-xl hover:translate-y-[-4px] transition-all">
                <span className="material-symbols-outlined text-accent text-3xl mb-6">
                  psychology
                </span>
                <div className="text-[10px] font-mono text-creamy-white/30 mb-2 uppercase tracking-widest">
                  Creators
                </div>
                <h4 className="text-xl font-bold text-creamy-white mb-4">
                  Experiment With Genres
                </h4>
                <p className="text-sm text-creamy-white/50 leading-relaxed">
                  Break out of creative ruts by transforming reference tracks.
                  Use AI to explore styles before committing to production.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section
          className="py-24 bg-surface/20 border-y border-creamy-white/5"
          id="features"
        >
          <div className="max-w-7xl mx-auto px-6">
            <div className="mb-16">
              <div className="text-accent font-mono text-sm tracking-widest uppercase mb-3">
                {"// FEATURES"}
              </div>
              <h2 className="text-3xl md:text-4xl font-display font-bold text-creamy-white">
                Feature Highlights
              </h2>
            </div>
            <div className="grid md:grid-cols-2 gap-px bg-creamy-white/5 border border-creamy-white/5 rounded-2xl overflow-hidden">
              <div className="p-10 bg-background-dark hover:bg-surface/40 transition-colors group">
                <div className="w-10 h-10 rounded bg-primary/10 flex items-center justify-center text-primary mb-6">
                  <span className="material-symbols-outlined">tune</span>
                </div>
                <h4 className="font-bold text-creamy-white mb-2">
                  Genre Transformation Presets
                </h4>
                <p className="text-sm text-creamy-white/50">
                  50+ professionally designed presets spanning rock, electronic,
                  jazz, orchestral, and more. Each tuned for musical accuracy.
                </p>
              </div>
              <div className="p-10 bg-background-dark hover:bg-surface/40 transition-colors group">
                <div className="w-10 h-10 rounded bg-accent/10 flex items-center justify-center text-accent mb-6">
                  <span className="material-symbols-outlined">
                    temp_preferences_custom
                  </span>
                </div>
                <h4 className="font-bold text-creamy-white mb-2">
                  AI-Assisted Generation
                </h4>
                <p className="text-sm text-creamy-white/50">
                  Start from a prompt or mood, generate original compositions,
                  then transform them through the re-orchestration pipeline.
                </p>
              </div>
              <div className="p-10 bg-background-dark hover:bg-surface/40 transition-colors group">
                <div className="w-10 h-10 rounded bg-primary/10 flex items-center justify-center text-primary mb-6">
                  <span className="material-symbols-outlined">schedule</span>
                </div>
                <h4 className="font-bold text-creamy-white mb-2">
                  Background Processing
                </h4>
                <p className="text-sm text-creamy-white/50">
                  Complex transformations run as background jobs with real-time
                  progress tracking. Get notified when your track is ready.
                </p>
              </div>
              <div className="p-10 bg-background-dark hover:bg-surface/40 transition-colors group">
                <div className="w-10 h-10 rounded bg-accent/10 flex items-center justify-center text-accent mb-6">
                  <span className="material-symbols-outlined">
                    verified_user
                  </span>
                </div>
                <h4 className="font-bold text-creamy-white mb-2">
                  Quality Assurance
                </h4>
                <p className="text-sm text-creamy-white/50">
                  Automated analysis ensures consistent output quality. Clear
                  feedback on processing results and any detected issues.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section className="py-24 bg-background-dark">
          <div className="max-w-7xl mx-auto px-6 text-center">
            <div className="text-primary font-mono text-sm tracking-widest uppercase mb-3">
              {"// TRUST"}
            </div>
            <h2 className="text-3xl md:text-4xl font-display font-bold text-creamy-white mb-4">
              Built for Quality
            </h2>
            <p className="text-creamy-white/50 mb-16">
              Professional tools deserve professional standards.
            </p>
            <div className="grid md:grid-cols-3 gap-12">
              <div>
                <div className="w-12 h-12 glass-card rounded-lg flex items-center justify-center text-accent mx-auto mb-6">
                  <span className="material-symbols-outlined">shield</span>
                </div>
                <h4 className="font-bold text-creamy-white mb-3">Audio Integrity</h4>
                <p className="text-sm text-creamy-white/50">
                  We preserve the musical essence of your original work.
                  Transformations are meaningful, not destructive.
                </p>
              </div>
              <div>
                <div className="w-12 h-12 glass-card rounded-lg flex items-center justify-center text-primary mx-auto mb-6">
                  <span className="material-symbols-outlined">visibility</span>
                </div>
                <h4 className="font-bold text-creamy-white mb-3">
                  Transparent Limitations
                </h4>
                <p className="text-sm text-creamy-white/50">
                  No overpromises. We&apos;re upfront about what works well and where
                  current technology has constraints.
                </p>
              </div>
              <div>
                <div className="w-12 h-12 glass-card rounded-lg flex items-center justify-center text-accent mx-auto mb-6">
                  <span className="material-symbols-outlined">bolt</span>
                </div>
                <h4 className="font-bold text-creamy-white mb-3">
                  Consistent Quality
                </h4>
                <p className="text-sm text-creamy-white/50">
                  Production-ready output every time. Our pipeline is tested
                  against thousands of tracks across genres.
                </p>
              </div>
            </div>
          </div>
        </section>
        <section className="py-24">
          <div className="max-w-5xl mx-auto px-6">
            <div className="relative bg-surface border-2 border-primary/20 p-12 md:p-20 text-center overflow-hidden rounded-xl">
              <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-accent"></div>
              <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-accent"></div>
              <h2 className="text-3xl md:text-5xl font-display font-extrabold text-creamy-white mb-6 relative z-10">
                Rebuild Your Music with REORCH
              </h2>
              <p className="text-creamy-white/50 mb-10 max-w-xl mx-auto relative z-10">
                Transform your tracks, explore new genres, and push your
                creative boundaries.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 relative z-10">
                <button className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-creamy-white px-8 py-4 rounded-lg font-bold flex items-center justify-center gap-2 transition-all shadow-xl shadow-primary/30 cursor-pointer">
                  Get Started{" "}
                  <span className="material-symbols-outlined text-sm">
                    arrow_forward
                  </span>
                </button>
                <button className="w-full sm:w-auto glass-card text-creamy-white px-8 py-4 rounded-lg font-bold border-creamy-white/20 hover:bg-creamy-white/10 transition-all cursor-pointer">
                  View Documentation
                </button>
              </div>
              <p className="text-[10px] text-creamy-white/40 font-mono mt-8 uppercase tracking-widest">
                Free tier available. No credit card required.
              </p>
            </div>
          </div>
        </section>
      </main>
      <footer className="bg-background-dark border-t border-creamy-white/5 py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-primary rounded flex items-center justify-center text-creamy-white font-bold text-xs">
              R
            </div>
            <span className="font-display font-bold text-lg text-creamy-white uppercase tracking-tighter">
              REORCH
            </span>
          </div>
          <div className="flex items-center gap-8 text-sm text-creamy-white/40">
            <a className="hover:text-accent transition-colors" href="#">
              Documentation
            </a>
            <a className="hover:text-accent transition-colors" href="#">
              Pricing
            </a>
            <a className="hover:text-accent transition-colors" href="#">
              Privacy
            </a>
            <a className="hover:text-accent transition-colors" href="#">
              Terms
            </a>
          </div>
          <div className="text-xs font-mono text-creamy-white/20">
            © 2024 REORCH. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
