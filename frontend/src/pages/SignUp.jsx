import React from 'react';
import SignUpCard from '../components/auth/SignUpCard';
import { Box } from '@mui/material';

export default function SignUp() {
  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'background.default' }}>
      <SignUpCard />
    </Box>
  );
}
