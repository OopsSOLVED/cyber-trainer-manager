import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  BookOpen, 
  ListTodo, 
  Settings, 
  Terminal,
  ShieldAlert
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Curriculum', path: '/curriculum', icon: BookOpen },
  { name: 'Daily Tasks', path: '/tasks', icon: ListTodo },
  { name: 'Labs', path: '/labs', icon: Terminal },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 h-screen bg-cyber-darker border-r border-cyber-border flex flex-col hidden md:flex">
      <div className="h-16 flex items-center px-6 border-b border-cyber-border">
        <ShieldAlert className="w-6 h-6 text-cyber-neon mr-3" />
        <span className="text-lg font-bold tracking-wider text-white">CYBER<span className="text-cyber-neon">TRAINER</span></span>
      </div>
      
      <nav className="flex-1 py-6 px-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={twMerge(
                clsx(
                  'flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 group',
                  isActive 
                    ? 'bg-cyber-neon/10 text-cyber-neon neon-border' 
                    : 'text-cyber-muted hover:bg-cyber-card hover:text-white'
                )
              )}
            >
              <Icon className={clsx(
                "w-5 h-5 mr-3 transition-colors",
                isActive ? "text-cyber-neon" : "text-cyber-muted group-hover:text-white"
              )} />
              {item.name}
            </Link>
          );
        })}
      </nav>
      
      <div className="p-4 border-t border-cyber-border">
        <div className="flex items-center">
          <div className="w-8 h-8 rounded-full bg-cyber-accent/20 border border-cyber-accent flex items-center justify-center text-cyber-accent font-bold">
            U
          </div>
          <div className="ml-3">
            <p className="text-sm font-medium text-white">Test User</p>
            <p className="text-xs text-cyber-muted">Phase 1: Foundations</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
