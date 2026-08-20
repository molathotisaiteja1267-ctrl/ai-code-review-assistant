import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Code2, 
  GitPullRequest, 
  History, 
  BookOpen, 
  BarChart3,
  Settings,
  ShieldCheck,
  X
} from 'lucide-react';

interface SidebarProps {
  mobileOpen?: boolean;
  onCloseMobile?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ mobileOpen, onCloseMobile }) => {
  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/reviews/new', label: 'New Review', icon: Code2 },
    { to: '/github', label: 'GitHub PR Reviews', icon: GitPullRequest },
    { to: '/history', label: 'Review History', icon: History },
    { to: '/rules', label: 'Project Rules (RAG)', icon: BookOpen },
    { to: '/evaluation', label: 'AI Evaluation & Benchmarks', icon: BarChart3 },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  const sidebarContent = (
    <div className="flex flex-col justify-between h-full p-3 bg-white">
      <div className="space-y-1">
        <div className="flex items-center justify-between px-3 py-2 text-[11px] font-bold tracking-wider text-text-muted uppercase">
          <span>Review Workspace</span>
          {mobileOpen && (
            <button onClick={onCloseMobile} className="md:hidden p-1 text-text-secondary hover:text-text-primary">
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={onCloseMobile}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-brand-50 text-brand-600 font-semibold shadow-subtle border-l-4 border-brand-500'
                    : 'text-text-secondary hover:text-text-primary hover:bg-surface-subtle'
                }`
              }
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      <div className="p-3 bg-surface-subtle border border-surface-border rounded-xl space-y-1.5">
        <div className="flex items-center space-x-1.5 text-xs font-semibold text-text-primary">
          <ShieldCheck className="w-4 h-4 text-accent-green" />
          <span>Safety Validator Active</span>
        </div>
        <p className="text-[11px] text-text-secondary leading-relaxed">
          In-memory AST & Bandit regression validation on all suggested patches.
        </p>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex w-60 border-r border-surface-border bg-white flex-col shrink-0 min-h-[calc(100vh-3.5rem)] shadow-subtle">
        {sidebarContent}
      </aside>

      {/* Mobile Drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-40 flex md:hidden">
          <div className="fixed inset-0 bg-gray-900/30 backdrop-blur-xs" onClick={onCloseMobile} />
          <div className="relative w-64 max-w-[80%] bg-white h-full shadow-2xl z-50">
            {sidebarContent}
          </div>
        </div>
      )}
    </>
  );
};
