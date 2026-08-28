'use client';

import Link from 'next/link';
import { ArrowRight, TrendingUp, Anchor, Bot, Shield, BarChart3, Clock } from 'lucide-react';
import ForecastChart from '@/components/ForecastChart';
import { Hexagon } from 'lucide-react';

const features = [
  {
    icon: TrendingUp,
    title: 'Quantile Engine',
    description: 'State-of-the-art quantile forecasting model evaluating 1-day, 1-month, and 3-month horizons for Brent and WTI.',
  },
  {
    icon: Anchor,
    title: 'Maritime Chokepoints',
    description: 'Real-time monitoring of global transit corridors to preempt supply chain delays.',
  },
  {
    icon: Bot,
    title: 'Autonomous Co-Pilot',
    description: 'ReAct-based intelligence agent that dynamically fetches market telemetry and formulates action plans.',
  },
  {
    icon: Shield,
    title: 'Risk Exposure Control',
    description: 'Maximum risk exposure quantification across volatile energy markets.',
  },
  {
    icon: BarChart3,
    title: 'Live Telemetry',
    description: 'Real-time dashboard syncing global commodities and macroeconomic markers.',
  },
  {
    icon: Clock,
    title: 'Predictive Defense',
    description: 'Detect anomalies in energy prices before they propagate downstream.',
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary/30 relative overflow-hidden">
      {/* Animated Aurora Background Elements */}
      <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vh] rounded-full bg-primary/20 blur-[100px] animate-blob mix-blend-screen pointer-events-none" />
      <div className="absolute top-[20%] right-[-10%] w-[40vw] h-[60vh] rounded-full bg-accent/20 blur-[100px] animate-blob animation-delay-2000 mix-blend-screen pointer-events-none" />
      <div className="absolute bottom-[-20%] left-[20%] w-[60vw] h-[50vh] rounded-full bg-blue-500/20 blur-[100px] animate-blob animation-delay-4000 mix-blend-screen pointer-events-none" />

      {/* Background grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none" />

      {/* Header */}
      <header className="relative z-10 border-b border-border/50 bg-background/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3 h-full">
              <Hexagon className="h-8 w-8 text-primary fill-primary/20" />
              <span className="font-bold text-xl tracking-tight">Petrocast Resilience</span>
            </div>
            <Link href="/console">
              <button className="bg-transparent border border-border/50 hover:bg-muted px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center">
                Open Console
                <ArrowRight className="ml-2 h-4 w-4" />
              </button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
            {/* Left: Copy */}
            <div className="space-y-8">
              <div className="space-y-4">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-sm text-emerald-400">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
                  </span>
                  Pipeline Active
                </div>
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight leading-tight">
                  Crude{' '}
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
                    Intelligence
                  </span>
                </h1>
                <p className="text-lg sm:text-xl text-muted-foreground max-w-xl">
                  AI-powered procurement forecasting and maritime resilience. Transform uncertainty into actionable decisions with quantile predictions and an autonomous co-pilot.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/console" className="flex-1 sm:flex-none">
                  <button className="w-full sm:w-auto bg-primary hover:bg-primary/90 text-primary-foreground px-6 py-3 rounded-lg font-medium transition-colors flex items-center justify-center text-lg shadow-lg shadow-primary/25">
                    Open Procurement Console
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </button>
                </Link>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 pt-4">
                <div>
                  <div className="text-2xl sm:text-3xl font-bold text-foreground">3</div>
                  <div className="text-sm text-muted-foreground">Forecast Horizons</div>
                </div>
                <div>
                  <div className="text-2xl sm:text-3xl font-bold text-foreground">5</div>
                  <div className="text-sm text-muted-foreground">Tool Integrations</div>
                </div>
                <div>
                  <div className="text-2xl sm:text-3xl font-bold text-foreground">24/7</div>
                  <div className="text-sm text-muted-foreground">Autonomous Engine</div>
                </div>
              </div>
            </div>

            {/* Right: Probability Cone Preview */}
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-accent/20 rounded-2xl blur-3xl pointer-events-none" />
              <div className="relative pointer-events-none scale-90 origin-top lg:scale-100">
                {/* Re-using the ForecastChart, but wrapped nicely */}
                <ForecastChart />
              </div>
            </div>
          </div>

          {/* Features Grid */}
          <div className="mt-24 lg:mt-32">
            <div className="text-center mb-12">
              <h2 className="text-2xl sm:text-3xl font-bold">Built for Strategic Procurement</h2>
              <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">
                A complete forecasting pipeline optimized for navigating supply chain disruptions.
              </p>
            </div>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature) => (
                <div
                  key={feature.title}
                  className="group p-6 rounded-xl border border-border/50 bg-card/50 hover:bg-card hover:border-border transition-all duration-200"
                >
                  <div className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center mb-4 group-hover:bg-primary/10 transition-colors">
                    <feature.icon className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
                  </div>
                  <h3 className="font-semibold mb-2">{feature.title}</h3>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
