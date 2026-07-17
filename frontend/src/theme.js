import { createTheme } from '@mui/material/styles';

export const getDesignTokens = (mode) => ({
  palette: {
    mode,
    ...(mode === 'dark'
      ? {
          primary: { main: '#ff9800', light: '#ffb74d', dark: '#f57c00', contrastText: '#ffffff' },
          secondary: { main: '#ffeb3b', light: '#fff59d', dark: '#fbc02d', contrastText: '#000000' },
          background: { default: '#121212', paper: '#1e1e1e' },
          text: { primary: '#ffffff', secondary: '#b3b3b3' },
        }
      : {
          primary: { main: '#f57c00', light: '#ff9800', dark: '#e65100', contrastText: '#ffffff' },
          secondary: { main: '#fbc02d', light: '#ffeb3b', dark: '#f57f17', contrastText: '#000000' },
          background: { default: '#f5f5f5', paper: '#ffffff' },
          text: { primary: '#333333', secondary: '#666666' },
        }),
    error: { main: '#f44336' },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: { fontFamily: '"Outfit", "Inter", sans-serif', fontWeight: 800 },
    h2: { fontFamily: '"Outfit", "Inter", sans-serif', fontWeight: 700 },
    h3: { fontFamily: '"Outfit", "Inter", sans-serif', fontWeight: 700 },
    h4: { fontFamily: '"Outfit", "Inter", sans-serif', fontWeight: 600 },
    h5: { fontFamily: '"Outfit", "Inter", sans-serif', fontWeight: 600 },
    h6: { fontFamily: '"Outfit", "Inter", sans-serif', fontWeight: 500 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 8, padding: '8px 24px' },
        containedPrimary: {
          background: mode === 'dark' ? 'linear-gradient(45deg, #FF8E53 30%, #FF5722 90%)' : 'linear-gradient(45deg, #FF5722 30%, #FF8E53 90%)',
          boxShadow: '0 3px 5px 2px rgba(255, 105, 135, .3)',
          transition: 'transform 0.2s',
          '&:hover': { transform: 'scale(1.02)' },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: mode === 'dark' ? 'rgba(30, 30, 30, 0.6)' : 'rgba(255, 255, 255, 0.8)',
          backdropFilter: 'blur(10px)',
          border: mode === 'dark' ? '1px solid rgba(255, 255, 255, 0.1)' : '1px solid rgba(0, 0, 0, 0.1)',
          transition: 'transform 0.2s, box-shadow 0.2s',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: mode === 'dark' ? '0 8px 24px rgba(0,0,0,0.4)' : '0 8px 24px rgba(0,0,0,0.1)',
          },
        },
      },
    },
  },
});
