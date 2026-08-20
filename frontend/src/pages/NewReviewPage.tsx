import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Code2, Upload, FileCode, Play, CheckCircle2, Shield, Bug, Gauge, Cpu } from 'lucide-react';
import { reviewService } from '../services/reviewService';
import { MonacoCodeEditor } from '../components/editor/MonacoCodeEditor';
import { useToast } from '../context/ToastContext';

export const NewReviewPage: React.FC = () => {
  const navigate = useNavigate();
  const { showToast } = useToast();
  const [tab, setTab] = useState<'paste' | 'upload'>('paste');
  const [title, setTitle] = useState('auth_controller.py');
  const [language, setLanguage] = useState('python');
  const [sourceCode, setSourceCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentStage, setCurrentStage] = useState('');
  const [scopes, setScopes] = useState({
    security: true,
    reliability: true,
    performance: true,
    maintainability: true,
  });

  const presets = [
    {
      name: 'SQL Injection Vulnerability',
      desc: 'Raw string concatenation in cursor.execute',
      code: `import sqlite3

def get_user_profile(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Vulnerable direct SQL concatenation
    query = f"SELECT id, username, email, is_admin FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    return cursor.fetchone()`
    },
    {
      name: 'Command Injection & Secret',
      desc: 'Shell=True subprocess and exposed AWS key',
      code: `import os
import subprocess

AWS_ACCESS_KEY_ID = "AKIA1234567890EXAMPLE"

def backup_directory(target_path):
    # Command injection via shell=True
    cmd = f"tar -czvf backup.tar.gz {target_path}"
    subprocess.run(cmd, shell=True)`
    },
    {
      name: 'O(n²) Algorithmic Bottleneck',
      desc: 'Nested iteration over large datasets',
      code: `def find_duplicate_transactions(primary_batch, secondary_batch):
    duplicates = []
    # O(n^2) nested loop without hash lookup
    for item_a in primary_batch:
        for item_b in secondary_batch:
            if item_a['transaction_id'] == item_b['transaction_id']:
                duplicates.append((item_a, item_b))
    return duplicates`
    },
    {
      name: 'Clean & Parameterized Python',
      desc: 'Safe parameterized SQL & typed return',
      code: `import os
import sqlite3
from typing import Optional, Dict, Any

def get_user_profile(cursor: sqlite3.Cursor, user_id: int) -> Optional[Dict[str, Any]]:
    """Safely fetches user record using parameterized SQL placeholder."""
    query = "SELECT id, username, email FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    if not row:
        return None
    return {"id": row[0], "username": row[1], "email": row[2]}`
    }
  ];

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setTitle(file.name);
    const reader = new FileReader();
    reader.onload = (event) => {
      setSourceCode(event.target?.result as string);
    };
    reader.readAsText(file);
  };

  const handleReview = async () => {
    if (!sourceCode.trim()) {
      showToast('warning', 'Missing code', 'Please paste source code or select a preset.');
      return;
    }
    setLoading(true);

    const activeScopes = Object.entries(scopes).filter(([_, v]) => v).map(([k]) => k);

    try {
      setCurrentStage('Running AST analysis & taint tracking...');
      await new Promise(r => setTimeout(r, 200));
      setCurrentStage('Executing Ruff & Bandit security scanners...');
      
      const review = await reviewService.createReview({
        title,
        language,
        source_type: tab,
        file_path: title.includes('.') ? title : 'snippet.py',
        source_code: sourceCode,
        min_confidence: 0.60,
        apply_rag_rules: true,
        scopes: activeScopes
      });

      showToast('success', 'Review completed', `Overall Quality: ${review.overall_score.toFixed(1)}/100 (${review.letter_grade})`);
      navigate(`/reviews/${review.id}`);
    } catch (err: any) {
      showToast('error', 'Review failed', err.response?.data?.detail || 'Execution error');
    } finally {
      setLoading(false);
      setCurrentStage('');
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="border-b border-surface-border pb-3">
        <h1 className="text-2xl font-bold text-text-primary">New Code Review</h1>
        <p className="text-xs text-text-secondary mt-0.5">
          Execute multi-tier static analysis, AST taint tracking, and AI reasoning.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-surface-border space-x-6">
        <button
          onClick={() => setTab('paste')}
          className={`pb-2.5 text-sm font-semibold flex items-center space-x-2 border-b-2 transition-colors ${
            tab === 'paste' ? 'border-brand-500 text-brand-600' : 'border-transparent text-text-secondary hover:text-text-primary'
          }`}
        >
          <Code2 className="w-4 h-4" />
          <span>Paste Code</span>
        </button>

        <button
          onClick={() => setTab('upload')}
          className={`pb-2.5 text-sm font-semibold flex items-center space-x-2 border-b-2 transition-colors ${
            tab === 'upload' ? 'border-brand-500 text-brand-600' : 'border-transparent text-text-secondary hover:text-text-primary'
          }`}
        >
          <Upload className="w-4 h-4" />
          <span>Upload Source File</span>
        </button>
      </div>

      {/* Test Fixture Presets */}
      <div className="space-y-2">
        <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">Test Presets & Fixtures:</span>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
          {presets.map((p) => (
            <button
              key={p.name}
              type="button"
              onClick={() => {
                setTitle(p.name);
                setSourceCode(p.code);
              }}
              className="p-3 rounded-xl bg-white border border-surface-border hover:border-brand-400 hover:bg-surface-hover text-left transition-all shadow-subtle group"
            >
              <div className="text-xs font-bold text-text-primary group-hover:text-brand-600">{p.name}</div>
              <div className="text-[11px] text-text-muted line-clamp-1 mt-0.5">{p.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Config & Editor Card */}
      <div className="bg-white border border-surface-border rounded-xl p-5 space-y-4 shadow-subtle">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-text-primary">Review Title / Target File</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white transition-colors"
            />
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-text-primary">Language</label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full px-3 py-2 bg-surface-subtle border border-surface-border rounded-lg text-xs text-text-primary focus:outline-none focus:border-brand-500 focus:bg-white"
            >
              <option value="python">Python (AST + Ruff + Bandit + Radon + LLM)</option>
              <option value="typescript">TypeScript (AI Reasoning)</option>
              <option value="javascript">JavaScript (AI Reasoning)</option>
              <option value="java">Java (AI Reasoning)</option>
              <option value="go">Go (AI Reasoning)</option>
              <option value="cpp">C++ (AI Reasoning)</option>
            </select>
          </div>
        </div>

        {/* Scope Toggles */}
        <div className="space-y-1.5 pt-1">
          <label className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Analysis Scope:</label>
          <div className="flex flex-wrap gap-2">
            {[
              { key: 'security', label: 'Security & Taint', icon: Shield },
              { key: 'reliability', label: 'Reliability & Bugs', icon: Bug },
              { key: 'performance', label: 'Performance & Algo', icon: Gauge },
              { key: 'maintainability', label: 'Maintainability', icon: Cpu },
            ].map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                type="button"
                onClick={() => setScopes({ ...scopes, [key as keyof typeof scopes]: !scopes[key as keyof typeof scopes] })}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold border flex items-center space-x-1.5 transition-colors ${
                  scopes[key as keyof typeof scopes]
                    ? 'bg-brand-50 text-brand-700 border-brand-300 shadow-subtle'
                    : 'bg-surface-subtle text-text-muted border-surface-border hover:text-text-primary'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{label}</span>
              </button>
            ))}
          </div>
        </div>

        {tab === 'upload' && (
          <div className="border-2 border-dashed border-surface-border hover:border-brand-300 rounded-xl p-6 text-center space-y-2 bg-surface-subtle">
            <FileCode className="w-8 h-8 text-brand-500 mx-auto" />
            <div className="text-xs font-semibold text-text-primary">Select source file from your device</div>
            <input
              type="file"
              onChange={handleFileUpload}
              className="text-xs text-text-secondary file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-brand-500 file:text-white hover:file:bg-brand-600 cursor-pointer"
            />
          </div>
        )}

        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-text-primary">Source Code</label>
            <span className="text-[11px] text-text-muted font-mono">{sourceCode.split('\n').length} lines</span>
          </div>

          <div className="h-80 w-full">
            <MonacoCodeEditor
              code={sourceCode}
              language={language}
              onChange={(val) => setSourceCode(val)}
              readOnly={false}
            />
          </div>
        </div>

        {/* Progress State */}
        {loading && (
          <div className="p-3.5 bg-brand-50 border border-brand-200 rounded-xl flex items-center space-x-3">
            <div className="w-4 h-4 border-2 border-brand-500 border-t-transparent rounded-full animate-spin shrink-0" />
            <span className="text-xs font-semibold text-brand-800">{currentStage || 'Running multi-tier analysis...'}</span>
          </div>
        )}

        <div className="flex items-center justify-between pt-2 border-t border-surface-border">
          <span className="text-[11px] text-text-secondary">
            Deterministic Engine: AST Taint Tracker • Ruff • Bandit • RAG Guidelines • Safety Validator
          </span>

          <button
            onClick={handleReview}
            disabled={loading}
            className="px-6 py-2.5 rounded-lg text-xs font-semibold bg-brand-500 hover:bg-brand-600 text-white flex items-center space-x-2 shadow-sm disabled:opacity-50 transition-all"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>Run Code Review</span>
          </button>
        </div>
      </div>
    </div>
  );
};
