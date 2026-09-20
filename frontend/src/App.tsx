import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { Dashboard } from './pages/Dashboard';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { Tasks } from './pages/Tasks';
import { Today } from './pages/Today';
import { Roadmap } from './pages/Roadmap';

// Dummy components for unbuilt routes
const Placeholder = ({ title }: { title: string }) => (
  <div className="flex items-center justify-center h-full">
    <div className="glass-panel p-8 rounded-xl text-center">
      <h2 className="text-2xl font-bold text-cyber-neon mb-2">{title}</h2>
      <p className="text-cyber-muted">Module under construction</p>
    </div>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/" element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="today" element={<Today />} />
          <Route path="tasks" element={<Tasks />} />
          <Route path="roadmap" element={<Roadmap />} />
          <Route path="curriculum" element={<Roadmap />} />
          <Route path="labs" element={<Placeholder title="Labs & CTFs" />} />
          <Route path="settings" element={<Placeholder title="Settings" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}


export default App;
