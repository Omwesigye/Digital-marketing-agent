import React from 'react';
import { Typography } from '@mui/material';
import MainLayout from '../components/layout/MainLayout';
import SentimentCard from '../components/dashboard/SentimentCard';

export default function Sentiment() {
  return (
    <MainLayout>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        Sentiment & Emotion
      </Typography>
      <SentimentCard />
    </MainLayout>
  );
}
