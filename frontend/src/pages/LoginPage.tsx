import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ShieldCheck, LogIn, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { apiClient } from '../services/api';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { showToast } = useToast();
  const [email, setEmail] = useState('lead.reviewer@acme.dev');
  const [password, setPassword] = useState('securepassword123');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await apiClient.post('/auth/login', { email, password });
      login(res.data.access_token, res.data.user);
      showToast('success', 'Welcome back', `Logged in as ${res.data.user.username}`);
      navigate('/');
    } catch (err: any) {
      // If user doesn't exist yet, auto register for seamless demo
      try {
        const reg = await apiClient.post('/auth/register', { email, username: email.split('@')[0], password });
        login(reg.data.access_token, reg.data.user);
        showToast('success', 'Account created', `Logged in as ${reg.data.user.username}`);
        navigate('/');
      } catch (regErr: any) {
        showToast('error', 'Login Failed', 'Please verify your credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-bg flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white border border-surface-border rounded-2xl p-8 shadow-elevated space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-xl bg-brand-500 text-white flex items-center justify-center mx-auto shadow-sm">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-text-primary">Sign in to CodeReviewAI</h2>
          <p className="text-xs text-text-secondary">AI-powered code quality and security analysis platform</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-text-primary">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-text-primary">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white flex items-center justify-center space-x-2 shadow-sm transition-all disabled:opacity-50"
          >
            <LogIn className="w-4 h-4" />
            <span>{loading ? 'Authenticating...' : 'Sign In to Workspace'}</span>
          </button>
        </form>

        <div className="p-3 bg-surface-subtle border border-surface-border rounded-xl text-center text-[11px] text-text-secondary">
          <span>Demo Account: </span>
          <span className="font-mono font-semibold text-text-primary">lead.reviewer@acme.dev</span>
        </div>
      </div>
    </div>
  );
};
