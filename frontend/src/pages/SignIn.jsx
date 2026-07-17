import React from 'react';
import SignInCard from '../components/auth/SignInCard';
import { Box } from '@mui/material';

export default function SignIn() {
  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'background.default' }}>
      <SignInCard />
    </Box>
  );
}
