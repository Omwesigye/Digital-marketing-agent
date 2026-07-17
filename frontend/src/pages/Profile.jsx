import React from 'react';
import ProfileCard from '../components/profile/ProfileCard';
import MainLayout from '../components/layout/MainLayout';
import { Typography } from '@mui/material';

export default function Profile() {
  return (
    <MainLayout>
      <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
        My Profile
      </Typography>
      <ProfileCard />
    </MainLayout>
  );
}
