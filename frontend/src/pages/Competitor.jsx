import React from 'react';
import { Typography } from '@mui/material';
import MainLayout from '../components/layout/MainLayout';
import CompetitorCard from '../components/dashboard/CompetitorCard';

export default function Competitor() {
  return (
    <MainLayout>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Competitor Intelligence
      </Typography>
      <CompetitorCard />
    </MainLayout>
  );
}
