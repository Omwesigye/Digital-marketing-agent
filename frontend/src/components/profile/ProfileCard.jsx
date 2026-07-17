import React from 'react';
import { Card, CardContent, Typography, Avatar, Box, Button, TextField, Grid } from '@mui/material';

export default function ProfileCard() {
  return (
    <Card sx={{ maxWidth: 800, mx: 'auto', mt: 4, p: 2 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 4, gap: 3 }}>
          <Avatar sx={{ width: 100, height: 100, bgcolor: 'primary.main', fontSize: '2rem' }}>AD</Avatar>
          <Box>
            <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
              Admin User
            </Typography>
            <Typography variant="body1" color="text.secondary">
              admin@digitalmarketing.io
            </Typography>
            <Button variant="outlined" size="small" sx={{ mt: 1 }}>
              Change Avatar
            </Button>
          </Box>
        </Box>

        <Typography variant="h6" sx={{ mb: 2, fontWeight: '600' }}>
          Personal Information
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="First Name" defaultValue="Admin" variant="outlined" />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="Last Name" defaultValue="User" variant="outlined" />
          </Grid>
          <Grid item xs={12}>
            <TextField fullWidth label="Email Address" defaultValue="admin@digitalmarketing.io" variant="outlined" />
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary">
              Save Changes
            </Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
