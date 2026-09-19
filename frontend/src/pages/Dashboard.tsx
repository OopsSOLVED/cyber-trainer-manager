import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/useAuthStore';
import { api } from '../lib/api';
import type { CurriculumStats } from '../types/curriculum';
import type { Task } from '../types/task';
import { 
  Terminal, Shield, Target, Clock, Activity, 
  BookOpen, Layers, CheckCircle2, ListTodo, AlertTriangle
} from 'lucide-react';
import { Link } from 'react-router-dom';

export function Dashboard() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<CurriculumStats | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, tasksRes] = await Promise.all([
          api.get('/api/v1/curriculum/stats'),
          api.get('/api/v1/tasks/today')
        ]);
        setStats(statsRes.data);
        setTasks(tasksRes.data);
      } catch (err) {
        console.error('Failed to fetch dashboard data', err);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, []);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'MORNING BRIEFING';
    if (hour < 18) return 'AFTERNOON STATUS';
    return 'NIGHT OPERATIONS';
  };

  const tasksCompleted = tasks.filter(t => t.status === 'completed').length;
  const tasksTotal = tasks.length;
  const progressPercentage = tasksTotal === 0 ? 0 : Math.round((tasksCompleted / tasksTotal) * 100);

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-12">
      {/* Header Section */}
      <div className="glass-panel p-8 rounded-xl border border-cyber-border relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
          <Shield className="w-48 h-48 text-cyber-neon" />
        </div>
        
        <div className="relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-cyber-dark/50 border border-cyber-border rounded-full text-xs text-cyber-muted font-mono mb-4 tracking-wider uppercase">
            <Terminal className="w-3 h-3 text-cyber-neon" />
            <span>SYSTEM_READY :: {getGreeting()}</span>
          </div>
          
          <h1 className="text-3xl font-bold text-white mb-2">
            Welcome back, <span className="text-cyber-neon">{user?.display_name}</span>.
          </h1>
          <p className="text-gray-400 max-w-2xl">
            Your CyberTrainer instance is online. Review your curriculum progress and execute today's assigned objectives to advance your skill layer.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Today's Mission Status */}
        <div className="md:col-span-2 glass-panel p-6 rounded-xl border border-cyber-border">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white flex items-center">
              <Target className="w-5 h-5 mr-2 text-cyber-accent" />
              TODAY'S MISSION
            </h2>
            <Link to="/tasks" className="text-sm text-cyber-neon hover:underline flex items-center">
              View All <CheckCircle2 className="w-4 h-4 ml-1" />
            </Link>
          </div>

          {isLoading ? (
            <div className="h-40 flex items-center justify-center">
              <Activity className="w-8 h-8 text-cyber-muted animate-spin" />
            </div>
          ) : tasksTotal === 0 ? (
            <div className="h-40 flex flex-col items-center justify-center text-center border border-dashed border-cyber-border rounded-lg bg-cyber-dark/30">
              <AlertTriangle className="w-8 h-8 text-yellow-500 mb-2 opacity-70" />
              <p className="text-gray-300 font-medium">No objectives scheduled</p>
              <p className="text-sm text-cyber-muted mt-1">Generate today's tasks from the Curriculum.</p>
              <Link to="/tasks" className="mt-3 px-4 py-2 bg-cyber-accent/10 border border-cyber-accent/50 text-cyber-accent rounded hover:bg-cyber-accent/20 transition-colors text-sm">
                Generate Tasks
              </Link>
            </div>
          ) : (
            <div>
              <div className="mb-4">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-300">Daily Progress</span>
                  <span className="text-cyber-neon font-mono">{progressPercentage}%</span>
                </div>
                <div className="w-full bg-cyber-darker rounded-full h-2.5 border border-cyber-border overflow-hidden">
                  <div 
                    className="bg-cyber-neon h-2.5 rounded-full transition-all duration-1000 ease-out shadow-[0_0_10px_#00ff9d]" 
                    style={{ width: `${progressPercentage}%` }}
                  ></div>
                </div>
              </div>

              <div className="space-y-3 mt-6">
                {tasks.slice(0, 3).map(task => (
                  <div key={task.id} className="flex items-center justify-between p-3 bg-cyber-darker/50 border border-cyber-border/50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      {task.status === 'completed' ? (
                        <CheckCircle2 className="w-5 h-5 text-cyber-neon" />
                      ) : (
                        <ListTodo className="w-5 h-5 text-cyber-muted" />
                      )}
                      <span className={task.status === 'completed' ? 'text-cyber-muted line-through' : 'text-gray-200'}>
                        {task.topic.name}
                      </span>
                    </div>
                    <span className="text-xs text-cyber-muted font-mono">{task.estimated_hours}h</span>
                  </div>
                ))}
                {tasksTotal > 3 && (
                  <p className="text-center text-xs text-cyber-muted pt-2 border-t border-cyber-border/50 mt-4">
                    + {tasksTotal - 3} more tasks
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Curriculum Stats */}
        <div className="glass-panel p-6 rounded-xl border border-cyber-border">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white flex items-center">
              <BookOpen className="w-5 h-5 mr-2 text-blue-400" />
              CURRICULUM
            </h2>
          </div>

          {isLoading || !stats ? (
            <div className="h-40 flex items-center justify-center">
              <Activity className="w-8 h-8 text-cyber-muted animate-spin" />
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-cyber-darker/80 border border-cyber-border rounded-lg text-center">
                <div className="text-2xl font-bold text-white mb-1 font-mono">{stats.total_phases}</div>
                <div className="text-xs text-cyber-muted uppercase tracking-wider">Phases</div>
              </div>
              <div className="p-4 bg-cyber-darker/80 border border-cyber-border rounded-lg text-center">
                <div className="text-2xl font-bold text-white mb-1 font-mono">{stats.total_skill_layers}</div>
                <div className="text-xs text-cyber-muted uppercase tracking-wider">Skill Layers</div>
              </div>
              <div className="p-4 bg-cyber-darker/80 border border-cyber-border rounded-lg text-center">
                <div className="text-2xl font-bold text-white mb-1 font-mono">{stats.total_domains}</div>
                <div className="text-xs text-cyber-muted uppercase tracking-wider">Domains</div>
              </div>
              <div className="p-4 bg-cyber-darker/80 border border-cyber-border rounded-lg text-center">
                <div className="text-2xl font-bold text-white mb-1 font-mono">{stats.total_topics}</div>
                <div className="text-xs text-cyber-muted uppercase tracking-wider">Topics</div>
              </div>
              <div className="col-span-2 p-4 bg-cyber-neon/5 border border-cyber-neon/30 rounded-lg flex items-center justify-between">
                <div className="flex items-center">
                  <Clock className="w-5 h-5 text-cyber-neon mr-3" />
                  <div>
                    <div className="text-sm text-gray-300 font-medium">Total Duration</div>
                    <div className="text-xs text-cyber-muted">Estimated roadmap length</div>
                  </div>
                </div>
                <div className="text-xl font-bold text-cyber-neon font-mono">{stats.total_days} Days</div>
              </div>
            </div>
          )}
          
          <div className="mt-6 text-center">
             <Link to="/curriculum" className="text-sm text-gray-400 hover:text-white transition-colors flex items-center justify-center">
              <Layers className="w-4 h-4 mr-1" /> View Full Hierarchy
            </Link>
          </div>
        </div>

      </div>
    </div>
  );
}
