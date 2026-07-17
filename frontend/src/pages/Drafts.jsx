import React from 'react';
import { Typography } from '@mui/material';
import MainLayout from '../components/layout/MainLayout';
import DraftApproval from '../components/dashboard/DraftApproval';

export default function Drafts() {
  return (
    <MainLayout>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Campaign Drafts
      </Typography>
      <DraftApproval />
    </MainLayout>
  );
}
