import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShieldCheck, Sparkles, Bell, Search, User, LogOut, Settings, FolderGit2, Menu, X } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

interface NavbarProps {
  onToggleMobileMenu?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onToggleMobileMenu }) => {
  const { user, logout } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [profileOpen, setProfileOpen] = useState(false);

  const handleLogout = () => {
    logout();
    showToast('info', 'Logged out', 'You have been signed out of your session.');
    navigate('/login');
  };

  return (
    <header className="h-14 border-b border-surface-border bg-white sticky top-0 z-30 px-4 md:px-6 flex items-center justify-between shadow-subtle">
      <div className="flex items-center space-x-3">
        <button
          onClick={onToggleMobileMenu}
          className="md:hidden p-1.5 rounded-lg text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors"
          aria-label="Toggle Navigation"
        >
          <Menu className="w-5 h-5" />
        </button>

        <Link to="/" className="flex items-center space-x-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center text-white shadow-sm group-hover:bg-brand-600 transition-colors">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div className="flex items-baseline space-x-1.5">
            <span className="font-bold text-base tracking-tight text-text-primary">
              CodeReview<span className="text-brand-500">AI</span>
            </span>
          </div>
        </Link>

        <span className="hidden sm:inline-flex items-center px-2 py-0.5 text-[11px] font-semibold bg-brand-50 text-brand-700 border border-brand-200 rounded-md">
          v1.0 Hybrid Engine
        </span>
      </div>

      <div className="flex items-center space-x-3 sm:space-x-4">
        <div className="hidden lg:flex items-center space-x-2 bg-surface-subtle border border-surface-border rounded-lg px-2.5 py-1 text-xs text-text-secondary">
          <FolderGit2 className="w-3.5 h-3.5 text-brand-500" />
          <span className="font-medium text-text-primary">acme-corp/ecommerce-api</span>
          <span className="text-text-muted">• (main)</span>
        </div>

        <div className="relative">
          <button
            onClick={() => setProfileOpen(!profileOpen)}
            className="flex items-center space-x-2 p-1.5 rounded-lg hover:bg-surface-subtle transition-colors text-text-primary"
          >
            <div className="w-7 h-7 rounded-full bg-brand-100 border border-brand-200 flex items-center justify-center text-xs font-bold text-brand-700">
              {user?.username?.substring(0, 2).toUpperCase() || 'LR'}
            </div>
            <span className="hidden md:inline text-xs font-semibold text-text-primary">{user?.username || 'lead_reviewer'}</span>
          </button>

          {profileOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white border border-surface-border rounded-xl shadow-elevated py-1 z-40">
              <div className="px-3 py-2 border-b border-surface-border text-xs">
                <p className="font-semibold text-text-primary">{user?.username}</p>
                <p className="text-text-secondary text-[11px] truncate">{user?.email}</p>
              </div>
              <Link
                to="/settings"
                onClick={() => setProfileOpen(false)}
                className="flex items-center space-x-2 px-3 py-2 text-xs text-text-secondary hover:text-text-primary hover:bg-surface-subtle transition-colors"
              >
                <Settings className="w-3.5 h-3.5" />
                <span>Settings</span>
              </Link>
              <button
                onClick={handleLogout}
                className="w-full flex items-center space-x-2 px-3 py-2 text-xs text-accent-red hover:bg-accent-redLight transition-colors"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>Sign Out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
