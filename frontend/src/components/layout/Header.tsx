import { Bell, Search, Menu } from 'lucide-react';

export function Header() {
  return (
    <header className="h-16 bg-cyber-darker/80 backdrop-blur-md border-b border-cyber-border flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center">
        <button className="md:hidden text-cyber-muted hover:text-white mr-4">
          <Menu className="w-6 h-6" />
        </button>
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-cyber-muted" />
          <input 
            type="text" 
            placeholder="Search commands, topics..." 
            className="pl-10 pr-4 py-2 bg-cyber-card border border-cyber-border rounded-md text-sm text-gray-200 focus:outline-none focus:border-cyber-neon focus:ring-1 focus:ring-cyber-neon/50 w-64 transition-all"
          />
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        <button className="relative p-2 text-cyber-muted hover:text-white transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-cyber-neon rounded-full shadow-[0_0_5px_#00ff9d]"></span>
        </button>
      </div>
    </header>
  );
}
