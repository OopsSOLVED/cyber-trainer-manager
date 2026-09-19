import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import type { Task, Subtask, TaskStatus } from '../types/task';
import { Shield, ListTodo, Plus, CheckCircle2, Circle, Clock, PlayCircle } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [dayToGenerate, setDayToGenerate] = useState(1);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setIsLoading(true);
    try {
      const res = await api.get('/api/v1/tasks/today');
      setTasks(res.data);
      setError(null);
    } catch (err: any) {
      setError('Failed to fetch tasks.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const generateTasks = async () => {
    setIsGenerating(true);
    try {
      await api.post('/api/v1/tasks/generate', { day_number: dayToGenerate });
      await fetchTasks();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate tasks.');
    } finally {
      setIsGenerating(false);
    }
  };

  const updateSubtaskStatus = async (taskId: number, subtask: Subtask) => {
    // Determine next status (simple toggle for now: todo -> completed -> todo)
    const newStatus: TaskStatus = subtask.status === 'completed' ? 'todo' : 'completed';
    
    // Optimistic UI update
    setTasks(current => 
      current.map(t => {
        if (t.id === taskId) {
          return {
            ...t,
            subtasks: t.subtasks.map(st => st.id === subtask.id ? { ...st, status: newStatus } : st)
          };
        }
        return t;
      })
    );

    try {
      await api.patch(`/api/v1/tasks/subtasks/${subtask.id}`, { status: newStatus });
    } catch (e) {
      // Revert on failure
      console.error('Failed to update subtask', e);
      fetchTasks();
    }
  };

  const updateTaskStatus = async (task: Task, newStatus: TaskStatus) => {
    setTasks(current => current.map(t => t.id === task.id ? { ...t, status: newStatus } : t));
    try {
      await api.patch(`/api/v1/tasks/${task.id}`, { status: newStatus });
    } catch (e) {
      console.error('Failed to update task', e);
      fetchTasks();
    }
  };

  const getStatusIcon = (status: TaskStatus) => {
    switch (status) {
      case 'completed': return <CheckCircle2 className="w-5 h-5 text-cyber-neon" />;
      case 'in_progress': return <PlayCircle className="w-5 h-5 text-cyber-accent animate-pulse" />;
      default: return <Circle className="w-5 h-5 text-cyber-muted" />;
    }
  };

  return (
    <div className="max-w-4xl mx-auto pb-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8">
        <div className="flex items-center mb-4 md:mb-0">
          <ListTodo className="w-8 h-8 text-cyber-neon mr-3" />
          <div>
            <h1 className="text-2xl font-bold text-white tracking-widest uppercase">Daily Objectives</h1>
            <p className="text-cyber-muted text-sm mt-1">Execute your training protocol</p>
          </div>
        </div>

        <div className="flex items-center glass-panel px-4 py-2 rounded-lg">
          <label className="text-sm text-gray-300 mr-3">Day:</label>
          <input 
            type="number" 
            min="1" 
            max="365" 
            value={dayToGenerate}
            onChange={(e) => setDayToGenerate(parseInt(e.target.value) || 1)}
            className="w-16 bg-cyber-dark border border-cyber-border rounded px-2 py-1 text-white text-sm focus:outline-none focus:border-cyber-neon"
          />
          <button 
            onClick={generateTasks}
            disabled={isGenerating}
            className="ml-4 bg-cyber-neon/10 hover:bg-cyber-neon/20 text-cyber-neon border border-cyber-neon/50 px-3 py-1.5 rounded-md text-sm font-medium flex items-center transition-colors disabled:opacity-50"
          >
            {isGenerating ? 'GENERATING...' : <><Plus className="w-4 h-4 mr-1"/> GENERATE TASKS</>}
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-6 bg-red-500/10 border border-red-500/50 p-4 rounded-lg text-red-200 text-sm">
          {error}
        </div>
      )}

      {isLoading ? (
        <div className="flex justify-center p-12">
          <p className="text-cyber-neon animate-pulse font-mono">LOADING OBJECTIVES...</p>
        </div>
      ) : tasks.length === 0 ? (
        <div className="glass-panel p-12 text-center rounded-xl border-dashed">
          <Shield className="w-16 h-16 text-cyber-muted mx-auto mb-4 opacity-50" />
          <h3 className="text-lg font-bold text-gray-300">No Objectives Found</h3>
          <p className="text-sm text-cyber-muted mt-2 max-w-sm mx-auto">
            You don't have any tasks assigned for today. Select a day from your curriculum and generate your daily tasks.
          </p>
        </div>
      ) : (
        <div className="space-y-6">
          {tasks.map(task => {
            const isCompleted = task.status === 'completed';
            
            return (
              <div key={task.id} className={twMerge(
                clsx(
                  "glass-panel rounded-xl overflow-hidden border transition-all duration-300",
                  isCompleted ? "border-cyber-neon/30 opacity-75" : "border-cyber-border"
                )
              )}>
                <div className="p-5 border-b border-cyber-border/50 bg-cyber-darker/50 flex flex-col md:flex-row md:items-center justify-between">
                  <div className="flex items-start md:items-center">
                    <button 
                      onClick={() => updateTaskStatus(task, isCompleted ? 'todo' : 'completed')}
                      className="mt-1 md:mt-0 mr-4 flex-shrink-0"
                    >
                      {getStatusIcon(task.status)}
                    </button>
                    <div>
                      <h2 className={twMerge(
                        clsx(
                          "text-lg font-bold transition-all",
                          isCompleted ? "text-cyber-muted line-through" : "text-white"
                        )
                      )}>
                        {task.topic.name}
                      </h2>
                      <div className="flex items-center space-x-4 mt-1 text-xs text-cyber-muted">
                        <span className="uppercase tracking-wider text-blue-400">Day {task.topic.day_number}</span>
                        <span className="flex items-center"><Clock className="w-3 h-3 mr-1"/> {task.estimated_hours}h estimated</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 md:mt-0 ml-9 md:ml-0 flex space-x-2">
                    {['todo', 'in_progress', 'completed'].map(status => (
                      <button
                        key={status}
                        onClick={() => updateTaskStatus(task, status as TaskStatus)}
                        className={twMerge(
                          clsx(
                            "px-2 py-1 text-xs rounded border transition-colors capitalize",
                            task.status === status 
                              ? (status === 'completed' ? 'bg-cyber-neon/20 text-cyber-neon border-cyber-neon' : 
                                 status === 'in_progress' ? 'bg-cyber-accent/20 text-cyber-accent border-cyber-accent' :
                                 'bg-gray-700 text-white border-gray-500')
                              : "border-transparent text-cyber-muted hover:bg-cyber-card"
                          )
                        )}
                      >
                        {status.replace('_', ' ')}
                      </button>
                    ))}
                  </div>
                </div>

                {task.subtasks.length > 0 && (
                  <div className="p-5 bg-cyber-dark/30 space-y-3">
                    {task.subtasks.map(subtask => {
                      const stCompleted = subtask.status === 'completed';
                      return (
                        <div key={subtask.id} className="flex items-start group">
                          <button 
                            onClick={() => updateSubtaskStatus(task.id, subtask)}
                            className="mt-0.5 mr-3 flex-shrink-0 text-cyber-muted hover:text-cyber-neon transition-colors"
                          >
                            {stCompleted ? <CheckCircle2 className="w-4 h-4 text-cyber-neon" /> : <Circle className="w-4 h-4" />}
                          </button>
                          <p className={twMerge(
                            clsx(
                              "text-sm transition-all duration-200",
                              stCompleted ? "text-cyber-muted line-through" : "text-gray-300 group-hover:text-white"
                            )
                          )}>
                            {subtask.learning_objective.description}
                          </p>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
