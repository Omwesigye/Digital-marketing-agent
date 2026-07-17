import React from 'react';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Toolbar, Box } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import MoodIcon from '@mui/icons-material/Mood';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import CampaignIcon from '@mui/icons-material/Campaign';
import PersonIcon from '@mui/icons-material/Person';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 240;

const menuItems = [
  { text: 'Dashboard', icon: <HomeIcon />, path: '/dashboard' },
  { text: 'Insights', icon: <TrendingUpIcon />, path: '/insights' },
  { text: 'Competitor Intel', icon: <QueryStatsIcon />, path: '/competitor' },
  { text: 'Sentiment', icon: <MoodIcon />, path: '/sentiment' },
  { text: 'Retention', icon: <AutorenewIcon />, path: '/retention' },
  { text: 'Drafts', icon: <CampaignIcon />, path: '/drafts' },
  { text: 'Profile', icon: <PersonIcon />, path: '/profile' },
];

export default function SideMenu({ open, onClose, isMobile }) {
  const navigate = useNavigate();
  const location = useLocation();

  const drawerContent = (
    <Box sx={{ overflow: 'auto' }}>
      <Toolbar /> {/* Spacer for TopBar */}
      <List sx={{ mt: 2 }}>
        {menuItems.map((item) => {
          const isSelected = location.pathname.startsWith(item.path);
          return (
            <ListItem key={item.text} disablePadding>
              <ListItemButton 
                selected={isSelected}
                onClick={() => {
                  navigate(item.path);
                  if (isMobile) onClose();
                }}
                sx={{
                  mx: 1,
                  borderRadius: 2,
                  mb: 1,
                  '&.Mui-selected': {
                    backgroundColor: 'rgba(255, 152, 0, 0.15)',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 152, 0, 0.25)',
                    }
                  }
                }}
              >
                <ListItemIcon sx={{ color: isSelected ? 'primary.main' : 'inherit' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} sx={{ color: isSelected ? 'primary.main' : 'inherit' }} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </Box>
  );

  return (
    <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
      {isMobile ? (
        <Drawer
          variant="temporary"
          open={open}
          onClose={onClose}
          ModalProps={{ keepMounted: true }} // Better open performance on mobile
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, backgroundColor: 'background.paper' },
          }}
        >
          {drawerContent}
        </Drawer>
      ) : (
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, borderRight: '1px solid rgba(255, 255, 255, 0.1)', backgroundColor: 'background.default' },
          }}
          open
        >
          {drawerContent}
        </Drawer>
      )}
    </Box>
  );
}
