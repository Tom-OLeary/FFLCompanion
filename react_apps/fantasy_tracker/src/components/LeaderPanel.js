import * as React from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
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

const drawerWidth = 475;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

const DrawerHeader = styled('header')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

export default function LeaderPanel() {
  const theme = useTheme();
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const handleMenuSelection = (index) => {
    //   switch (index) {
    //       case 0:
    //         navigate('/projections');
    //         break;
    //       default:
    //           navigate(`/`);
    //   }
    //   console.log("CLICKED", index)
  };

  // const panelItems = [
  //
  // ]

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
                      Rankings
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
                  },
              }}
              variant="persistent"
              anchor="right"
              open={open}
          >
              <DrawerHeader style={{marginTop: .5, marginBottom: .5, height: "5%"}}>
                  <IconButton onClick={handleDrawerClose}>
                      {theme.direction === 'ltr' ? <ChevronLeftIcon/> : <ChevronRightIcon/>}
                  </IconButton>
              </DrawerHeader>
              <Divider/>
              <List>
                  {['2024 Projections', 'Team Stats', 'Rosters (coming soon)'].map((text, index) => (
                      <ListItem key={text} disablePadding>
                          <ListItemButton onClick={() => handleMenuSelection(index)}>
                              <ListItemIcon>
                                  {
                                      index === 0 ? <QueryStatsIcon/>
                                          : index === 1 ? <SportsFootballIcon/>
                                              : <GroupsIcon/>
                                  }
                              </ListItemIcon>
                              <ListItemText primary={text}/>
                          </ListItemButton>
                      </ListItem>
                  ))}
              </List>
              <Divider/>
              {/*<List>*/}
              {/*  {['All mail', 'Trash', 'Spam'].map((text, index) => (*/}
              {/*    <ListItem key={text} disablePadding>*/}
              {/*      <ListItemButton>*/}
              {/*        <ListItemIcon>*/}
              {/*          {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}*/}
              {/*        </ListItemIcon>*/}
              {/*        <ListItemText primary={text} />*/}
              {/*      </ListItemButton>*/}
              {/*    </ListItem>*/}
              {/*  ))}*/}
              {/*</List>*/}
          </Drawer>
          <Main open={open}>
              {/*<DrawerHeader />*/}
          </Main>
      </div>
      // </Box>
  );
}
