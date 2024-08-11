import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Drawer from '@mui/material/Drawer';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { useNavigate } from 'react-router-dom';
import LinkIcon from '@mui/icons-material/Link';
import NotesIcon from '@mui/icons-material/Notes';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import FmdGoodIcon from '@mui/icons-material/FmdGood';
import {useState} from "react";
import Main from "../menuMain";

const drawerWidth = 275;

const DrawerHeader = styled('header')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function InfoDrawer(props) {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();

  const [data, setData] = useState([]);
  let endpoint = props.url + "leagues/?get_url=true"

  const fetchLeague = () => {
      fetch(endpoint, {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + window.localStorage.getItem('USER_STATE')
            }
        })
          .then(res => res.json())
          .then(json => {
              console.log(json);
              setData(json);
          })
          .catch(err => console.log(err));
  }

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleMenuSelection = (index) => {
      // todo fix fetchLeague not completing before button click
      fetchLeague();
      handleDrawerClose();
      switch (index) {
          case 0:
              let hostUrl = data["league_host_url"];
              if (!hostUrl) { hostUrl = 'https://www.espn.com/fantasy/' }
              window.open(hostUrl, '_blank').focus();
              break;
          // case 1:
          //     navigate(`requests`);
          //     break;
          case 2:
              navigate(`notes`);
            break;
          case 3:
              navigate(`links`);
            break;
          default:
              navigate(`home`);
      }
  };

  const panelItems = ['League Home', 'Requests', 'Notes', 'Links']

  return (
      <div style={{marginBottom: 1}}>
          <div className={"leader-panel"}>
              <Toolbar>
                  <IconButton
                      color="inherit"
                      aria-label="open drawer"
                      onClick={handleDrawerOpen}
                      edge="end"
                      sx={{mr: 2, ...(open && {display: 'none'}), color: "whitesmoke"}}
                  >
                      <MenuIcon/>
                  </IconButton>
                  <Typography variant="h6" noWrap component="div" color={"whitesmoke"}>
                      App Info
                  </Typography>
              </Toolbar>
          </div>
          <Drawer
              sx={{
                  width: drawerWidth,
                  flexShrink: 0,
                  '& .MuiDrawer-paper': {
                      width: drawerWidth,
                      boxSizing: 'border-box',
                      backgroundColor: 'gray',
                  },
              }}
              variant="persistent"
              anchor="right"
              open={open}
          >
              <DrawerHeader style={{marginTop: .5, marginBottom: .5, height: "5%"}}>
                  <IconButton onClick={handleDrawerClose}>
                      {theme.direction === 'rtl' ? <ChevronLeftIcon/> : <ChevronRightIcon/>}
                  </IconButton>
              </DrawerHeader>
              <Divider style={{ backgroundColor: 'black' }} />
              <List>
                  {panelItems.map((text, index) => (
                      <ListItem key={text} disablePadding style={{color: 'whitesmoke'}}>
                          <ListItemButton onClick={() => handleMenuSelection(index)}>
                              <ListItemIcon style={{ color: 'whitesmoke' }}>
                                  {
                                      index === 0 ? <FmdGoodIcon/>
                                          : index === 1 ? <QuestionAnswerIcon/>
                                              : index === 2 ? <NotesIcon/>
                                                  : <LinkIcon/>
                                  }
                              </ListItemIcon>
                              <ListItemText primary={text}/>
                          </ListItemButton>
                      </ListItem>
                  ))}
              </List>
            <Divider style={{ backgroundColor: 'black' }} />
          </Drawer>
          <Main open={open}>
          </Main>
      </div>
  );
}
