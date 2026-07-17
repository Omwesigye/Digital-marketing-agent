import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import { ColorModeProvider } from './themeContext';

import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import Profile from './pages/Profile';
import Dashboard from './pages/Dashboard';
import Competitor from './pages/Competitor';
import Sentiment from './pages/Sentiment';
import Retention from './pages/Retention';
import Insights from './pages/Insights';
import Drafts from './pages/Drafts';

function App() {
  return (
    <ColorModeProvider>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/competitor" element={<Competitor />} />
          <Route path="/sentiment" element={<Sentiment />} />
          <Route path="/retention" element={<Retention />} />
          <Route path="/insights" element={<Insights />} />
          <Route path="/drafts" element={<Drafts />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </ColorModeProvider>
  );
}

export default App;