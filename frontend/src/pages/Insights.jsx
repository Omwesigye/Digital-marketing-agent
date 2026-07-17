import React from 'react';
import { Typography } from '@mui/material';
import MainLayout from '../components/layout/MainLayout';
import InsightCard from '../components/dashboard/InsightCard';

export default function Insights() {
  return (
    <MainLayout>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Market Insights
      </Typography>
      <InsightCard />
    </MainLayout>
  );
}
