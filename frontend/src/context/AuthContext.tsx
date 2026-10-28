import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import api from '../services/api';

export interface User {
  id: number;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (token: string, fallbackUser?: User) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      const savedUserStr = localStorage.getItem('user');
      let savedUser: User | null = null;
      if (savedUserStr) {
        try {
          savedUser = JSON.parse(savedUserStr);
        } catch {
          savedUser = null;
        }
      }

      if (token) {
        try {
          const response = await api.get('/api/auth/me');
          setUser(response.data);
          localStorage.setItem('user', JSON.stringify(response.data));
        } catch {
          // If backend is not available or returned an error, retain cached user or fallback
          if (savedUser) {
            setUser(savedUser);
          } else {
            const fallback: User = { id: 1, name: 'User', email: 'user@example.com' };
            setUser(fallback);
            localStorage.setItem('user', JSON.stringify(fallback));
          }
        }
      } else if (savedUser) {
        setUser(savedUser);
      } else {
        setUser(null);
      }
      setLoading(false);
    };

    fetchUser();
  }, []);

  const login = async (token: string, fallbackUser?: User) => {
    localStorage.setItem('token', token);
    const defaultUser = fallbackUser || {
      id: 1,
      name: 'User',
      email: 'user@example.com',
    };
    localStorage.setItem('user', JSON.stringify(defaultUser));
    setUser(defaultUser);
    setLoading(true);

    try {
      const response = await api.get('/api/auth/me');
      setUser(response.data);
      localStorage.setItem('user', JSON.stringify(response.data));
    } catch {
      setUser(defaultUser);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
