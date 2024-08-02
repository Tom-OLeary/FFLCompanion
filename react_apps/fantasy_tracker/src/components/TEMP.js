// import * as React from 'react';
// import { styled, useTheme } from '@mui/material/styles';
// import Drawer from '@mui/material/Drawer';
// import Toolbar from '@mui/material/Toolbar';
// import Typography from '@mui/material/Typography';
// import IconButton from '@mui/material/IconButton';
// import MenuIcon from '@mui/icons-material/Menu';
// import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
// import ChevronRightIcon from '@mui/icons-material/ChevronRight';
// import { useNavigate } from 'react-router-dom';
// import '../css/LeaderBoard.scss';
//
// const drawerWidth = 775;
//
// const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
//   ({ theme, open }) => ({
//     flexGrow: 1,
//     padding: theme.spacing(3),
//     transition: theme.transitions.create('margin', {
//       easing: theme.transitions.easing.sharp,
//       duration: theme.transitions.duration.leavingScreen,
//     }),
//     marginLeft: `-${drawerWidth}px`,
//     ...(open && {
//       transition: theme.transitions.create('margin', {
//         easing: theme.transitions.easing.easeOut,
//         duration: theme.transitions.duration.enteringScreen,
//       }),
//       marginLeft: 0,
//     }),
//   }),
// );
//
// const DrawerHeader = styled('header')(({ theme }) => ({
//   display: 'flex',
//   alignItems: 'center',
//   padding: theme.spacing(0, 1),
//   // necessary for content to be below app bar
//   ...theme.mixins.toolbar,
//   justifyContent: 'flex-end',
// }));
//
// export default function TEMP() {
//   const theme = useTheme();
//   const [open, setOpen] = React.useState(false);
//   const navigate = useNavigate();
//
//   const handleDrawerOpen = () => {
//     setOpen(true);
//   };
//
//   const handleDrawerClose = () => {
//     setOpen(false);
//   };
//
//   const handleMenuSelection = (index) => {
//     //   switch (index) {
//     //       case 0:
//     //         navigate('/projections');
//     //         break;
//     //       default:
//     //           navigate(`/`);
//     //   }
//     //   console.log("CLICKED", index)
//   };
//
//   // const panelItems = [
//   //
//   // ]
//
//   return (
//       <div style={{marginBottom: 1}}>
//           <div className={"leader-panel"}>
//               <Toolbar>
//                   <IconButton
//                       color="inherit"
//                       aria-label="open drawer"
//                       onClick={handleDrawerOpen}
//                       edge="end"
//                       sx={{mr: 2, ...(open && {display: 'none'}), color: "whitesmoke"}}
//                   >
//                       <MenuIcon/>
//                   </IconButton>
//                   <Typography variant="h6" noWrap component="div" color={"whitesmoke"}>
//                       Rankings
//                   </Typography>
//               </Toolbar>
//           </div>
//           <Drawer
//               sx={{
//                   width: drawerWidth,
//                   flexShrink: 0,
//                   '& .MuiDrawer-paper': {
//                       width: drawerWidth,
//                       boxSizing: 'border-box',
//                   },
//               }}
//               variant="persistent"
//               anchor="right"
//               open={open}
//           >
//               <div style={{backgroundColor: "#e45b6c"}}>
//
//                   <DrawerHeader style={{marginTop: .5, marginBottom: .5, height: "5%"}}>
//                       <IconButton onClick={handleDrawerClose}>
//                           {theme.direction === 'ltr' ? <ChevronLeftIcon/> : <ChevronRightIcon/>}
//                       </IconButton>
//                   </DrawerHeader>
//                   <div className="card" >
//                       <section className="card-info card-section">
//                           <i className="ion-navicon menu"></i>
//                           <i className="ion-ios-search search"></i>
//
//                           <div className="avatar row">
//                           </div>
//
//                           <section className="user row">
//                               <h1 className="user-header">
//                                   Bryan Smith
//                                   <h2 className="sub header">
//                                       400 hours
//                                   </h2>
//                               </h1>
//                           </section>
//
//                           <section className="statistics">
//                               <article className="statistic">
//                                   <h4 className="statistic-title">
//                                       Rank
//                                   </h4>
//                                   <h3 className="statistic-value">
//                                       360
//                                   </h3>
//                               </article>
//
//                               <article className="statistic">
//                                   <h4 className="statistic-title">
//                                       Score
//                                   </h4>
//                                   <h3 className="statistic-value">
//                                       1,034
//                                   </h3>
//                               </article>
//                           </section>
//
//                           <div className="dial">
//                               <h2 className="dial-title">
//                                   35
//                               </h2>
//                               <h3 className="dial-value">
//                                   Level
//                               </h3>
//                           </div>
//                       </section>
//                       <section className="card-details card-section">
//
//                           <nav className="menu">
//                               <article className="menu-item menu-item-active">
//                                   Global
//                               </article>
//                               <article className="menu-item">
//                                   Friends
//                               </article>
//                           </nav>
//
//                           <dl className="leaderboard">
//                               <dt>
//                                   <article className="progress">
//                                       <section className="progress-bar" style={{width: "85%"}}></section>
//                                   </article>
//                               </dt>
//                               <dd>
//                                   <div className="leaderboard-name">Bryan Smith</div>
//                                   <div className="leaderboard-value">20.123</div>
//                               </dd>
//                               <dt>
//                                   <article className="progress">
//                                       <section className="progress-bar" style={{width: "65%"}}></section>
//                                   </article>
//                               </dt>
//                               <dd>
//                                   <div className="leaderboard-name">Kevin Johnson</div>
//                                   <div className="leaderboard-value">16.354</div>
//                               </dd>
//                               <dt>
//                                   <article className="progress">
//                                       <section className="progress-bar" style={{width: "60%"}}></section>
//                                   </article>
//                               </dt>
//                               <dd>
//                                   <div className="leaderboard-name">Glen Howie</div>
//                                   <div className="leaderboard-value">15.873</div>
//                               </dd>
//                               <dt>
//                                   <article className="progress">
//                                       <section className="progress-bar" style={{width: "55%"}}></section>
//                                   </article>
//                               </dt>
//                               <dd>
//                                   <div className="leaderboard-name">Mark Desa</div>
//                                   <div className="leaderboard-value">12.230</div>
//                               </dd>
//                               <dt>
//                                   <article className="progress">
//                                       <section className="progress-bar" style={{width: "35%"}}></section>
//                                   </article>
//                               </dt>
//                               <dd>
//                                   <div className="leaderboard-name">Martin Geiger</div>
//                                   <div className="leaderboard-value">10.235</div>
//                               </dd>
//                           </dl>
//                       </section>
//                   </div>
//             </div>
//           </Drawer>
//     <Main open={open}>
//           </Main>
//       </div>
//   );
// }
