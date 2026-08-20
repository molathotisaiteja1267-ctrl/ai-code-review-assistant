import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ToastProvider } from './context/ToastContext';
import { AuthProvider } from './context/AuthContext';
import { Layout } from './components/layout/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { NewReviewPage } from './pages/NewReviewPage';
import { GitHubReviewPage } from './pages/GitHubReviewPage';
import { ReviewDetailPage } from './pages/ReviewDetailPage';
import { ReviewHistoryPage } from './pages/ReviewHistoryPage';
import { ProjectRulesPage } from './pages/ProjectRulesPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { SettingsPage } from './pages/SettingsPage';
import { LoginPage } from './pages/LoginPage';

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <ToastProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<Layout />}>
              <Route index element={<DashboardPage />} />
              <Route path="reviews/new" element={<NewReviewPage />} />
              <Route path="reviews/:id" element={<ReviewDetailPage />} />
              <Route path="github" element={<GitHubReviewPage />} />
              <Route path="history" element={<ReviewHistoryPage />} />
              <Route path="rules" element={<ProjectRulesPage />} />
              <Route path="evaluation" element={<EvaluationPage />} />
              <Route path="settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </AuthProvider>
  );
};

export default App;
