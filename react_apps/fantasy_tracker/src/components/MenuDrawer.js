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
import QueryStatsIcon from '@mui/icons-material/QueryStats';
import SportsFootballIcon from '@mui/icons-material/SportsFootball';
import GroupsIcon from '@mui/icons-material/Groups';
import { useNavigate } from 'react-router-dom';
import SwapVertIcon from '@mui/icons-material/SwapVert';
import HomeIcon from '@mui/icons-material/Home';
import LoginIcon from '@mui/icons-material/Login';
import Main from '../menuMain';

const drawerWidth = 275;

const DrawerHeader = styled('header')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function MenuDrawer() {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleMenuSelection = (element) => {
      handleDrawerClose()
      switch (element) {
          case 0:
            navigate('/projections');
            break;
          case 1:
            navigate('/stats');
            break;
          case 2:
            navigate('/trades');
            break;
          case 3:
              // TODO ROSTERS
            navigate('/home');
            break;
          case 'Load League':
            navigate('/');
            break;
          default:
              navigate(`/home`);
      }
  };

  const menuItems = [
      '2024 Projections',
      'Team Stats',
      'Trade Ratings',
      'Rosters (coming soon)',
      'Home',
  ]

  return (
      <div style={{ marginBottom: 1}}>
          <div className={"menu-drawer"}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }), color: "whitesmoke" }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" color={"whitesmoke"}>
            Menu
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
        anchor="left"
        open={open}
      >
        <DrawerHeader style={{ marginTop: .5, marginBottom: .5, height: "5%" }}>
          <IconButton onClick={handleDrawerClose} >
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </DrawerHeader>
        <Divider style={{ backgroundColor: 'black' }} />
        <List >
          {menuItems.map((text, index) => (
            <ListItem key={text} disablePadding style={{ color: 'whitesmoke' }}>
              <ListItemButton onClick={() => handleMenuSelection(index)}>
                <ListItemIcon style={{ color: 'whitesmoke' }}>
                    {
                        index === 0 ? <QueryStatsIcon />
                            : index === 1 ? <SportsFootballIcon />
                                : index === 2 ? <SwapVertIcon />
                                    : index === 3 ? <GroupsIcon />
                                        : index === 4 ? <HomeIcon />
                                            : <GroupsIcon />
                    }
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
        <Divider style={{ backgroundColor: 'black' }} />
        <List style={{ position: 'absolute', bottom: 0 }}>
          {['Load League'].map((text, index) => (
            <ListItem key={text} disablePadding style={{ color: 'whitesmoke' }}>
              <ListItemButton onClick={() => handleMenuSelection(text)}>
                <ListItemIcon style={{ color: 'whitesmoke' }}>
                  {
                      text === 'Load League' ? <LoginIcon />
                          : <LoginIcon />
                  }
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Drawer>
      <Main open={open} />
      </div>
  );
}
