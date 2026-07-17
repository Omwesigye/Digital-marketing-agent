import React, { useState } from 'react';
import { Card, CardContent, Typography, TextField, Button, Box, Link } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function SignInCard() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <Card sx={{ maxWidth: 400, width: '100%', mx: 'auto', mt: 8, p: 2 }}>
      <CardContent>
        <Typography variant="h4" component="h1" align="center" gutterBottom sx={{ fontWeight: 'bold' }}>
          Welcome Back
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 4 }}>
          Sign in to your Digital Marketing Assistant
        </Typography>

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Email Address"
            variant="outlined"
            margin="normal"
            required
            type="email"
          />
          <TextField
            fullWidth
            label="Password"
            variant="outlined"
            margin="normal"
            required
            type="password"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            disabled={loading}
            sx={{ mt: 3, mb: 2, py: 1.5 }}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
          
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="body2">
              Don't have an account?{' '}
              <Link 
                component="button" 
                variant="body2" 
                onClick={() => navigate('/signup')}
                sx={{ color: 'primary.main', textDecoration: 'none', fontWeight: 'bold' }}
              >
                Sign Up
              </Link>
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}
