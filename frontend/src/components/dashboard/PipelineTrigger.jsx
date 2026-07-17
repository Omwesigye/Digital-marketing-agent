import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Button, CircularProgress, Box, Divider, List, ListItem, ListItemText, Switch, FormControlLabel } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import { triggerPipeline, startContinuous, stopContinuous, getPipelineStatus } from '../../services/api';

export default function PipelineTrigger() {
  const [state, setState] = useState({
    status: 'idle',
    continuous: false,
    logs: []
  });

  const fetchStatus = async () => {
    try {
      const data = await getPipelineStatus();
      setState(prev => ({ ...prev, status: data.status, continuous: data.continuous }));
    } catch (e) {
      console.error("Failed to fetch pipeline status");
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const isRunning = state.status === 'processing' || state.status === 'sleeping';
  const isContinuous = state.continuous;

  const handleTrigger = async () => {
    setState(prev => ({ ...prev, logs: [...prev.logs, 'Initializing pipeline execution...'] }));
    try {
      await triggerPipeline();
      fetchStatus();
    } catch (error) {
      setState(prev => ({ ...prev, logs: [...prev.logs, `Error: ${error.message}`] }));
    }
  };

  const handleContinuousToggle = async (e) => {
    const checked = e.target.checked;
    try {
      if (checked) {
        setState(prev => ({ ...prev, logs: [...prev.logs, 'Activating continuous mode...'] }));
        await startContinuous();
      } else {
        setState(prev => ({ ...prev, logs: [...prev.logs, 'Deactivating continuous mode...'] }));
        await stopContinuous();
      }
      fetchStatus();
    } catch (error) {
      setState(prev => ({ ...prev, logs: [...prev.logs, `Error: ${error.message}`] }));
    }
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          Pipeline Control
        </Typography>
        <Divider sx={{ mb: 3, borderColor: 'rgba(255,255,255,0.1)' }} />
        
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 3 }}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={handleTrigger}
            disabled={isRunning || isContinuous}
            startIcon={(isRunning && !isContinuous) ? <CircularProgress size={20} color="inherit" /> : <PlayArrowIcon />}
            sx={{ width: '100%', py: 1.5, fontSize: '1rem' }}
          >
            {(isRunning && !isContinuous) ? 'Pipeline Running...' : 'Trigger Full Pipeline (Once)'}
          </Button>

          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', bgcolor: 'background.paper', p: 2, borderRadius: 1, border: '1px solid', borderColor: 'divider' }}>
            <Box>
              <Typography variant="subtitle1" fontWeight="bold">Continuous Mode</Typography>
              <Typography variant="body2" color="text.secondary">Run automatically in the background</Typography>
            </Box>
            <FormControlLabel
              control={<Switch checked={isContinuous} onChange={handleContinuousToggle} color="secondary" />}
              label={isContinuous ? "Active" : "Off"}
            />
          </Box>
        </Box>

        {(state.logs.length > 0 || isRunning) && (
          <Box sx={{ mt: 2, bgcolor: 'background.default', p: 2, borderRadius: 2, maxHeight: 200, overflow: 'auto' }}>
            <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 'bold', display: 'block', mb: 1 }}>
              STATUS: {state.status.toUpperCase()}
            </Typography>
            <List dense disablePadding>
              {state.logs.map((log, index) => (
                <ListItem key={index} disablePadding>
                  <ListItemText 
                    primary={`> ${log}`} 
                    primaryTypographyProps={{ variant: 'body2', fontFamily: 'monospace', color: 'success.main' }} 
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
