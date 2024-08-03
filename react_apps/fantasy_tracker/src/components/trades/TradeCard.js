import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { red } from '@mui/material/colors';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import SwapVerticalCircleIcon from '@mui/icons-material/SwapVerticalCircle';
import SyncAltIcon from '@mui/icons-material/SyncAlt';
import '../../css/Header.css';
import '../../css/TradeCard.css';

const ExpandMore = styled((props) => {
  const {expand, ...other} = props;
  return <IconButton {...other} />;
})(({theme, expand}) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));


export default function TradeCard(props) {

  const [expanded, setExpanded] = React.useState(false);
  const handleExpandClick = () => {
    setExpanded(!expanded);
  };
  const teamOne = props.data.details[0]
  const teamTwo = props.data.details[1]

  return (
      <div>
        <Card sx={{maxWidth: 500}}>
          <CardHeader
              avatar={
                <Avatar sx={{bgcolor: red[500]}} aria-label="recipe">
                  1
                </Avatar>
              }
              action={
                <IconButton aria-label="settings">
                  <MoreVertIcon/>
                </IconButton>
              }
              title={teamOne.team_name}
              subheader={teamOne.team_owner}
          />
          <h1 className={"card-body"}>
            {teamOne.total_points}
          </h1>
          <div className={"card-players"}>
            {teamOne.players_received.map((player, index) => (<div>{player}</div>))}
          </div>
          <CardContent>
            <div className={"div-icon"}>
              {
                (props.data.winner === teamOne.team_owner) ? <SwapVerticalCircleIcon className={"trade-winner"}/>
                    : (props.data.winner === teamTwo.team_owner)
                        ? <SwapVerticalCircleIcon className={"trade-loser"}/>
                          : <SwapVerticalCircleIcon className={"trade-draw"}/>
              }
            </div>
          </CardContent>
          <CardActions disableSpacing>
            <ExpandMore
                expand={expanded}
                onClick={handleExpandClick}
                aria-expanded={expanded}
                aria-label="show more"
            >
              <ExpandMoreIcon/>
            </ExpandMore>
          </CardActions>
          <Collapse in={expanded} timeout="auto" unmountOnExit>
            <div className={"card-summary"}>
              <CardContent>
                <Typography>
                  Pass Yards: {teamOne.pass_yds}
                </Typography>
                <Typography>
                  Pass TD: {teamOne.pass_td}
                </Typography>
                <Typography paragraph>
                  Interceptions: {teamOne.interceptions}
                </Typography>
                <Typography>
                  Rec Yards: {teamOne.receiving_yards}
                </Typography>
                <Typography>
                  Rec TD: {teamOne.receiving_td}
                </Typography>
                <Typography paragraph>
                  Receptions: {teamOne.receptions}
                </Typography>
                <Typography>
                  Rush Yards: {teamOne.rush_yds}
                </Typography>
                <Typography>
                  Rush TD: {teamOne.rush_td}
                </Typography>
              </CardContent>
            </div>
          </Collapse>
        </Card>
        <h1 className={"date-title"}>{props.data.trade_date}</h1>
        {/*<h1 className={"date-title"}>{props.data.winner}</h1>*/}
        <div className={"div-icon"}>
          <h1 className={"winner-title"}> {
            (props.data.winner) ? <div className={"winner-result"}>{props.data.winner} </div>
                : <div className={"winner-result"}>DRAW</div>}
          </h1>
          <SyncAltIcon style={{fontSize: 75, color: red[500]}}/>
        </div>
        <Card>
          <CardHeader
              avatar={
                <Avatar sx={{bgcolor: red[500]}} aria-label="recipe">
                  2
                </Avatar>
              }
              action={
                <IconButton aria-label="settings">
                  <MoreVertIcon/>
                </IconButton>
              }
              title={teamTwo.team_name}
              subheader={teamTwo.team_owner}
          />
          <h1 className={"card-body"}>
            {teamTwo.total_points}
          </h1>
          <div className={"card-players"}>
            {teamTwo.players_received.map((player, index) => (<div>{player}</div>))}
          </div>
          <CardContent>
            <div className={"div-icon"}>
              {
                (props.data.winner === teamTwo.team_owner) ? <SwapVerticalCircleIcon className={"trade-winner"}/>
                    : (props.data.winner === teamOne.team_owner)
                        ? <SwapVerticalCircleIcon className={"trade-loser"}/>
                          : <SwapVerticalCircleIcon className={"trade-draw"}/>
              }
            </div>
          </CardContent>
          <CardActions disableSpacing>
            <ExpandMore
                expand={expanded}
                onClick={handleExpandClick}
                aria-expanded={expanded}
                aria-label="show more"
            >
              <ExpandMoreIcon/>
            </ExpandMore>
          </CardActions>
          <Collapse in={expanded} timeout="auto" unmountOnExit>
            <div className={"card-summary"}>
              <CardContent>
                <Typography>
                  Pass Yards: {teamTwo.pass_yds}
                </Typography>
                <Typography>
                  Pass TD: {teamTwo.pass_td}
                </Typography>
                <Typography paragraph>
                  Interceptions: {teamTwo.interceptions}
                </Typography>
                <Typography>
                  Rec Yards: {teamTwo.receiving_yards}
                </Typography>
                <Typography>
                  Rec TD: {teamTwo.receiving_td}
                </Typography>
                <Typography paragraph>
                  Receptions: {teamTwo.receptions}
                </Typography>
                <Typography>
                  Rush Yards: {teamTwo.rush_yds}
                </Typography>
                <Typography>
                  Rush TD: {teamTwo.rush_td}
                </Typography>
              </CardContent>
            </div>
          </Collapse>
        </Card>
      </div>
  )
}
