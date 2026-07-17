import React, { createContext, useState, useMemo } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { getDesignTokens } from './theme';

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

export const ColorModeProvider = ({ children }) => {
  // Check local storage or system preference, default to light
  const [mode, setMode] = useState(() => {
    const saved = localStorage.getItem('themeMode');
    return saved || 'light';
  });

  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => {
          const newMode = prevMode === 'light' ? 'dark' : 'light';
          localStorage.setItem('themeMode', newMode);
          return newMode;
        });
      },
    }),
    [],
  );

  const theme = useMemo(() => createTheme(getDesignTokens(mode)), [mode]);

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};
