import React from 'react';
import { Typography } from '@mui/material';
import MainLayout from '../components/layout/MainLayout';
import RetentionCard from '../components/dashboard/RetentionCard';

export default function Retention() {
  return (
    <MainLayout>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Retention Marketing
      </Typography>
      <RetentionCard />
    </MainLayout>
  );
}
