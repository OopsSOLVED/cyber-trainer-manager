import { useEffect, useState } from 'react';
import { api } from '../lib/api';
import type { Phase, SkillLayer, Domain, Topic, Objective } from '../types/curriculum';
import { ChevronRight, ChevronDown, BookOpen, Target, Clock, Shield } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function TopicNode({ topic }: { topic: Topic }) {
  const [isOpen, setIsOpen] = useState(false);
  const [objectives, setObjectives] = useState<Objective[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const toggle = async () => {
    if (!isOpen && !objectives) {
      setIsLoading(true);
      try {
        const res = await api.get(`/api/v1/curriculum/topics/${topic.id}`);
        setObjectives(res.data.objectives);
      } catch (e) {
        console.error(e);
      } finally {
        setIsLoading(false);
      }
    }
    setIsOpen(!isOpen);
  };

  return (
    <div className="ml-6 mt-2 border-l border-cyber-border pl-4">
      <div 
        className="flex items-center cursor-pointer group py-2"
        onClick={toggle}
      >
        <span className="text-gray-400 group-hover:text-blue-400 mr-2 transition-colors">
          {isOpen ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </span>
        <div className="flex-1">
          <span className="text-gray-300 font-medium group-hover:text-blue-400 transition-colors text-sm">
            Topic {topic.order}: {topic.name}
          </span>
          <div className="flex items-center mt-1 space-x-3 text-xs text-cyber-muted">
            {topic.day_number && <span className="flex items-center"><Clock className="w-3 h-3 mr-1"/> Day {topic.day_number}</span>}
            <span className="flex items-center"><Target className="w-3 h-3 mr-1"/> {topic.estimated_hours}h</span>
            <span className="uppercase text-blue-500/80">{topic.difficulty}</span>
          </div>
        </div>
      </div>
      
      {isOpen && (
        <div className="mt-2 mb-4 ml-6 space-y-2">
          {isLoading && <p className="text-xs text-cyber-muted animate-pulse">Loading objectives...</p>}
          {objectives?.map(obj => (
            <div key={obj.id} className="flex items-start text-sm text-gray-400 bg-cyber-darker p-2 rounded border border-cyber-border/50">
              <div className="w-4 h-4 rounded-full border border-cyber-muted flex-shrink-0 mt-0.5 mr-3 flex items-center justify-center">
                {obj.is_measurable && <div className="w-1.5 h-1.5 bg-cyber-neon rounded-full"></div>}
              </div>
              <p>{obj.description}</p>
            </div>
          ))}
          {objectives?.length === 0 && <p className="text-xs text-cyber-muted">No objectives defined.</p>}
        </div>
      )}
    </div>
  );
}

function DomainNode({ domain }: { domain: Domain }) {
  const [isOpen, setIsOpen] = useState(false);
  const [topics, setTopics] = useState<Topic[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const toggle = async () => {
    if (!isOpen && !topics) {
      setIsLoading(true);
      try {
        const res = await api.get(`/api/v1/curriculum/domains/${domain.id}`);
        setTopics(res.data.topics);
      } catch (e) {
        console.error(e);
      } finally {
        setIsLoading(false);
      }
    }
    setIsOpen(!isOpen);
  };

  return (
    <div className="ml-6 mt-3 border-l-2 border-cyber-border/70 pl-4">
      <div 
        className="flex items-center cursor-pointer group py-2"
        onClick={toggle}
      >
        <span className="text-gray-400 group-hover:text-purple-400 mr-2 transition-colors">
          {isOpen ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </span>
        <div>
          <span className="text-gray-200 font-medium group-hover:text-purple-400 transition-colors">
            Domain {domain.order}: {domain.name}
          </span>
          <p className="text-xs text-cyber-muted mt-0.5">{domain.description}</p>
        </div>
      </div>
      {isOpen && (
        <div className="mt-2 mb-4">
          {isLoading && <p className="text-xs text-cyber-muted ml-6 animate-pulse">Loading topics...</p>}
          {topics?.map(topic => <TopicNode key={topic.id} topic={topic} />)}
        </div>
      )}
    </div>
  );
}

function SkillLayerNode({ layer }: { layer: SkillLayer }) {
  const [isOpen, setIsOpen] = useState(false);
  const [domains, setDomains] = useState<Domain[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const toggle = async () => {
    if (!isOpen && !domains) {
      setIsLoading(true);
      try {
        const res = await api.get(`/api/v1/curriculum/skill-layers/${layer.id}`);
        setDomains(res.data.domains);
      } catch (e) {
        console.error(e);
      } finally {
        setIsLoading(false);
      }
    }
    setIsOpen(!isOpen);
  };

  return (
    <div className="ml-6 mt-4 border-l-2 border-cyber-accent/30 pl-4">
      <div 
        className="flex items-center cursor-pointer group py-2"
        onClick={toggle}
      >
        <span className="text-cyber-accent group-hover:text-cyber-neon mr-2 transition-colors">
          {isOpen ? <ChevronDown className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
        </span>
        <div>
          <span className="text-lg text-white font-semibold group-hover:text-cyber-neon transition-colors">
            Layer {layer.order}: {layer.name}
          </span>
          <p className="text-sm text-cyber-muted mt-0.5">{layer.description}</p>
        </div>
      </div>
      {isOpen && (
        <div className="mt-2 mb-4">
          {isLoading && <p className="text-xs text-cyber-muted ml-6 animate-pulse">Loading domains...</p>}
          {domains?.map(domain => <DomainNode key={domain.id} domain={domain} />)}
        </div>
      )}
    </div>
  );
}

export function Curriculum() {
  const [phases, setPhases] = useState<Phase[]>([]);
  const [expandedPhaseId, setExpandedPhaseId] = useState<number | null>(null);
  const [phaseLayers, setPhaseLayers] = useState<Record<number, SkillLayer[]>>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    api.get('/api/v1/curriculum/phases')
      .then(res => setPhases(res.data))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  const togglePhase = async (phase: Phase) => {
    if (expandedPhaseId === phase.id) {
      setExpandedPhaseId(null);
      return;
    }

    setExpandedPhaseId(phase.id);
    if (!phaseLayers[phase.id]) {
      try {
        const res = await api.get(`/api/v1/curriculum/phases/${phase.id}`);
        setPhaseLayers(prev => ({ ...prev, [phase.id]: res.data.skill_layers }));
      } catch (e) {
        console.error(e);
      }
    }
  };

  return (
    <div className="max-w-5xl mx-auto pb-12">
      <div className="flex items-center mb-8">
        <Shield className="w-8 h-8 text-cyber-neon mr-3" />
        <div>
          <h1 className="text-2xl font-bold text-white tracking-widest uppercase">Curriculum Master Plan</h1>
          <p className="text-cyber-muted text-sm mt-1">196-Day Cybersecurity Operations Roadmap</p>
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center p-12">
          <p className="text-cyber-neon animate-pulse font-mono">LOADING CURRICULUM DATA...</p>
        </div>
      ) : (
        <div className="space-y-6">
          {phases.map(phase => {
            const isOpen = expandedPhaseId === phase.id;
            const layers = phaseLayers[phase.id];

            return (
              <div key={phase.id} className="glass-panel rounded-xl overflow-hidden border border-cyber-border transition-all duration-300">
                <div 
                  className={twMerge(
                    clsx(
                      "p-5 flex items-center justify-between cursor-pointer transition-colors",
                      isOpen ? "bg-cyber-darker border-b border-cyber-border" : "hover:bg-cyber-darker"
                    )
                  )}
                  onClick={() => togglePhase(phase)}
                >
                  <div className="flex items-center">
                    <div className="w-12 h-12 rounded-lg bg-cyber-card border border-cyber-border flex items-center justify-center mr-4 shadow-sm">
                      <BookOpen className={clsx("w-6 h-6", isOpen ? "text-cyber-neon" : "text-cyber-muted")} />
                    </div>
                    <div>
                      <h2 className="text-xl font-bold text-white uppercase tracking-wide">Phase {phase.order}: {phase.name}</h2>
                      <p className="text-sm text-cyber-muted mt-1">{phase.description}</p>
                    </div>
                  </div>
                  <ChevronDown className={clsx("w-6 h-6 text-cyber-muted transition-transform duration-300", isOpen && "transform rotate-180 text-cyber-neon")} />
                </div>
                
                {isOpen && (
                  <div className="p-6 bg-cyber-darker/50">
                    {!layers ? (
                      <p className="text-sm text-cyber-muted animate-pulse">Loading skill layers...</p>
                    ) : (
                      <div className="space-y-2">
                        {layers.map(layer => <SkillLayerNode key={layer.id} layer={layer} />)}
                      </div>
                    )}
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
