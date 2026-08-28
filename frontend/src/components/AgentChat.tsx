"use client";
import { useState, useRef, useEffect } from 'react';
import api from '@/lib/api';
import { Send, Terminal, Loader2, Sparkles, Code2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function AgentChat() {
  const [msg, setMsg] = useState("");
  const [log, setLog] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [log, loading]);

  const handleSend = async () => {
    if(!msg.trim()) return;
    setLog(prev => [...prev, { role: 'user', content: msg }]);
    setMsg("");
    setLoading(true);
    try {
      const res = await api.post('/agent/chat', { message: msg });
      setLog(prev => [...prev, { role: 'agent', content: res.data.response, tools: res.data.tool_calls_executed }]);
    } catch(e: any) {
      setLog(prev => [...prev, { role: 'agent', content: "SYSTEM ERR: " + e.message }]);
    }
    setLoading(false);
  };

  return (
    <div className="relative border border-border/50 rounded-2xl bg-card/80 backdrop-blur-sm flex flex-col h-full shadow-xl overflow-hidden">
      
      {/* Terminal Header */}
      <div className="px-4 py-3 border-b border-border/50 flex items-center justify-between bg-muted/30">
        <div className="flex items-center gap-2">
          <Terminal className="h-4 w-4 text-primary" />
          <span className="text-sm font-medium">Petrocast Orchestrator</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-2.5 h-2.5 rounded-full bg-destructive/80" />
          <div className="w-2.5 h-2.5 rounded-full bg-accent/80" />
          <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
        </div>
      </div>
      
      {/* Terminal Body */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-6 font-sans">
        
        {/* Welcome Message */}
        <div className="flex justify-start">
          <div className="max-w-[90%] bg-muted/30 rounded-xl p-4 border border-border/50">
            <div className="flex items-center gap-2 mb-2 text-primary font-medium">
              <Sparkles className="w-4 h-4" /> Petrocast Co-Pilot
            </div>
            <p className="text-sm text-foreground leading-relaxed">
              System online. Connected to global market data, maritime routing, and procurement APIs. Ready for query.
            </p>
          </div>
        </div>

        {log.map((entry, i) => (
          <div key={i} className={`flex ${entry.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[90%] rounded-xl p-4 border ${entry.role === 'user' ? 'bg-primary/10 border-primary/20 text-foreground shadow-sm' : 'bg-muted/30 border-border/50 text-foreground'}`}>
              
              {entry.tools && entry.tools.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-3 pb-3 border-b border-border/50">
                  {entry.tools.map((t: string, j: number) => (
                    <span key={j} className="text-[10px] uppercase font-mono bg-background border border-border text-muted-foreground px-2 py-1 rounded-md flex items-center gap-1.5 shadow-sm">
                      <Code2 className="w-3 h-3 text-primary" /> {t}
                    </span>
                  ))}
                </div>
              )}
              
              <div className="text-sm leading-relaxed prose prose-invert max-w-none prose-p:my-2 prose-ul:my-2 prose-li:my-0 prose-headings:my-2 prose-strong:text-primary">
                {entry.role === 'user' ? (
                  <div className="whitespace-pre-wrap">{entry.content}</div>
                ) : (
                  <ReactMarkdown>{entry.content}</ReactMarkdown>
                )}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-muted/30 border border-border/50 rounded-xl p-4 text-sm text-muted-foreground flex items-center gap-3 shadow-sm">
              <Loader2 className="w-4 h-4 text-primary animate-spin" />
              Running execution trace...
            </div>
          </div>
        )}
      </div>

      {/* Terminal Input */}
      <div className="p-4 bg-muted/20 border-t border-border/50">
        <div className="relative flex items-center">
          <span className="absolute left-4 text-primary font-mono font-bold text-sm">{'>'}</span>
          <input 
            type="text" 
            value={msg}
            onChange={e => setMsg(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Initialize command..."
            className="w-full bg-background border border-border text-foreground font-mono text-sm rounded-xl pl-10 pr-12 py-3.5 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary/50 transition-all placeholder:text-muted-foreground shadow-inner"
          />
          <button 
            onClick={handleSend} 
            disabled={loading || !msg.trim()} 
            className="absolute right-2 bg-primary hover:bg-primary/90 text-primary-foreground p-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
