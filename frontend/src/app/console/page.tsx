"use client";

import DashboardGrid from '@/components/DashboardGrid';
import ForecastChart from '@/components/ForecastChart';
import AgentChat from '@/components/AgentChat';
import { Hexagon, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function ConsolePage() {
  return (
    <div className="min-h-screen bg-background relative overflow-x-hidden">
      {/* Animated Aurora Background Elements */}
      <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vh] rounded-full bg-primary/20 blur-[100px] animate-blob mix-blend-screen pointer-events-none" />
      <div className="absolute top-[20%] right-[-10%] w-[40vw] h-[60vh] rounded-full bg-accent/20 blur-[100px] animate-blob animation-delay-2000 mix-blend-screen pointer-events-none" />
      <div className="absolute bottom-[-20%] left-[20%] w-[60vw] h-[50vh] rounded-full bg-blue-500/20 blur-[100px] animate-blob animation-delay-4000 mix-blend-screen pointer-events-none" />

      {/* Grid Background */}
      <div className="fixed inset-0 grid-background opacity-20 pointer-events-none" />
      <div className="fixed inset-0 bg-gradient-to-b from-transparent via-background/50 to-background pointer-events-none" />

      <div className="relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          
          {/* Header */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 pb-6 border-b border-border/50 gap-4">
            <div className="flex items-center gap-4">
              <Link href="/">
                <button className="flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors px-3 py-1.5 rounded-md hover:bg-muted cursor-pointer">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back
                </button>
              </Link>
              <div className="h-6 w-px bg-border hidden sm:block" />
              <div className="flex items-center gap-3">
                <Hexagon className="h-8 w-8 text-primary fill-primary/20" />
                <span className="font-semibold text-lg text-foreground tracking-tight leading-none">Petrocast Resilience</span>
                <span className="font-semibold text-lg text-muted-foreground leading-none">| Console</span>
              </div>
            </div>

            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-sm">
              <span className="relative flex h-2 w-2 mr-1">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              Pipeline Live
            </div>
          </div>

          {/* Main Grid */}
          <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
            <div className="xl:col-span-8 flex flex-col gap-8">
              <ForecastChart />
              <DashboardGrid />
            </div>
            <div className="xl:col-span-4 min-h-[600px]">
              <AgentChat />
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
