import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, TextField, Button, Box, Divider, Alert, CircularProgress, List, ListItem, ListItemText, Chip } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { fetchDrafts } from '../../services/api';

export default function DraftApproval() {
  const [drafts, setDrafts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDrafts()
      .then(res => { 
        // Filter out email drafts since they belong in the Retention tab
        const socialDrafts = res.filter(d => d.platform?.toLowerCase() !== 'email');
        setDrafts(socialDrafts); 
        setLoading(false); 
      })
      .catch(err => { console.error(err); setLoading(false); });
  }, []);

  if (loading) return <Card><CardContent>Loading Drafts...</CardContent></Card>;
  if (drafts.length === 0) return <Card><CardContent>No social media drafts available.</CardContent></Card>;

  const handleApprove = (id) => {
    // In a real app, this would call an API to mark it as approved
    setDrafts(prev => prev.filter(d => d.id !== id));
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          Social Media Drafts Awaiting Approval
        </Typography>
        <Divider sx={{ mb: 3, borderColor: 'divider' }} />
        
        <List sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {drafts.map((draft) => (
            <Card key={draft.id} variant="outlined" sx={{ bgcolor: 'background.default' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip label={draft.platform.toUpperCase()} color="primary" size="small" />
                    <Typography variant="subtitle1" fontWeight="bold">
                      {draft.title}
                    </Typography>
                  </Box>
                  <Button 
                    variant="contained" 
                    color="primary" 
                    size="small"
                    startIcon={<SendIcon />}
                    onClick={() => handleApprove(draft.id)}
                  >
                    Approve
                  </Button>
                </Box>
                
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  variant="outlined"
                  defaultValue={draft.body || draft.content} // Handle both old and new schema
                  sx={{ mb: 1 }}
                />
              </CardContent>
            </Card>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}
