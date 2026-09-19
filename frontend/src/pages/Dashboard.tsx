import { Activity, Shield, Target, Zap } from 'lucide-react';

export function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-wide">COMMAND CENTER</h1>
          <p className="text-sm text-cyber-muted mt-1">Phase 1: Foundations | Day 12/196</p>
        </div>
        <div className="bg-cyber-card px-4 py-2 rounded-lg border border-cyber-border text-sm">
          Status: <span className="text-cyber-neon font-medium ml-2">ONLINE</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Completion', value: '6%', icon: Target, color: 'text-cyber-neon' },
          { label: 'Current Streak', value: '12 Days', icon: Zap, color: 'text-cyber-accent' },
          { label: 'Tasks Today', value: '4/5', icon: Activity, color: 'text-blue-400' },
          { label: 'Labs Pwned', value: '2', icon: Shield, color: 'text-red-400' },
        ].map((stat, i) => {
          const Icon = stat.icon;
          return (
            <div key={i} className="glass-panel p-5 rounded-xl relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 transform translate-x-2 -translate-y-2 group-hover:scale-110 transition-transform">
                <Icon className={`w-16 h-16 ${stat.color}`} />
              </div>
              <p className="text-sm font-medium text-cyber-muted">{stat.label}</p>
              <p className="text-3xl font-bold text-white mt-2">{stat.value}</p>
            </div>
          );
        })}
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 glass-panel rounded-xl p-6 h-96 flex items-center justify-center">
          <p className="text-cyber-muted">Activity Chart Placeholder</p>
        </div>
        <div className="glass-panel rounded-xl p-6 h-96">
          <h2 className="text-lg font-bold text-white mb-4">Today's Objectives</h2>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-start p-3 bg-cyber-darker rounded-lg border border-cyber-border">
                <div className="w-5 h-5 rounded border border-cyber-muted flex-shrink-0 mt-0.5"></div>
                <p className="ml-3 text-sm text-gray-300">Complete networking module {i}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
