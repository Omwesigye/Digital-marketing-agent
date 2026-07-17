import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Box, Divider, List, ListItem, ListItemIcon, ListItemText, Grid, Button, IconButton } from '@mui/material';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import LightbulbCircleIcon from '@mui/icons-material/LightbulbCircle';
import EmailIcon from '@mui/icons-material/Email';
import SendIcon from '@mui/icons-material/Send';
import { fetchRetention } from '../../services/api';

export default function RetentionCard() {
  const [data, setData] = useState(null);
  const [drafts, setDrafts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRetention()
      .then(res => { setData(res); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });

    // Fetch email drafts specifically
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
    fetch(`${API_BASE_URL}/drafts`)
      .then(res => res.json())
      .then(data => {
        const emails = data.filter(d => d.platform?.toLowerCase() === 'email');
        setDrafts(emails);
      })
      .catch(err => console.error("Error fetching email drafts:", err));
  }, []);

  if (loading) return <Card><CardContent>Loading Retention Data...</CardContent></Card>;
  if (!data) return <Card><CardContent>No Retention Data Available</CardContent></Card>;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
          <AutorenewIcon color="primary" /> Retention Marketing
        </Typography>
        <Divider sx={{ mb: 2, borderColor: 'divider' }} />
        
        <Grid container spacing={2} sx={{ mb: 3 }}>
          {data.metrics?.map(m => (
            <Grid item xs={6} key={m.label}>
              <Box sx={{ p: 1.5, bgcolor: 'background.default', borderRadius: 2 }}>
                <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>{m.label}</Typography>
                <Typography variant="h6" sx={{ fontWeight: 'bold', display: 'inline-block', mr: 1 }}>{m.value}</Typography>
                <Typography variant="caption" color="primary.main">{m.trend}</Typography>
              </Box>
            </Grid>
          ))}
        </Grid>

        <Typography variant="subtitle2" sx={{ mb: 1, color: 'secondary.main' }}>Suggested Actions</Typography>
        <List dense disablePadding sx={{ mb: 3 }}>
          {data.suggested_actions?.map((action, i) => (
            <ListItem key={i} disablePadding sx={{ mb: 1 }}>
              <ListItemIcon sx={{ minWidth: 32 }}>
                <LightbulbCircleIcon fontSize="small" color="primary" />
              </ListItemIcon>
              <ListItemText primary={action} primaryTypographyProps={{ variant: 'body2' }} />
            </ListItem>
          ))}
        </List>

        {drafts.length > 0 && (
          <>
            <Typography variant="subtitle2" sx={{ mb: 1, color: 'primary.main', display: 'flex', alignItems: 'center', gap: 1 }}>
              <EmailIcon fontSize="small" /> Pending Email Drafts
            </Typography>
            <Divider sx={{ mb: 2, borderColor: 'divider' }} />
            <List dense disablePadding>
              {drafts.map((draft) => (
                <ListItem key={draft.id} sx={{ bgcolor: 'background.default', mb: 1, borderRadius: 1, border: '1px solid', borderColor: 'divider', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', mb: 1 }}>
                    <Typography variant="body2" fontWeight="bold">{draft.title}</Typography>
                    <Button variant="contained" size="small" endIcon={<SendIcon />} sx={{ minWidth: 120 }}>
                      Approve & Send
                    </Button>
                  </Box>
                  <Typography variant="caption" color="text.secondary" sx={{ whiteSpace: 'pre-wrap' }}>
                    {draft.body}
                  </Typography>
                </ListItem>
              ))}
            </List>
          </>
        )}
      </CardContent>
    </Card>
  );
}
