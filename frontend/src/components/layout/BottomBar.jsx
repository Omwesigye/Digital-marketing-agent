import React from 'react';
import { Paper, BottomNavigation, BottomNavigationAction } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import PersonIcon from '@mui/icons-material/Person';
import { useNavigate, useLocation } from 'react-router-dom';

export default function BottomBar() {
  const navigate = useNavigate();
  const location = useLocation();

  const getValue = () => {
    if (location.pathname.startsWith('/dashboard')) return 0;
    if (location.pathname.startsWith('/insights')) return 1;
    if (location.pathname.startsWith('/retention')) return 2;
    if (location.pathname.startsWith('/profile')) return 3;
    return 0;
  };

  return (
    <Paper sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 1000, display: { sm: 'none' } }} elevation={3}>
      <BottomNavigation
        showLabels
        value={getValue()}
        onChange={(event, newValue) => {
          if (newValue === 0) navigate('/dashboard');
          if (newValue === 1) navigate('/insights');
          if (newValue === 2) navigate('/retention');
          if (newValue === 3) navigate('/profile');
        }}
        sx={{
          backgroundColor: 'background.paper',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)'
        }}
      >
        <BottomNavigationAction label="Home" icon={<HomeIcon />} />
        <BottomNavigationAction label="Insights" icon={<TrendingUpIcon />} />
        <BottomNavigationAction label="Retention" icon={<AutorenewIcon />} />
        <BottomNavigationAction label="Profile" icon={<PersonIcon />} />
      </BottomNavigation>
    </Paper>
  );
}
