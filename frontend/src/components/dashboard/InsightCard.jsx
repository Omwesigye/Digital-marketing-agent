import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, Divider, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import InfoIcon from '@mui/icons-material/Info';
import { fetchInsights } from '../../services/api';

export default function InsightCard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInsights()
      .then(res => { setData(res); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  }, []);

  if (loading) return <Card><CardContent>Loading Insights...</CardContent></Card>;
  if (!data || data.length === 0) return <Card><CardContent>No Insights Available</CardContent></Card>;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
          <TrendingUpIcon color="primary" /> Market Insights
        </Typography>
        <Divider sx={{ mb: 2, borderColor: 'rgba(255,255,255,0.1)' }} />
        
        <List dense disablePadding>
          {data.map((insight) => (
            <ListItem key={insight.id} disablePadding sx={{ mb: 2, display: 'block' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                <Typography variant="subtitle2" color="secondary.main">{insight.metric}</Typography>
                <Typography variant="caption" sx={{ color: insight.change.includes('+') ? 'success.main' : 'error.main', fontWeight: 'bold' }}>
                  {insight.change}
                </Typography>
              </Box>
              <Typography variant="body2" sx={{ display: 'flex', alignItems: 'flex-start', gap: 0.5 }}>
                <InfoIcon fontSize="small" color="primary" sx={{ mt: 0.3 }} />
                {insight.recommendation}
              </Typography>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}
