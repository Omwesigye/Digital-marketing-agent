import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, Divider, List, ListItem, ListItemIcon, ListItemText, Chip } from '@mui/material';
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import { fetchCompetitors } from '../../services/api';

export default function CompetitorCard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCompetitors()
      .then(res => { setData(res); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  }, []);

  if (loading) return <Card><CardContent>Loading Competitor Intel...</CardContent></Card>;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
          <QueryStatsIcon color="primary" /> Competitor Intelligence
        </Typography>
        <Divider sx={{ mb: 2, borderColor: 'rgba(255,255,255,0.1)' }} />
        
        <List dense>
          {data.map((comp) => (
            <ListItem key={comp.id} disablePadding sx={{ mb: 2, display: 'block' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                <Typography variant="subtitle1" color="secondary.main" sx={{ fontWeight: 'bold' }}>
                  {comp.name}
                </Typography>
                <Chip 
                  label={`${comp.threat_level} Threat`} 
                  color={comp.threat_level === 'High' ? 'error' : 'warning'} 
                  size="small" 
                />
              </Box>
              <Typography variant="body2" sx={{ mb: 0.5 }}>
                <strong>Move:</strong> {comp.move}
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'flex-start', gap: 0.5 }}>
                <PriorityHighIcon fontSize="small" color="primary" />
                {comp.action}
              </Typography>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}
