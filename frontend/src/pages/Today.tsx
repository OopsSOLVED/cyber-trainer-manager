import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import type { Task, Subtask, TaskStatus, TodaySummary } from '../types/task';
import { 
  CheckCircle2, 
  Circle, 
  PlayCircle, 
  AlertTriangle, 
  Clock, 
  Flame, 
  CheckSquare, 
  Sparkles, 
  ChevronRight, 
  X, 
  BookOpen, 
  ShieldAlert, 
  Award,
  Layers
} from 'lucide-react';
import { clsx } from 'clsx';

export function Today() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [overdueTasks, setOverdueTasks] = useState<Task[]>([]);
  const [summary, setSummary] = useState<TodaySummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [dayToGenerate, setDayToGenerate] = useState(1);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Selected Task for Detail Modal
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [editNotes, setEditNotes] = useState('');
  const [editConfidence, setEditConfidence] = useState<number>(75);
  const [editActualHours, setEditActualHours] = useState<number>(1.0);
  const [isSavingDetail, setIsSavingDetail] = useState(false);

  const fetchTodayData = async () => {
    setIsLoading(true);
    try {
      const [tasksRes, overdueRes, summaryRes] = await Promise.all([
        api.get('/api/v1/tasks/today'),
        api.get('/api/v1/tasks/overdue'),
        api.get('/api/v1/tasks/summary/today'),
      ]);
      setTasks(tasksRes.data);
      setOverdueTasks(overdueRes.data);
      setSummary(summaryRes.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load today data.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTodayData();
  }, []);

  const generateTasks = async () => {
    setIsGenerating(true);
    try {
      await api.post('/api/v1/tasks/generate', { day_number: dayToGenerate });
      await fetchTodayData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate tasks for selected day.');
    } finally {
      setIsGenerating(false);
    }
  };

  const updateTaskStatus = async (taskId: number, newStatus: TaskStatus) => {
    // Optimistic UI update
    setTasks(prev => prev.map(t => t.id === taskId ? { ...t, status: newStatus } : t));
    setOverdueTasks(prev => prev.map(t => t.id === taskId ? { ...t, status: newStatus } : t));

    try {
      await api.patch(`/api/v1/tasks/${taskId}`, { status: newStatus });
      // Refresh summary metrics
      const summaryRes = await api.get('/api/v1/tasks/summary/today');
      setSummary(summaryRes.data);
    } catch (err: any) {
      console.error('Failed to update task status:', err);
      setError(err.response?.data?.detail || 'Failed to update task status.');
      fetchTodayData();
    }
  };

  const toggleSubtaskStatus = async (taskId: number, subtask: Subtask) => {
    const nextStatus: TaskStatus = subtask.status === 'completed' ? 'todo' : 'completed';

    setTasks(prev =>
      prev.map(t => {
        if (t.id === taskId) {
          return {
            ...t,
            subtasks: t.subtasks.map(st => st.id === subtask.id ? { ...st, status: nextStatus } : st)
          };
        }
        return t;
      })
    );

    try {
      await api.patch(`/api/v1/tasks/subtasks/${subtask.id}`, { status: nextStatus });
    } catch (err) {
      console.error('Failed to update subtask:', err);
      fetchTodayData();
    }
  };

  const openDetailModal = (task: Task) => {
    setSelectedTask(task);
    setEditNotes(task.notes || '');
    setEditConfidence(task.confidence_score ?? 75);
    setEditActualHours(task.actual_hours || task.estimated_hours);
  };

  const closeDetailModal = () => {
    setSelectedTask(null);
  };

  const saveTaskDetails = async () => {
    if (!selectedTask) return;
    setIsSavingDetail(true);
    try {
      const res = await api.patch(`/api/v1/tasks/${selectedTask.id}`, {
        notes: editNotes,
        confidence_score: editConfidence,
        actual_hours: editActualHours,
      });

      // Update local state
      setTasks(prev => prev.map(t => t.id === selectedTask.id ? res.data : t));
      setOverdueTasks(prev => prev.map(t => t.id === selectedTask.id ? res.data : t));
      setSelectedTask(res.data);
      closeDetailModal();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save task reflections.');
    } finally {
      setIsSavingDetail(false);
    }
  };

  const getStatusIcon = (status: TaskStatus) => {
    switch (status) {
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-cyber-neon" />;
      case 'in_progress':
        return <PlayCircle className="w-5 h-5 text-cyber-accent animate-pulse" />;
      default:
        return <Circle className="w-5 h-5 text-gray-500 hover:text-gray-300" />;
    }
  };

  return (
    <div className="max-w-5xl mx-auto pb-16 space-y-8">
      {/* ── Daily Objective Banner ────────────────────────────────── */}
      <div className="relative overflow-hidden rounded-2xl border border-cyber-border bg-gradient-to-r from-cyber-card via-cyber-darker to-cyber-card p-6 md:p-8 shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-cyber-neon text-xs font-mono uppercase tracking-widest mb-1">
              <Sparkles className="w-4 h-4" />
              <span>Execution Protocol — Today's Mission</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold text-white tracking-wide">
              {summary?.daily_objective ? summary.daily_objective.split(':')[0] : "Today's Learning Focus"}
            </h1>
            <p className="text-cyber-muted text-sm md:text-base mt-2 max-w-2xl">
              {summary?.daily_objective 
                ? summary.daily_objective.split(':').slice(1).join(':').trim()
                : "Select or generate tasks for today's curriculum milestone to start your daily mission."}
            </p>
          </div>

          <div className="flex items-center gap-3 bg-cyber-darker/80 border border-cyber-border/80 px-4 py-3 rounded-xl backdrop-blur-md self-start md:self-auto">
            <span className="text-xs text-gray-400 font-mono">DAY:</span>
            <input
              type="number"
              min={1}
              max={196}
              value={dayToGenerate}
              onChange={(e) => setDayToGenerate(Number(e.target.value))}
              className="w-16 bg-cyber-card text-white text-center font-bold px-2 py-1 rounded border border-cyber-border text-sm focus:outline-none focus:border-cyber-neon"
            />
            <button
              onClick={generateTasks}
              disabled={isGenerating}
              className="bg-cyber-neon/10 hover:bg-cyber-neon/20 text-cyber-neon border border-cyber-neon/40 px-3 py-1 rounded text-xs font-semibold uppercase tracking-wider transition-all disabled:opacity-50"
            >
              {isGenerating ? 'Loading...' : 'Load'}
            </button>
          </div>
        </div>

        {/* ── Daily Metrics Bar ───────────────────────────────────── */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6 pt-6 border-t border-cyber-border/60">
          <div className="bg-cyber-card/60 p-3 rounded-xl border border-cyber-border/40">
            <div className="text-xs text-cyber-muted flex items-center gap-1 font-mono">
              <CheckSquare className="w-3.5 h-3.5 text-cyber-neon" />
              COMPLETION
            </div>
            <div className="text-xl font-bold text-white mt-1">
              {summary?.completion_percentage ?? 0}%
            </div>
            <div className="w-full bg-cyber-darker h-1.5 rounded-full mt-2 overflow-hidden">
              <div 
                className="bg-cyber-neon h-full transition-all duration-500" 
                style={{ width: `${summary?.completion_percentage ?? 0}%` }}
              />
            </div>
          </div>

          <div className="bg-cyber-card/60 p-3 rounded-xl border border-cyber-border/40">
            <div className="text-xs text-cyber-muted flex items-center gap-1 font-mono">
              <Layers className="w-3.5 h-3.5 text-cyber-accent" />
              ACTIVE TASKS
            </div>
            <div className="text-xl font-bold text-white mt-1">
              {summary?.completed_tasks ?? 0} / {summary?.total_tasks ?? 0}
            </div>
            <div className="text-xs text-cyber-muted mt-1">
              {summary?.in_progress_tasks ?? 0} in progress
            </div>
          </div>

          <div className="bg-cyber-card/60 p-3 rounded-xl border border-cyber-border/40">
            <div className="text-xs text-cyber-muted flex items-center gap-1 font-mono">
              <Clock className="w-3.5 h-3.5 text-amber-400" />
              HOURS LOGGED
            </div>
            <div className="text-xl font-bold text-white mt-1">
              {summary?.actual_hours ?? 0}h <span className="text-xs text-gray-500 font-normal">/ {summary?.estimated_hours ?? 0}h</span>
            </div>
            <div className="text-xs text-cyber-muted mt-1">Estimated duration</div>
          </div>

          <div className="bg-cyber-card/60 p-3 rounded-xl border border-cyber-border/40">
            <div className="text-xs text-cyber-muted flex items-center gap-1 font-mono">
              <AlertTriangle className={clsx("w-3.5 h-3.5", (summary?.overdue_tasks ?? 0) > 0 ? "text-red-400" : "text-gray-500")} />
              OVERDUE
            </div>
            <div className={clsx("text-xl font-bold mt-1", (summary?.overdue_tasks ?? 0) > 0 ? "text-red-400" : "text-gray-300")}>
              {summary?.overdue_tasks ?? 0}
            </div>
            <div className="text-xs text-cyber-muted mt-1">Prior missed tasks</div>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-950/40 border border-red-800 text-red-300 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-red-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)} className="text-red-400 hover:text-white text-xs font-mono">DISMISS</button>
        </div>
      )}

      {/* ── Overdue Tasks Section (If any) ─────────────────────────── */}
      {overdueTasks.length > 0 && (
        <div className="border border-red-900/60 bg-red-950/20 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4 text-red-400 font-mono text-sm tracking-wider uppercase">
            <AlertTriangle className="w-5 h-5" />
            <span>Overdue Revision Queue ({overdueTasks.length})</span>
          </div>
          <div className="space-y-3">
            {overdueTasks.map(task => (
              <div 
                key={task.id}
                className="bg-cyber-card/80 border border-red-900/40 rounded-xl p-4 flex items-center justify-between gap-4"
              >
                <div>
                  <h4 className="text-white font-medium text-sm">{task.topic.name}</h4>
                  <p className="text-cyber-muted text-xs mt-0.5">{task.topic.description}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => updateTaskStatus(task.id, 'completed')}
                    className="bg-cyber-neon/10 hover:bg-cyber-neon/20 text-cyber-neon text-xs border border-cyber-neon/30 px-3 py-1.5 rounded-lg transition-all"
                  >
                    Mark Done
                  </button>
                  <button
                    onClick={() => openDetailModal(task)}
                    className="text-gray-400 hover:text-white text-xs px-2 py-1"
                  >
                    Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ── Today's Tasks List ────────────────────────────────────── */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white tracking-wider flex items-center gap-2">
            <CheckSquare className="w-5 h-5 text-cyber-neon" />
            TODAY'S EXECUTION TASKS
          </h2>
          <span className="text-xs font-mono text-cyber-muted">
            {tasks.filter(t => t.status === 'completed').length} of {tasks.length} Completed
          </span>
        </div>

        {isLoading ? (
          <div className="glass-panel p-12 rounded-2xl text-center">
            <div className="w-8 h-8 border-2 border-cyber-neon border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            <p className="text-cyber-muted text-sm font-mono">Syncing execution protocol...</p>
          </div>
        ) : tasks.length === 0 ? (
          <div className="glass-panel p-12 rounded-2xl text-center border-dashed border-cyber-border">
            <BookOpen className="w-12 h-12 text-cyber-muted mx-auto mb-3 opacity-50" />
            <h3 className="text-lg font-bold text-white">No Tasks Scheduled For Today</h3>
            <p className="text-cyber-muted text-sm mt-1 max-w-md mx-auto">
              Select a day number above and click <strong>Load</strong> to generate actionable tasks for today.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={clsx(
                  "rounded-2xl border transition-all duration-300 p-5 md:p-6 bg-cyber-card/60 backdrop-blur-md",
                  task.status === 'completed' 
                    ? "border-cyber-neon/30 bg-cyber-card/30" 
                    : task.status === 'in_progress'
                      ? "border-cyber-accent/60 shadow-[0_0_15px_rgba(168,85,247,0.1)]"
                      : "border-cyber-border hover:border-gray-600"
                )}
              >
                <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                  {/* Left: Checkbox & Info */}
                  <div className="flex items-start gap-3">
                    <button
                      onClick={() => {
                        const next: TaskStatus = task.status === 'completed' ? 'todo' : 'completed';
                        updateTaskStatus(task.id, next);
                      }}
                      className="mt-1 transition-transform active:scale-90"
                    >
                      {getStatusIcon(task.status)}
                    </button>
                    <div>
                      <div className="flex flex-wrap items-center gap-2 mb-1">
                        <span className="text-xs font-mono font-bold text-cyber-neon bg-cyber-neon/10 px-2 py-0.5 rounded">
                          Day {task.topic.day_number ?? 1}
                        </span>
                        <span className="text-xs font-mono text-purple-400 bg-purple-950/40 border border-purple-800/40 px-2 py-0.5 rounded capitalize">
                          {task.task_type || 'study'}
                        </span>
                        <span className="text-xs font-mono text-gray-400 bg-cyber-darker px-2 py-0.5 rounded capitalize">
                          {task.priority || 'medium'} priority
                        </span>
                        <span className="text-xs font-mono text-gray-500 flex items-center gap-1">
                          <Clock className="w-3 h-3" /> {task.estimated_hours}h
                        </span>
                      </div>
                      <h3 className={clsx(
                        "text-lg font-bold transition-colors",
                        task.status === 'completed' ? "line-through text-gray-500" : "text-white"
                      )}>
                        {task.topic.name}
                      </h3>
                      <p className="text-cyber-muted text-sm mt-1 leading-relaxed">
                        {task.topic.description}
                      </p>
                    </div>
                  </div>

                  {/* Right: Quick actions */}
                  <div className="flex items-center gap-2 self-end md:self-start">
                    <button
                      onClick={() => updateTaskStatus(task.id, task.status === 'in_progress' ? 'todo' : 'in_progress')}
                      className={clsx(
                        "px-3 py-1.5 rounded-lg text-xs font-mono transition-all",
                        task.status === 'in_progress'
                          ? "bg-purple-900/50 text-purple-300 border border-purple-500"
                          : "bg-cyber-darker text-gray-400 hover:text-white border border-cyber-border"
                      )}
                    >
                      {task.status === 'in_progress' ? 'Pause' : 'Start'}
                    </button>
                    <button
                      onClick={() => openDetailModal(task)}
                      className="px-3 py-1.5 bg-cyber-darker hover:bg-cyber-card text-cyber-neon text-xs font-mono border border-cyber-border hover:border-cyber-neon/40 rounded-lg flex items-center gap-1 transition-all"
                    >
                      <span>Reflection & Details</span>
                      <ChevronRight className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                {/* Subtasks (Actionable criteria) */}
                {task.subtasks && task.subtasks.length > 0 && (
                  <div className="mt-5 pt-4 border-t border-cyber-border/40 space-y-2">
                    <div className="text-xs font-mono text-cyber-muted uppercase tracking-wider mb-2">
                      Deliverable & Checkpoints:
                    </div>
                    {task.subtasks.map((st) => (
                      <div
                        key={st.id}
                        onClick={() => toggleSubtaskStatus(task.id, st)}
                        className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-cyber-darker/60 cursor-pointer transition-colors"
                      >
                        <button className="mt-0.5">
                          {st.status === 'completed' ? (
                            <CheckCircle2 className="w-4 h-4 text-cyber-neon" />
                          ) : (
                            <Circle className="w-4 h-4 text-gray-600" />
                          )}
                        </button>
                        <span className={clsx(
                          "text-xs leading-relaxed",
                          st.status === 'completed' ? "line-through text-gray-500" : "text-gray-300"
                        )}>
                          {st.learning_objective.description}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── Task Detail & Reflection Modal (Section 22 UX) ─────────── */}
      {selectedTask && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-cyber-card border border-cyber-border rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl p-6 md:p-8 space-y-6 animate-in fade-in zoom-in-95">
            {/* Modal Header */}
            <div className="flex items-start justify-between">
              <div>
                <span className="text-xs font-mono text-cyber-neon uppercase tracking-wider">
                  Day {selectedTask.topic.day_number ?? 1} Protocol Detail
                </span>
                <h2 className="text-xl font-bold text-white mt-1">{selectedTask.topic.name}</h2>
              </div>
              <button
                onClick={closeDetailModal}
                className="p-1 rounded-lg text-gray-400 hover:text-white hover:bg-cyber-darker"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Objective & Action */}
            <div className="space-y-3 bg-cyber-darker/70 p-4 rounded-xl border border-cyber-border/60">
              <div>
                <span className="text-xs font-mono text-gray-400 uppercase tracking-wider block">Learning Objective</span>
                <p className="text-sm text-gray-200 mt-1">{selectedTask.topic.description}</p>
              </div>
            </div>

            {/* Reflection prompt (Section 22) */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-white flex items-center gap-2">
                <Flame className="w-4 h-4 text-cyber-accent" />
                Learner Reflection
              </label>
              <p className="text-xs text-cyber-muted">
                "What did I understand today that I could not explain yesterday?"
              </p>
              <textarea
                value={editNotes}
                onChange={(e) => setEditNotes(e.target.value)}
                placeholder="Record technical insights, packet flow nuances, or defensive notes..."
                rows={4}
                className="w-full bg-cyber-darker border border-cyber-border rounded-xl p-3 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-cyber-neon transition-colors"
              />
            </div>

            {/* Confidence Slider (Section 22) */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="font-semibold text-white flex items-center gap-2">
                  <Award className="w-4 h-4 text-cyber-neon" />
                  Confidence Score
                </span>
                <span className="font-mono text-cyber-neon font-bold">{editConfidence}%</span>
              </div>
              <input
                type="range"
                min={0}
                max={100}
                value={editConfidence}
                onChange={(e) => setEditConfidence(Number(e.target.value))}
                className="w-full accent-cyber-neon cursor-pointer"
              />
              <div className="flex justify-between text-[10px] font-mono text-gray-500">
                <span>0% Unknown</span>
                <span>50% Practiced</span>
                <span>75% Demonstrated</span>
                <span>100% Teaching Ready</span>
              </div>
            </div>

            {/* Time Tracking */}
            <div className="space-y-2">
              <label className="text-sm font-semibold text-white flex items-center gap-2">
                <Clock className="w-4 h-4 text-amber-400" />
                Actual Hours Spent
              </label>
              <input
                type="number"
                step="0.5"
                min="0"
                max="24"
                value={editActualHours}
                onChange={(e) => setEditActualHours(Number(e.target.value))}
                className="w-32 bg-cyber-darker border border-cyber-border rounded-xl p-2.5 text-sm text-white focus:outline-none focus:border-cyber-neon font-mono"
              />
            </div>

            {/* Modal Actions */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-cyber-border">
              <button
                onClick={closeDetailModal}
                className="px-4 py-2 text-sm text-gray-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={saveTaskDetails}
                disabled={isSavingDetail}
                className="px-5 py-2 rounded-xl text-sm font-semibold text-black bg-cyber-neon hover:bg-cyber-neon/90 transition-all disabled:opacity-50"
              >
                {isSavingDetail ? 'Saving...' : 'Save & Sync'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
