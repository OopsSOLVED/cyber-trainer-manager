import { useEffect, useState, useMemo } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../lib/api';
import type { 
  RoadmapResponse, 
  PhaseRoadmapItem, 
  DomainRoadmapItem,
  DomainTopicsResponse,
  TopicRoadmapItem 
} from '../types/curriculum';
import { 
  Map, 
  CheckCircle2, 
  Clock, 
  Target, 
  Search, 
  ChevronRight, 
  ChevronDown, 
  Layers, 
  ArrowRight, 
  BookOpen,
  Sparkles,
  AlertCircle
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Roadmap() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  // Data state
  const [roadmap, setRoadmap] = useState<RoadmapResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Selected state
  const [selectedPhaseId, setSelectedPhaseId] = useState<number>(1);
  const [selectedDomainId, setSelectedDomainId] = useState<number | null>(null);
  const [domainDetails, setDomainDetails] = useState<Record<number, DomainTopicsResponse>>({});
  const [loadingDomainId, setLoadingDomainId] = useState<number | null>(null);

  // Filter state
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [expandedTopicIds, setExpandedTopicIds] = useState<Set<number>>(new Set());

  // Fetch full roadmap data on mount
  useEffect(() => {
    fetchRoadmap();
  }, []);

  const fetchRoadmap = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await api.get<RoadmapResponse>('/api/v1/curriculum/roadmap');
      setRoadmap(res.data);
      if (res.data.phases.length > 0) {
        // Respect query param phase if set
        const phaseParam = searchParams.get('phase');
        const initialPhaseId = phaseParam ? parseInt(phaseParam, 10) : res.data.phases[0].id;
        setSelectedPhaseId(initialPhaseId);

        // Select the first domain in that phase by default
        const initialPhase = res.data.phases.find(p => p.id === initialPhaseId) || res.data.phases[0];
        if (initialPhase?.skill_layers?.[0]?.domains?.[0]) {
          const firstDomain = initialPhase.skill_layers[0].domains[0];
          setSelectedDomainId(firstDomain.id);
          fetchDomainTopics(firstDomain.id);
        }
      }
    } catch (err: any) {
      console.error('Failed to load roadmap:', err);
      setError('Unable to load curriculum roadmap. Please check backend connection.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchDomainTopics = async (domainId: number) => {
    if (domainDetails[domainId]) return;
    setLoadingDomainId(domainId);
    try {
      const res = await api.get<DomainTopicsResponse>(`/api/v1/curriculum/domains/${domainId}/topics-with-status`);
      setDomainDetails(prev => ({ ...prev, [domainId]: res.data }));
    } catch (err) {
      console.error(`Failed to load domain ${domainId} topics:`, err);
    } finally {
      setLoadingDomainId(null);
    }
  };

  const handleSelectPhase = (phaseId: number) => {
    setSelectedPhaseId(phaseId);
    setSearchParams({ phase: phaseId.toString() });

    const phase = roadmap?.phases.find(p => p.id === phaseId);
    if (phase?.skill_layers?.[0]?.domains?.[0]) {
      const firstDomain = phase.skill_layers[0].domains[0];
      setSelectedDomainId(firstDomain.id);
      fetchDomainTopics(firstDomain.id);
    } else {
      setSelectedDomainId(null);
    }
  };

  const handleSelectDomain = (domainId: number) => {
    setSelectedDomainId(domainId);
    fetchDomainTopics(domainId);
  };

  const toggleTopicExpand = (topicId: number) => {
    setExpandedTopicIds(prev => {
      const next = new Set(prev);
      if (next.has(topicId)) {
        next.delete(topicId);
      } else {
        next.add(topicId);
      }
      return next;
    });
  };

  const handleLaunchDay = (dayNumber: number | null) => {
    if (!dayNumber) return;
    navigate(`/today?day=${dayNumber}`);
  };

  // Active Phase
  const currentPhase: PhaseRoadmapItem | undefined = useMemo(() => {
    return roadmap?.phases.find(p => p.id === selectedPhaseId);
  }, [roadmap, selectedPhaseId]);

  // Active Domain
  const currentDomain: DomainRoadmapItem | undefined = useMemo(() => {
    if (!currentPhase || !selectedDomainId) return undefined;
    for (const layer of currentPhase.skill_layers) {
      const d = layer.domains.find(dom => dom.id === selectedDomainId);
      if (d) return d;
    }
    return undefined;
  }, [currentPhase, selectedDomainId]);

  // Current domain topics filtered
  const filteredTopics: TopicRoadmapItem[] = useMemo(() => {
    if (!selectedDomainId || !domainDetails[selectedDomainId]) return [];
    let list = domainDetails[selectedDomainId].topics;

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      list = list.filter(t => 
        t.name.toLowerCase().includes(q) ||
        (t.description && t.description.toLowerCase().includes(q)) ||
        (t.day_number && t.day_number.toString().includes(q))
      );
    }

    if (difficultyFilter !== 'all') {
      list = list.filter(t => t.difficulty.toLowerCase() === difficultyFilter.toLowerCase());
    }

    if (statusFilter !== 'all') {
      if (statusFilter === 'completed') {
        list = list.filter(t => t.status === 'completed');
      } else if (statusFilter === 'in_progress') {
        list = list.filter(t => t.status === 'in_progress');
      } else if (statusFilter === 'unstarted') {
        list = list.filter(t => !t.status || t.status === 'todo');
      }
    }

    return list;
  }, [selectedDomainId, domainDetails, searchQuery, difficultyFilter, statusFilter]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="w-12 h-12 border-4 border-cyber-neon/20 border-t-cyber-neon rounded-full animate-spin mb-4" />
        <p className="text-cyber-neon font-mono tracking-widest text-sm uppercase animate-pulse">
          Initializing 196-Day Curriculum Roadmap Matrix...
        </p>
      </div>
    );
  }

  if (error || !roadmap) {
    return (
      <div className="max-w-xl mx-auto mt-12 p-6 glass-panel border border-red-500/30 rounded-xl text-center">
        <AlertCircle className="w-10 h-10 text-red-400 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-white mb-2">Failed to Load Roadmap</h2>
        <p className="text-cyber-muted text-sm mb-4">{error}</p>
        <button
          onClick={fetchRoadmap}
          className="px-4 py-2 bg-cyber-neon/20 hover:bg-cyber-neon/30 text-cyber-neon border border-cyber-neon/40 rounded-lg text-sm font-medium transition-colors"
        >
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto pb-16 space-y-8">
      {/* ── Top Header & Global Mastery Banner ─────────────────────── */}
      <div className="glass-panel p-6 rounded-2xl border border-cyber-border shadow-2xl relative overflow-hidden">
        <div className="absolute -right-16 -top-16 w-64 h-64 bg-cyber-neon/5 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -left-16 -bottom-16 w-64 h-64 bg-cyber-accent/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2.5 rounded-xl bg-cyber-neon/10 border border-cyber-neon/30 text-cyber-neon">
                <Map className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl font-black text-white uppercase tracking-wider">
                  Cybersecurity Trainer Roadmap
                </h1>
                <p className="text-xs text-cyber-muted font-mono tracking-widest uppercase">
                  Production Master Curriculum • 196 Days • 28 Weeks • 4 Phases
                </p>
              </div>
            </div>
            <p className="text-sm text-gray-400 max-w-2xl mt-2">
              Interactive execution curriculum engineered from computer foundations through enterprise Active Directory, SOC operations, and trainer mastery.
            </p>
          </div>

          {/* Global Progress Metrics Card */}
          <div className="bg-cyber-darker/80 border border-cyber-border/80 rounded-xl p-4 lg:w-96 flex flex-col justify-center">
            <div className="flex items-center justify-between text-xs mb-2">
              <span className="text-gray-300 font-semibold uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-cyber-neon" /> Overall Curriculum Progress
              </span>
              <span className="font-mono text-cyber-neon font-bold text-sm">
                {roadmap.progress_percent.toFixed(1)}%
              </span>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-cyber-card h-2.5 rounded-full overflow-hidden border border-cyber-border/40 p-0.5 mb-3">
              <div 
                className="bg-gradient-to-r from-cyber-neon via-blue-500 to-purple-600 h-full rounded-full transition-all duration-700 ease-out"
                style={{ width: `${Math.min(100, Math.max(2, roadmap.progress_percent))}%` }}
              />
            </div>

            <div className="grid grid-cols-4 gap-2 text-center text-xs">
              <div className="p-1.5 rounded bg-cyber-card/60">
                <p className="text-white font-bold">{roadmap.completed_topics}</p>
                <p className="text-[10px] text-cyber-muted uppercase">Done</p>
              </div>
              <div className="p-1.5 rounded bg-cyber-card/60">
                <p className="text-white font-bold">{roadmap.total_topics}</p>
                <p className="text-[10px] text-cyber-muted uppercase">Topics</p>
              </div>
              <div className="p-1.5 rounded bg-cyber-card/60">
                <p className="text-white font-bold">{roadmap.total_domains}</p>
                <p className="text-[10px] text-cyber-muted uppercase">Domains</p>
              </div>
              <div className="p-1.5 rounded bg-cyber-card/60">
                <p className="text-cyber-neon font-bold">{roadmap.total_days}d</p>
                <p className="text-[10px] text-cyber-muted uppercase">Total</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── Phase Navigation Tabs ────────────────────────────────── */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {roadmap.phases.map((phase) => {
          const isSelected = phase.id === selectedPhaseId;
          return (
            <button
              key={phase.id}
              onClick={() => handleSelectPhase(phase.id)}
              className={twMerge(
                clsx(
                  "p-5 rounded-xl text-left transition-all duration-300 relative border flex flex-col justify-between group",
                  isSelected
                    ? "bg-cyber-darker border-cyber-neon shadow-[0_0_20px_rgba(0,255,204,0.15)] ring-1 ring-cyber-neon/50"
                    : "glass-panel border-cyber-border hover:border-cyber-border/90 hover:bg-cyber-darker/60"
                )
              )}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className={clsx(
                    "text-[11px] font-mono uppercase tracking-widest font-bold px-2 py-0.5 rounded",
                    isSelected 
                      ? "bg-cyber-neon/20 text-cyber-neon border border-cyber-neon/30" 
                      : "bg-cyber-card text-cyber-muted"
                  )}>
                    Phase {phase.order} • {phase.estimated_weeks || 7} Wks
                  </span>
                  <span className="text-xs font-mono font-bold text-gray-300">
                    {phase.progress_percent.toFixed(0)}%
                  </span>
                </div>
                <h3 className={clsx(
                  "font-bold text-base transition-colors line-clamp-1",
                  isSelected ? "text-white" : "text-gray-300 group-hover:text-white"
                )}>
                  {phase.name}
                </h3>
                <p className="text-xs text-cyber-muted mt-1 line-clamp-2 leading-relaxed">
                  {phase.description}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-cyber-border/40">
                <div className="w-full bg-cyber-card h-1.5 rounded-full overflow-hidden">
                  <div 
                    className={clsx(
                      "h-full rounded-full transition-all duration-500",
                      isSelected ? "bg-cyber-neon" : "bg-cyber-muted/60"
                    )}
                    style={{ width: `${Math.min(100, Math.max(0, phase.progress_percent))}%` }}
                  />
                </div>
                <div className="flex items-center justify-between mt-2 text-[10px] text-cyber-muted">
                  <span>{phase.skill_layers.length} Skill Layers</span>
                  <span>{phase.completed_topics} / {phase.total_topics} Topics</span>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {/* ── Main Roadmap Content Grid ────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Column: Skill Layers & Domains Hierarchy (5 Columns) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-cyber-neon" />
              Domains & Skill Layers
            </h2>
            <span className="text-xs text-cyber-muted font-mono">
              Phase {currentPhase?.order} of {roadmap.total_phases}
            </span>
          </div>

          <div className="space-y-6">
            {currentPhase?.skill_layers.map((layer) => (
              <div key={layer.id} className="space-y-3">
                {/* Skill Layer Header */}
                <div className="flex items-center justify-between px-2">
                  <span className="text-xs font-mono font-bold tracking-wider text-cyber-accent uppercase">
                    Layer {layer.order}: {layer.name}
                  </span>
                  <span className="text-[11px] font-mono text-cyber-muted">
                    {layer.completed_topics}/{layer.total_topics} Done ({layer.progress_percent.toFixed(0)}%)
                  </span>
                </div>

                {/* Domain Cards */}
                <div className="space-y-2">
                  {layer.domains.map((dom) => {
                    const isDomainSelected = dom.id === selectedDomainId;
                    return (
                      <div
                        key={dom.id}
                        onClick={() => handleSelectDomain(dom.id)}
                        className={twMerge(
                          clsx(
                            "p-4 rounded-xl cursor-pointer transition-all duration-200 border",
                            isDomainSelected
                              ? "bg-cyber-darker border-cyber-accent/80 shadow-[0_0_15px_rgba(138,43,226,0.15)] ring-1 ring-cyber-accent/40"
                              : "glass-panel border-cyber-border hover:border-cyber-border/80 hover:bg-cyber-card/40"
                          )
                        )}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-darker text-cyber-neon border border-cyber-neon/30">
                                Days {dom.day_start || '?'}-{dom.day_end || '?'}
                              </span>
                              <span className="text-[10px] font-mono text-cyber-muted">
                                {dom.total_hours} hrs
                              </span>
                            </div>
                            <h4 className={clsx(
                              "font-semibold text-sm transition-colors truncate",
                              isDomainSelected ? "text-white" : "text-gray-300"
                            )}>
                              {dom.name}
                            </h4>
                            {dom.description && (
                              <p className="text-xs text-cyber-muted line-clamp-1 mt-0.5">
                                {dom.description}
                              </p>
                            )}
                          </div>

                          <div className="text-right flex-shrink-0">
                            <span className={clsx(
                              "text-xs font-mono font-bold",
                              dom.progress_percent === 100 ? "text-green-400" : "text-gray-400"
                            )}>
                              {dom.progress_percent.toFixed(0)}%
                            </span>
                            <ChevronRight className={clsx(
                              "w-4 h-4 ml-auto mt-1 transition-transform",
                              isDomainSelected ? "text-cyber-accent translate-x-1" : "text-cyber-muted"
                            )} />
                          </div>
                        </div>

                        {/* Domain Mini Progress */}
                        <div className="w-full bg-cyber-darker h-1.5 rounded-full overflow-hidden mt-3 border border-cyber-border/30">
                          <div
                            className={clsx(
                              "h-full rounded-full transition-all duration-500",
                              dom.progress_percent === 100 
                                ? "bg-green-400 shadow-[0_0_8px_rgba(74,222,128,0.5)]" 
                                : isDomainSelected ? "bg-cyber-accent" : "bg-cyber-muted/60"
                            )}
                            style={{ width: `${Math.min(100, Math.max(0, dom.progress_percent))}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Topics Explorer & Mission Launcher (7 Columns) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Domain Detail Header */}
          <div className="glass-panel p-6 rounded-2xl border border-cyber-border space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-cyber-neon font-bold">
                  Domain Inspector
                </span>
                <h3 className="text-xl font-bold text-white mt-0.5">
                  {currentDomain ? currentDomain.name : 'Select a Domain'}
                </h3>
                {currentDomain?.description && (
                  <p className="text-xs text-gray-400 mt-1 max-w-xl">
                    {currentDomain.description}
                  </p>
                )}
              </div>

              {currentDomain && (
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-xs font-mono text-cyber-muted">Completion</span>
                    <p className="text-base font-mono font-bold text-cyber-neon">
                      {currentDomain.completed_topics} / {currentDomain.topic_count} Topics
                    </p>
                  </div>
                  <div className="w-12 h-12 rounded-xl bg-cyber-darker border border-cyber-border flex items-center justify-center font-mono font-bold text-cyber-neon">
                    {currentDomain.progress_percent.toFixed(0)}%
                  </div>
                </div>
              )}
            </div>

            {/* Filter & Search Bar */}
            <div className="pt-3 border-t border-cyber-border/40 grid grid-cols-1 sm:grid-cols-12 gap-3">
              {/* Keyword Search */}
              <div className="sm:col-span-5 relative">
                <Search className="w-4 h-4 text-cyber-muted absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search topics or day #..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-1.5 bg-cyber-darker border border-cyber-border rounded-lg text-xs text-white placeholder-cyber-muted focus:outline-none focus:border-cyber-neon"
                />
              </div>

              {/* Difficulty Dropdown */}
              <div className="sm:col-span-4">
                <select
                  value={difficultyFilter}
                  onChange={(e) => setDifficultyFilter(e.target.value)}
                  className="w-full px-3 py-1.5 bg-cyber-darker border border-cyber-border rounded-lg text-xs text-gray-300 focus:outline-none focus:border-cyber-neon"
                >
                  <option value="all">All Difficulties</option>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                  <option value="expert">Expert</option>
                </select>
              </div>

              {/* Status Dropdown */}
              <div className="sm:col-span-3">
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="w-full px-3 py-1.5 bg-cyber-darker border border-cyber-border rounded-lg text-xs text-gray-300 focus:outline-none focus:border-cyber-neon"
                >
                  <option value="all">All Statuses</option>
                  <option value="completed">Completed</option>
                  <option value="in_progress">In Progress</option>
                  <option value="unstarted">Not Started</option>
                </select>
              </div>
            </div>
          </div>

          {/* Topics List */}
          {loadingDomainId === selectedDomainId ? (
            <div className="p-12 text-center glass-panel rounded-2xl border border-cyber-border">
              <div className="w-8 h-8 border-2 border-cyber-neon/20 border-t-cyber-neon rounded-full animate-spin mx-auto mb-3" />
              <p className="text-xs font-mono text-cyber-muted uppercase tracking-wider animate-pulse">
                Fetching domain objectives and learning modules...
              </p>
            </div>
          ) : filteredTopics.length === 0 ? (
            <div className="p-12 text-center glass-panel rounded-2xl border border-cyber-border">
              <BookOpen className="w-10 h-10 text-cyber-muted mx-auto mb-2 opacity-50" />
              <p className="text-gray-300 font-medium text-sm">No topics match your filter</p>
              <p className="text-xs text-cyber-muted mt-1">Try resetting the search query or difficulty filters.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {filteredTopics.map((topic) => {
                const isExpanded = expandedTopicIds.has(topic.id);
                const isCompleted = topic.status === 'completed';
                const isInProgress = topic.status === 'in_progress';

                return (
                  <div
                    key={topic.id}
                    className={twMerge(
                      clsx(
                        "rounded-xl border transition-all duration-200 overflow-hidden",
                        isCompleted 
                          ? "bg-green-950/10 border-green-500/30" 
                          : isInProgress
                          ? "bg-blue-950/10 border-blue-500/40 shadow-[0_0_15px_rgba(59,130,246,0.1)]"
                          : "glass-panel border-cyber-border hover:border-cyber-border/80"
                      )
                    )}
                  >
                    <div className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                      <div className="flex items-start gap-3 flex-1 min-w-0">
                        {/* Status Icon */}
                        <div className="mt-0.5 flex-shrink-0">
                          {isCompleted ? (
                            <CheckCircle2 className="w-5 h-5 text-green-400" />
                          ) : isInProgress ? (
                            <div className="w-5 h-5 rounded-full border-2 border-blue-400 border-t-transparent animate-spin" />
                          ) : (
                            <div className="w-5 h-5 rounded-full border border-cyber-muted flex items-center justify-center">
                              <div className="w-1.5 h-1.5 rounded-full bg-cyber-muted/40" />
                            </div>
                          )}
                        </div>

                        {/* Title & Metadata */}
                        <div className="flex-1 min-w-0">
                          <div className="flex flex-wrap items-center gap-2 mb-1">
                            {topic.day_number && (
                              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-cyber-darker text-cyber-neon border border-cyber-neon/30">
                                Day {topic.day_number}
                              </span>
                            )}
                            <span className={clsx(
                              "text-[10px] font-mono uppercase px-2 py-0.5 rounded border",
                              topic.difficulty === 'beginner' && "text-emerald-400 bg-emerald-950/30 border-emerald-500/30",
                              topic.difficulty === 'intermediate' && "text-blue-400 bg-blue-950/30 border-blue-500/30",
                              topic.difficulty === 'advanced' && "text-amber-400 bg-amber-950/30 border-amber-500/30",
                              topic.difficulty === 'expert' && "text-purple-400 bg-purple-950/30 border-purple-500/30",
                            )}>
                              {topic.difficulty}
                            </span>
                            <span className="text-[10px] text-cyber-muted flex items-center gap-1 font-mono">
                              <Clock className="w-3 h-3" /> {topic.estimated_hours}h
                            </span>
                          </div>

                          <h4 className="font-semibold text-sm text-white leading-snug">
                            {topic.name}
                          </h4>
                          {topic.description && (
                            <p className="text-xs text-gray-400 mt-1 line-clamp-2 leading-relaxed">
                              {topic.description}
                            </p>
                          )}
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex items-center gap-2 sm:self-center flex-shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-cyber-border/40">
                        {topic.objectives && topic.objectives.length > 0 && (
                          <button
                            onClick={() => toggleTopicExpand(topic.id)}
                            className="p-2 text-xs font-mono text-cyber-muted hover:text-white rounded-lg hover:bg-cyber-darker transition-colors flex items-center gap-1"
                            title="Toggle Objectives"
                          >
                            <Target className="w-3.5 h-3.5 text-cyber-neon" />
                            <span>{topic.objectives.length}</span>
                            <ChevronDown className={clsx(
                              "w-3.5 h-3.5 transition-transform duration-200",
                              isExpanded && "transform rotate-180 text-cyber-neon"
                            )} />
                          </button>
                        )}

                        <button
                          onClick={() => handleLaunchDay(topic.day_number)}
                          className="px-3 py-1.5 bg-cyber-neon/10 hover:bg-cyber-neon/25 text-cyber-neon border border-cyber-neon/30 hover:border-cyber-neon/60 rounded-lg text-xs font-medium flex items-center gap-1.5 transition-all shadow-sm group"
                        >
                          <span>Launch Day {topic.day_number}</span>
                          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                        </button>
                      </div>
                    </div>

                    {/* Expandable Objectives Sub-panel */}
                    {isExpanded && topic.objectives && topic.objectives.length > 0 && (
                      <div className="px-4 pb-4 pt-2 bg-cyber-darker/70 border-t border-cyber-border/40 space-y-2">
                        <p className="text-[10px] font-mono text-cyber-muted uppercase tracking-wider flex items-center gap-1">
                          <Target className="w-3 h-3 text-cyber-neon" /> Measurable Learning Objectives
                        </p>
                        <div className="space-y-1.5">
                          {topic.objectives.map((obj) => (
                            <div
                              key={obj.id}
                              className="flex items-start gap-2.5 p-2 rounded-lg bg-cyber-card/40 border border-cyber-border/30 text-xs text-gray-300"
                            >
                              <div className="w-4 h-4 rounded-full border border-cyber-neon/40 flex-shrink-0 mt-0.5 flex items-center justify-center">
                                <div className="w-1.5 h-1.5 rounded-full bg-cyber-neon" />
                              </div>
                              <p className="leading-relaxed">{obj.description}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
