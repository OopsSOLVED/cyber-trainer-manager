import { create } from 'zustand';

interface User {
  id: number;
  email: string;
  display_name: string;
  is_superuser: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true, // Initially true while we check for token
  
  setUser: (user) => set({ 
    user, 
    isAuthenticated: !!user,
    isLoading: false
  }),
  
  logout: () => {
    localStorage.removeItem('auth_token');
    set({ user: null, isAuthenticated: false, isLoading: false });
  },
}));
