import { Navigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/useAuthStore';
import { useEffect, useState } from 'react';
import { api } from '../../lib/api';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, setUser } = useAuthStore();
  const location = useLocation();
  const [isVerifying, setIsVerifying] = useState(isLoading);

  useEffect(() => {
    const verifyAuth = async () => {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        setIsVerifying(false);
        return;
      }
      
      try {
        // Just checking if token is still valid
        const response = await api.get('/api/v1/auth/me');
        setUser(response.data);
      } catch (error) {
        // Interceptor handles the local storage clearing
        console.error("Auth verification failed", error);
      } finally {
        setIsVerifying(false);
      }
    };

    if (isLoading) {
      verifyAuth();
    } else {
      setIsVerifying(false);
    }
  }, [isLoading, setUser]);

  if (isVerifying) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-cyber-dark">
        <div className="text-cyber-neon text-xl font-bold animate-pulse tracking-widest">
          INITIALIZING...
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect to login but save the attempted location
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
