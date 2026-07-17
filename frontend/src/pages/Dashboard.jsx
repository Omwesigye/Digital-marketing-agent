import React from 'react';
import { Typography, Grid, Box } from '@mui/material';
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
      
      <Grid container spacing={3} sx={{ mt: 1, alignItems: 'stretch' }}>
        <Grid item xs={12} sm={6} lg={4} sx={{ display: 'flex' }}>
          <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', '& > *': { flexGrow: 1, height: '100%' } }}>
            <PipelineTrigger />
          </Box>
        </Grid>
        
        <Grid item xs={12} sm={6} lg={4} sx={{ display: 'flex' }}>
          <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', '& > *': { flexGrow: 1, height: '100%' } }}>
            <SentimentCard />
          </Box>
        </Grid>

        <Grid item xs={12} sm={6} lg={4} sx={{ display: 'flex' }}>
          <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', '& > *': { flexGrow: 1, height: '100%' } }}>
            <InsightCard />
          </Box>
        </Grid>

        <Grid item xs={12} sm={6} lg={4} sx={{ display: 'flex' }}>
          <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', '& > *': { flexGrow: 1, height: '100%' } }}>
            <CompetitorCard />
          </Box>
        </Grid>
        
        <Grid item xs={12} sm={6} lg={4} sx={{ display: 'flex' }}>
          <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', '& > *': { flexGrow: 1, height: '100%' } }}>
            <RetentionCard />
          </Box>
        </Grid>
        
        <Grid item xs={12} sm={6} lg={4} sx={{ display: 'flex' }}>
          <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', '& > *': { flexGrow: 1, height: '100%' } }}>
            <DraftApproval />
          </Box>
        </Grid>
      </Grid>
    </MainLayout>
  );
}
