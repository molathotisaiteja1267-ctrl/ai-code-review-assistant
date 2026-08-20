import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Code2, 
  GitPullRequest, 
  ArrowUpRight, 
  Activity, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle2, 
  BarChart3, 
  BookOpen, 
  Calendar,
  Layers
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  PieChart, 
  Pie, 
  Cell 
} from 'recharts';
import { reviewService } from '../services/reviewService';
import { DashboardStats } from '../types';

export const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('30');

  useEffect(() => {
    fetchStats(timeRange);
  }, [timeRange]);

  const fetchStats = async (days: string) => {
    setLoading(true);
    try {
      const data = await reviewService.getDashboardStats(days);
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const SEVERITY_COLORS: Record<string, string> = {
    'Critical': '#e53935',
    'High': '#f4511e',
    'Medium': '#ffc107',
    'Low': '#1976d2',
  };

  const severityPieData = stats?.severity_distribution
    ? Object.entries(stats.severity_distribution).map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div className="space-y-6">
      {/* Top Header Section */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-2 border-b border-surface-border">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Dashboard</h1>
          <p className="text-xs text-text-secondary mt-0.5">
            Overview of code quality, security posture, and review telemetry.
          </p>
        </div>

        <div className="flex items-center space-x-3 w-full sm:w-auto">
          {/* Time range filter */}
          <div className="flex items-center space-x-1 bg-white border border-surface-border rounded-lg p-1 text-xs shadow-subtle">
            {['7', '30', '90', 'all'].map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-2.5 py-1 rounded-md font-semibold transition-colors ${
                  timeRange === range
                    ? 'bg-brand-500 text-white'
                    : 'text-text-secondary hover:text-text-primary hover:bg-surface-subtle'
                }`}
              >
                {range === 'all' ? 'All Time' : `${range}D`}
              </button>
            ))}
          </div>

          <Link
            to="/reviews/new"
            className="px-4 py-2 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white flex items-center space-x-1.5 shadow-sm transition-all shrink-0"
          >
            <Code2 className="w-4 h-4" />
            <span>New Review</span>
          </Link>
        </div>
      </div>

      {/* Metrics Stat Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-2 shadow-subtle">
          <div className="flex items-center justify-between text-text-secondary text-xs font-semibold uppercase tracking-wider">
            <span>Total Reviews</span>
            <Code2 className="w-4 h-4 text-brand-500" />
          </div>
          <div className="text-3xl font-bold text-text-primary">{stats?.total_reviews || 0}</div>
          <p className="text-[11px] text-text-secondary">Across paste, upload, and PR reviews</p>
        </div>

        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-2 shadow-subtle">
          <div className="flex items-center justify-between text-text-secondary text-xs font-semibold uppercase tracking-wider">
            <span>Critical Findings</span>
            <AlertTriangle className="w-4 h-4 text-accent-red" />
          </div>
          <div className="text-3xl font-bold text-accent-red">{stats?.critical_issues || 0}</div>
          <p className="text-[11px] text-text-secondary">Requires immediate remediation</p>
        </div>

        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-2 shadow-subtle">
          <div className="flex items-center justify-between text-text-secondary text-xs font-semibold uppercase tracking-wider">
            <span>Average Quality Score</span>
            <TrendingUp className="w-4 h-4 text-accent-green" />
          </div>
          <div className="text-3xl font-bold text-text-primary">
            {stats?.average_code_quality || 100.0}
            <span className="text-xs font-normal text-text-muted">/100</span>
          </div>
          <p className="text-[11px] text-text-secondary">Weighted multi-category index</p>
        </div>

        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-2 shadow-subtle">
          <div className="flex items-center justify-between text-text-secondary text-xs font-semibold uppercase tracking-wider">
            <span>Average Risk Score</span>
            <Activity className="w-4 h-4 text-amber-600" />
          </div>
          <div className="text-3xl font-bold text-text-primary">
            {stats?.average_risk_score || 1.0}
            <span className="text-xs font-normal text-text-muted">/10</span>
          </div>
          <p className="text-[11px] text-text-secondary">Exploitability and blast radius</p>
        </div>
      </div>

      {/* Quick Actions Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <Link
          to="/reviews/new"
          className="p-3 bg-white border border-surface-border rounded-xl hover:border-brand-300 hover:bg-surface-hover transition-all flex items-center space-x-2.5 shadow-subtle group"
        >
          <div className="w-8 h-8 rounded-lg bg-brand-50 border border-brand-100 flex items-center justify-center text-brand-600 group-hover:bg-brand-500 group-hover:text-white transition-colors">
            <Code2 className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-text-primary">Paste Code</div>
            <div className="text-[11px] text-text-muted">Quick single-file scan</div>
          </div>
        </Link>

        <Link
          to="/github"
          className="p-3 bg-white border border-surface-border rounded-xl hover:border-brand-300 hover:bg-surface-hover transition-all flex items-center space-x-2.5 shadow-subtle group"
        >
          <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-100 flex items-center justify-center text-accent-blue group-hover:bg-accent-blue group-hover:text-white transition-colors">
            <GitPullRequest className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-text-primary">Review Pull Request</div>
            <div className="text-[11px] text-text-muted">Line-by-line diff review</div>
          </div>
        </Link>

        <Link
          to="/rules"
          className="p-3 bg-white border border-surface-border rounded-xl hover:border-brand-300 hover:bg-surface-hover transition-all flex items-center space-x-2.5 shadow-subtle group"
        >
          <div className="w-8 h-8 rounded-lg bg-amber-50 border border-amber-100 flex items-center justify-center text-amber-700 group-hover:bg-amber-600 group-hover:text-white transition-colors">
            <BookOpen className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-text-primary">Project Rules (RAG)</div>
            <div className="text-[11px] text-text-muted">Architecture guidelines</div>
          </div>
        </Link>

        <Link
          to="/evaluation"
          className="p-3 bg-white border border-surface-border rounded-xl hover:border-brand-300 hover:bg-surface-hover transition-all flex items-center space-x-2.5 shadow-subtle group"
        >
          <div className="w-8 h-8 rounded-lg bg-green-50 border border-green-100 flex items-center justify-center text-accent-green group-hover:bg-accent-green group-hover:text-white transition-colors">
            <BarChart3 className="w-4 h-4" />
          </div>
          <div>
            <div className="text-xs font-bold text-text-primary">Run Benchmark</div>
            <div className="text-[11px] text-text-muted">Precision & recall test</div>
          </div>
        </Link>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trend Area Chart */}
        <div className="lg:col-span-2 bg-white border border-surface-border rounded-xl p-5 space-y-4 shadow-subtle">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-text-primary">Code Quality Score Over Time</h3>
            <span className="text-xs text-text-secondary">Selected: {timeRange === 'all' ? 'All Time' : `${timeRange} Days`}</span>
          </div>

          <div className="h-60 w-full">
            {stats?.quality_trends && stats.quality_trends.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={stats.quality_trends}>
                  <defs>
                    <linearGradient id="scoreOrangeGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ff6a00" stopOpacity={0.25}/>
                      <stop offset="95%" stopColor="#ff6a00" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="date" stroke="#9ca3af" fontSize={11} tickLine={false} />
                  <YAxis stroke="#9ca3af" fontSize={11} domain={[0, 100]} tickLine={false} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e8e0d8', borderRadius: '8px', fontSize: '12px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}
                  />
                  <Area type="monotone" dataKey="score" stroke="#ff6a00" strokeWidth={2.5} fillOpacity={1} fill="url(#scoreOrangeGrad)" name="Quality Score" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-text-muted">
                No trend data recorded for this time range.
              </div>
            )}
          </div>
        </div>

        {/* Severity Pie Chart */}
        <div className="bg-white border border-surface-border rounded-xl p-5 space-y-4 shadow-subtle">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-text-primary">Severity Distribution</h3>
            <span className="text-xs text-text-secondary">All Findings</span>
          </div>

          <div className="h-60 w-full flex flex-col items-center justify-center">
            {severityPieData.length > 0 && severityPieData.some(d => d.value > 0) ? (
              <>
                <ResponsiveContainer width="100%" height={160}>
                  <PieChart>
                    <Pie
                      data={severityPieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={45}
                      outerRadius={70}
                      paddingAngle={4}
                      dataKey="value"
                    >
                      {severityPieData.map((entry) => (
                        <Cell key={entry.name} fill={SEVERITY_COLORS[entry.name] || '#9ca3af'} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e8e0d8', borderRadius: '8px', fontSize: '12px' }} />
                  </PieChart>
                </ResponsiveContainer>
                <div className="flex flex-wrap items-center justify-center gap-3 pt-2 text-[11px] font-medium text-text-secondary">
                  {severityPieData.map((s) => (
                    <div key={s.name} className="flex items-center space-x-1">
                      <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: SEVERITY_COLORS[s.name] }} />
                      <span>{s.name}: {s.value}</span>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <div className="text-xs text-text-muted">No findings recorded in this period.</div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Reviews Table */}
      <div className="bg-white border border-surface-border rounded-xl overflow-hidden shadow-subtle">
        <div className="p-4 border-b border-surface-border flex items-center justify-between">
          <div>
            <h3 className="text-sm font-bold text-text-primary">Recent Code Reviews</h3>
            <p className="text-[11px] text-text-secondary">Latest automated scans across repositories and snippets</p>
          </div>
          <Link to="/history" className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center space-x-1">
            <span>View All</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-text-primary">
            <thead className="bg-surface-subtle text-text-secondary uppercase font-semibold text-[10px] tracking-wider border-b border-surface-border">
              <tr>
                <th className="px-5 py-3">Review ID</th>
                <th className="px-5 py-3">Title / Target</th>
                <th className="px-5 py-3">Source</th>
                <th className="px-5 py-3">Quality Score</th>
                <th className="px-5 py-3">Risk Level</th>
                <th className="px-5 py-3">Issues</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-border">
              {stats?.recent_reviews && stats.recent_reviews.length > 0 ? (
                stats.recent_reviews.map((r) => (
                  <tr key={r.id} className="hover:bg-surface-hover transition-colors">
                    <td className="px-5 py-3.5 font-mono text-[11px] text-text-muted">#{r.id}</td>
                    <td className="px-5 py-3.5 font-semibold text-text-primary">
                      <Link to={`/reviews/${r.id}`} className="hover:text-brand-600 transition-colors">
                        {r.title}
                      </Link>
                    </td>
                    <td className="px-5 py-3.5 uppercase text-[10px] text-text-secondary font-mono">{r.source_type}</td>
                    <td className="px-5 py-3.5">
                      <span className="font-bold text-text-primary bg-surface-subtle px-2 py-0.5 rounded border border-surface-border">
                        {r.letter_grade} ({r.overall_score.toFixed(0)})
                      </span>
                    </td>
                    <td className="px-5 py-3.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        r.risk_level === 'CRITICAL' ? 'bg-accent-redLight text-accent-red border border-red-200' :
                        r.risk_level === 'HIGH' ? 'bg-orange-50 text-brand-600 border border-brand-200' :
                        r.risk_level === 'MEDIUM' ? 'bg-accent-yellowLight text-amber-800 border border-amber-200' :
                        'bg-accent-greenLight text-accent-green border border-green-200'
                      }`}>
                        {r.risk_level}
                      </span>
                    </td>
                    <td className="px-5 py-3.5 text-text-secondary">{r.issues_count} found</td>
                    <td className="px-5 py-3.5">
                      <span className="inline-flex items-center space-x-1 text-[11px] font-medium text-accent-green">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Completed</span>
                      </span>
                    </td>
                    <td className="px-5 py-3.5 text-right">
                      <Link
                        to={`/reviews/${r.id}`}
                        className="text-xs font-semibold text-brand-600 hover:text-brand-700 bg-brand-50 hover:bg-brand-100 px-2.5 py-1 rounded-md transition-colors"
                      >
                        Inspect →
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={8} className="px-5 py-8 text-center text-text-muted">
                    No reviews in this period. Click "New Review" to scan your first codebase.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
