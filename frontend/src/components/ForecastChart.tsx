"use client";
import { useEffect, useState } from 'react';
import api from '@/lib/api';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, AlertOctagon, Target, ArrowDownCircle } from 'lucide-react';

export default function ForecastChart() {
  const [symbol, setSymbol] = useState<'Brent' | 'WTI'>('Brent');
  const [horizon, setHorizon] = useState<'1D' | '1M' | '3M'>('1M');
  const [data, setData] = useState<any[]>([]);
  const [rawForecast, setRawForecast] = useState<any>(null);

  useEffect(() => {
    api.get(`/forecast/latest/${symbol}`).then(res => {
      const f = res.data;
      setRawForecast(f);
      setData([
        { horizon: 'Current', p10: f.base_price, p50: f.base_price, p90: f.base_price, range: [f.base_price, f.base_price] },
        { horizon: '1 Day', p10: f.pred_1d_10th, p50: f.pred_1d_50th, p90: f.pred_1d_90th, range: [f.pred_1d_10th, f.pred_1d_90th] },
        { horizon: '1 Month', p10: f.pred_1m_10th, p50: f.pred_1m_50th, p90: f.pred_1m_90th, range: [f.pred_1m_10th, f.pred_1m_90th] },
        { horizon: '3 Months', p10: f.pred_3m_10th, p50: f.pred_3m_50th, p90: f.pred_3m_90th, range: [f.pred_3m_10th, f.pred_3m_90th] }
      ]);
    }).catch(console.error);
  }, [symbol]);

  const getCurrentMetrics = () => {
    if (!rawForecast) return { p10: 0, p50: 0, p90: 0 };
    if (horizon === '1D') return { p10: rawForecast.pred_1d_10th, p50: rawForecast.pred_1d_50th, p90: rawForecast.pred_1d_90th };
    if (horizon === '1M') return { p10: rawForecast.pred_1m_10th, p50: rawForecast.pred_1m_50th, p90: rawForecast.pred_1m_90th };
    return { p10: rawForecast.pred_3m_10th, p50: rawForecast.pred_3m_50th, p90: rawForecast.pred_3m_90th };
  };

  const metrics = getCurrentMetrics();

  return (
    <div className="flex flex-col gap-6 w-full pointer-events-auto">
      {/* Banner & Toggles */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center bg-card border border-border/50 rounded-xl p-4 gap-4 shadow-md backdrop-blur-sm">
        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <div className="bg-amber-500/10 text-amber-500 px-4 py-2.5 rounded-lg border border-amber-500/20 flex items-center gap-2">
            <AlertOctagon className="w-5 h-5" />
            <div className="flex flex-col">
              <span className="text-[10px] uppercase font-bold tracking-wider opacity-80">Strategic Action</span>
              <span className="text-sm font-semibold tracking-tight">STAGGER PROCUREMENT</span>
            </div>
          </div>
          
          <div className="flex bg-muted p-1 rounded-lg border border-border/50">
            <button onClick={() => setSymbol('Brent')} className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${symbol === 'Brent' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}>BRENT</button>
            <button onClick={() => setSymbol('WTI')} className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${symbol === 'WTI' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}>WTI</button>
          </div>
        </div>

        <div className="flex bg-muted p-1 rounded-lg border border-border/50">
          <button onClick={() => setHorizon('1D')} className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${horizon === '1D' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}>1-Day</button>
          <button onClick={() => setHorizon('1M')} className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${horizon === '1M' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}>1-Month</button>
          <button onClick={() => setHorizon('3M')} className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${horizon === '3M' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'}`}>3-Month</button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-card border border-destructive/30 rounded-xl p-5 relative overflow-hidden shadow-sm hover:border-destructive/50 transition-colors">
          <div className="absolute top-0 right-0 w-32 h-32 bg-destructive/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
          <div className="flex items-center gap-2 mb-2">
            <div className="w-8 h-8 rounded-lg bg-destructive/10 flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-destructive" />
            </div>
            <h3 className="text-muted-foreground text-sm font-medium">Maximum Risk (p90)</h3>
          </div>
          <p className="text-3xl font-bold text-foreground mt-2">${metrics.p90.toFixed(2)}</p>
        </div>
        
        <div className="bg-card border border-primary/30 rounded-xl p-5 relative overflow-hidden shadow-sm hover:border-primary/50 transition-colors">
          <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
          <div className="flex items-center gap-2 mb-2">
            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <Target className="w-4 h-4 text-primary" />
            </div>
            <h3 className="text-muted-foreground text-sm font-medium">Expected Baseline (p50)</h3>
          </div>
          <p className="text-3xl font-bold text-foreground mt-2">${metrics.p50.toFixed(2)}</p>
        </div>

        <div className="bg-card border border-emerald-500/30 rounded-xl p-5 relative overflow-hidden shadow-sm hover:border-emerald-500/50 transition-colors">
          <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>
          <div className="flex items-center gap-2 mb-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center">
              <ArrowDownCircle className="w-4 h-4 text-emerald-400" />
            </div>
            <h3 className="text-muted-foreground text-sm font-medium">Optimal Buying Zone (p10)</h3>
          </div>
          <p className="text-3xl font-bold text-foreground mt-2">${metrics.p10.toFixed(2)}</p>
        </div>
      </div>

      {/* Chart */}
      <div className="relative border border-border/50 rounded-2xl bg-card/80 backdrop-blur-sm overflow-hidden h-[360px]">
        <div className="px-4 py-3 border-b border-border/50 flex items-center justify-between">
          <span className="text-sm font-medium">{symbol} Probability Cone</span>
          <span className="text-xs text-muted-foreground">Live Quantile Prediction</span>
        </div>
        <div className="w-full" style={{ height: 315 }}>
          {data.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="quantileGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#38bdf8" stopOpacity={0.25}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#1e293b" />
                <XAxis dataKey="horizon" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis domain={['auto', 'auto']} stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} tickFormatter={(value) => `$${value.toFixed(0)}`} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'hsl(var(--color-popover))', border: '1px solid hsl(var(--color-border))', borderRadius: '8px', color: 'hsl(var(--color-popover-foreground))' }} 
                  itemStyle={{ color: 'hsl(var(--color-foreground))' }}
                  formatter={(value: any, name: string) => {
                    if (name === "range" && Array.isArray(value)) return [`$${value[0].toFixed(2)} - $${value[1].toFixed(2)}`, 'p10 - p90 Range'];
                    if (name === "p50") return [`$${Number(value).toFixed(2)}`, 'p50 Base'];
                    return [value, name];
                  }}
                />
                
                {/* Upper and lower bounds for p90 and p10 dashed lines */}
                <Area type="monotone" dataKey="p90" stroke="#93c5fd" strokeDasharray="3 3" fill="none" />
                <Area type="monotone" dataKey="p10" stroke="#93c5fd" strokeDasharray="3 3" fill="none" />
                
                {/* Quantile Area */}
                <Area type="monotone" dataKey="range" stroke="none" fill="url(#quantileGradient)" />
                
                {/* Center Baseline */}
                <Area type="monotone" dataKey="p50" stroke="#38bdf8" strokeWidth={2.5} fill="none" activeDot={{ r: 6, fill: '#38bdf8', strokeWidth: 0 }} />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-muted-foreground text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                Calculating Neural Probabilities...
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
