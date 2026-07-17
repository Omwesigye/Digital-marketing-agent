import React, { useState } from 'react';
import { Box, Toolbar, useTheme, useMediaQuery } from '@mui/material';
import TopBar from './TopBar';
import SideMenu from './SideMenu';
import BottomBar from './BottomBar';

export default function MainLayout({ children }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <TopBar onMenuClick={handleDrawerToggle} isMobile={isMobile} />
      
      <SideMenu 
        open={mobileOpen} 
        onClose={handleDrawerToggle} 
        isMobile={isMobile} 
      />
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: { xs: 2, sm: 3, md: 4 },
          width: { sm: `calc(100% - 240px)` },
          mb: { xs: 7, sm: 0 }, // margin bottom for mobile bottom bar
          mt: 8, // margin top for top bar
        }}
      >
        {children}
      </Box>

      {isMobile && <BottomBar />}
    </Box>
  );
}
