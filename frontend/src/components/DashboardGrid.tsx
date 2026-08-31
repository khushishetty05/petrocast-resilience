"use client";
import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { Activity, Anchor, Navigation } from 'lucide-react';

export default function DashboardGrid() {
  const [markets, setMarkets] = useState<any[]>([]);
  const [chokepoints, setChokepoints] = useState<any[]>([]);

  useEffect(() => {
    api.get('/market/live')
      .then(res => setMarkets(Array.isArray(res.data) ? res.data : (res.data.tickers || [])))
      .catch(console.error);
      
    api.get('/chokepoints/live')
      .then(res => {
        if (res.data) {
          setChokepoints(Array.isArray(res.data) ? res.data : []);
        } else {
          setChokepoints([]);
        }
      })
      .catch(console.error);
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      
      {/* Market Telemetry */}
      <div className="relative border border-border/50 rounded-2xl bg-card/80 backdrop-blur-sm overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b border-border/50 flex items-center justify-between bg-muted/30">
          <div className="flex items-center gap-2">
            <Activity className="h-4 w-4 text-primary" />
            <span className="text-sm font-medium">Market Telemetry</span>
          </div>
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
          </span>
        </div>
        <div className="p-4 grid grid-cols-2 gap-4 flex-1">
          {markets.map(m => (
            <div key={m.symbol} className="bg-background/50 border border-border/50 p-4 rounded-xl flex flex-col justify-center">
              <p className="text-muted-foreground text-xs font-mono uppercase tracking-wider mb-1">{m.symbol}</p>
              <p className="text-2xl font-bold text-foreground">${m.price?.toFixed(2)}</p>
            </div>
          ))}
          {markets.length === 0 && <p className="text-muted-foreground text-sm col-span-2 text-center my-auto">Pipeline Offline</p>}
        </div>
      </div>
      
      {/* Maritime Corridors */}
      <div className="relative border border-border/50 rounded-2xl bg-card/80 backdrop-blur-sm overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b border-border/50 flex items-center justify-between bg-muted/30">
          <div className="flex items-center gap-2">
            <Navigation className="h-4 w-4 text-accent" />
            <span className="text-sm font-medium">Maritime Corridors</span>
          </div>
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-accent"></span>
          </span>
        </div>
        <div className="p-4 space-y-3 flex-1 overflow-y-auto max-h-[300px]">
          {chokepoints.map(c => {
            const isHighRisk = c.current_risk_score > 5;
            return (
              <div key={c.name} className="flex justify-between items-center bg-background/50 border border-border/50 p-3 rounded-lg group hover:border-border transition-colors">
                <div className="flex items-center gap-3">
                  <div className={`p-1.5 rounded-md ${isHighRisk ? 'bg-destructive/10' : 'bg-emerald-500/10'}`}>
                    <Anchor className={`w-3.5 h-3.5 ${isHighRisk ? 'text-destructive' : 'text-emerald-500'}`} />
                  </div>
                  <span className="text-foreground text-sm font-medium">{c.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className={`h-1.5 w-16 rounded-full overflow-hidden bg-muted`}>
                    <div className={`h-full ${isHighRisk ? 'bg-destructive' : 'bg-emerald-500'}`} style={{ width: `${(c.current_risk_score / 10) * 100}%` }}></div>
                  </div>
                  <span className="text-xs font-mono font-medium text-muted-foreground w-6 text-right">{c.current_risk_score?.toFixed(1)}</span>
                </div>
              </div>
            );
          })}
          {chokepoints.length === 0 && <p className="text-muted-foreground text-sm text-center my-auto pt-8">Pipeline Offline</p>}
        </div>
      </div>

    </div>
  );
}
