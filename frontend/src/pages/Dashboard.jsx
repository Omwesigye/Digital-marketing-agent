import React from 'react';
import { Typography, Grid } from '@mui/material';
import MainLayout from '../components/layout/MainLayout';
import InsightCard from '../components/dashboard/InsightCard';
import DraftApproval from '../components/dashboard/DraftApproval';
import PipelineTrigger from '../components/dashboard/PipelineTrigger';
import CompetitorCard from '../components/dashboard/CompetitorCard';
import SentimentCard from '../components/dashboard/SentimentCard';
import RetentionCard from '../components/dashboard/RetentionCard';

export default function Dashboard() {
  return (
    <MainLayout>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Dashboard Overview
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 1 }}>
        <Grid item xs={12} md={4}>
          <PipelineTrigger />
        </Grid>
        
        <Grid item xs={12} md={8}>
          <SentimentCard />
        </Grid>

        <Grid item xs={12} md={6}>
          <InsightCard />
        </Grid>

        <Grid item xs={12} md={6}>
          <CompetitorCard />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <RetentionCard />
        </Grid>
        
        <Grid item xs={12} md={6}>
          <DraftApproval />
        </Grid>
      </Grid>
    </MainLayout>
  );
}
