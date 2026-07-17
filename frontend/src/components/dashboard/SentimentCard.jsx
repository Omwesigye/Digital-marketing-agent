import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, Divider, LinearProgress, List, ListItem, ListItemText } from '@mui/material';
import MoodIcon from '@mui/icons-material/Mood';
import { fetchSentiment } from '../../services/api';

export default function SentimentCard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSentiment()
      .then(res => { setData(res); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  }, []);

  if (loading) return <Card><CardContent>Loading Sentiment Analysis...</CardContent></Card>;
  if (!data) return <Card><CardContent>No Sentiment Data Available</CardContent></Card>;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
          <MoodIcon color="primary" /> Sentiment & Emotion
        </Typography>
        <Divider sx={{ mb: 2, borderColor: 'rgba(255,255,255,0.1)' }} />
        
        <Box sx={{ textAlign: 'center', mb: 3 }}>
          <Typography variant="h3" color="primary.main" sx={{ fontWeight: 'bold' }}>
            {data.overall_score}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Overall Brand Sentiment Score
          </Typography>
        </Box>

        <Typography variant="subtitle2" sx={{ mb: 1, color: 'secondary.main' }}>Emotion Breakdown</Typography>
        <Box sx={{ mb: 3 }}>
          {data.emotions?.map(emo => (
            <Box key={emo.name} sx={{ mb: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                <Typography variant="body2">{emo.name}</Typography>
                <Typography variant="body2">{emo.value}%</Typography>
              </Box>
              <LinearProgress 
                variant="determinate" 
                value={emo.value} 
                sx={{ 
                  height: 8, 
                  borderRadius: 4,
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  '& .MuiLinearProgress-bar': { backgroundColor: emo.color }
                }} 
              />
            </Box>
          ))}
        </Box>

        <Typography variant="subtitle2" sx={{ mb: 1, color: 'secondary.main' }}>Recent Feedback</Typography>
        <List dense disablePadding>
          {data.recent_feedback?.map((fb, i) => (
            <ListItem key={i} disablePadding sx={{ mb: 1 }}>
              <ListItemText 
                primary={`"${fb.text}"`} 
                secondary={fb.emotion}
                primaryTypographyProps={{ variant: 'body2', fontStyle: 'italic' }}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}
