import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ShieldAlert, UserPlus, AlertCircle } from 'lucide-react';
import { api } from '../lib/api';
import { useAuthStore } from '../store/useAuthStore';

export function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const navigate = useNavigate();
  const { setUser } = useAuthStore();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      // 1. Register the user
      await api.post('/api/v1/auth/register', {
        email,
        password,
        display_name: displayName
      });

      // 2. Automatically log them in after registration
      const loginResponse = await api.post('/api/v1/auth/login', {
        email,
        password,
      });

      const { access_token, user } = loginResponse.data;
      localStorage.setItem('auth_token', access_token);
      setUser(user);
      navigate('/');
    } catch (err: any) {
      if (err.response?.data?.detail) {
        // FastAPI sometimes sends detail as an array of validation errors
        const detail = err.response.data.detail;
        if (Array.isArray(detail)) {
          setError(detail[0].msg);
        } else {
          setError(detail);
        }
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cyber-dark flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-[url('/grid-pattern.svg')] bg-repeat">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <ShieldAlert className="w-12 h-12 text-cyber-neon" />
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-white tracking-widest">
          CYBER<span className="text-cyber-neon">TRAINER</span>
        </h2>
        <p className="mt-2 text-center text-sm text-cyber-muted">
          Request system access
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="glass-panel py-8 px-4 shadow sm:rounded-lg sm:px-10 border border-cyber-border relative overflow-hidden">
          
          <form className="space-y-6 relative z-10" onSubmit={handleRegister}>
            {error && (
              <div className="bg-red-500/10 border border-red-500/50 rounded-md p-4 flex items-start">
                <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" />
                <p className="text-sm text-red-200">{error}</p>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-300">
                Display Name / Handle
              </label>
              <div className="mt-1">
                <input
                  type="text"
                  required
                  value={displayName}
                  onChange={(e) => setDisplayName(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-cyber-border rounded-md shadow-sm bg-cyber-darker text-white focus:outline-none focus:ring-cyber-neon focus:border-cyber-neon sm:text-sm transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300">
                Email address
              </label>
              <div className="mt-1">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-cyber-border rounded-md shadow-sm bg-cyber-darker text-white focus:outline-none focus:ring-cyber-neon focus:border-cyber-neon sm:text-sm transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300">
                Password
              </label>
              <div className="mt-1">
                <input
                  type="password"
                  required
                  minLength={8}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 border border-cyber-border rounded-md shadow-sm bg-cyber-darker text-white focus:outline-none focus:ring-cyber-neon focus:border-cyber-neon sm:text-sm transition-colors"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-bold text-cyber-darker bg-cyber-neon hover:bg-[#00e68d] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyber-neon transition-colors disabled:opacity-50"
              >
                {isLoading ? 'PROCESSING...' : (
                  <>
                    <UserPlus className="w-5 h-5 mr-2" />
                    CREATE ACCOUNT
                  </>
                )}
              </button>
            </div>
          </form>
          
          <div className="mt-6 text-center relative z-10">
            <p className="text-sm text-cyber-muted">
              Already have access?{' '}
              <Link to="/login" className="font-medium text-cyber-neon hover:text-[#00e68d]">
                Login here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
