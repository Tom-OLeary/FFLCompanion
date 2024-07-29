import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { red } from '@mui/material/colors';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Radio from "@mui/material/Radio";
import '../../css/Header.css';


const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
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
    // season_year = models.IntegerField(default=0)
    // owner_one = models.ForeignKey(TeamOwner, on_delete=models.CASCADE, related_name="owner_one_trades", null=True)
    // owner_two = models.ForeignKey(TeamOwner, on_delete=models.CASCADE, related_name="owner_two_trades", null=True)
    // owner_one_received = models.ManyToManyField(Player, related_name="owner_one_received")
    // owner_two_received = models.ManyToManyField(Player, related_name="owner_two_received")
    // league = models.ForeignKey(LeagueSettings, on_delete=models.CASCADE, related_name="trades")
    // trade_date = models.DateField(null=True)

    return (
        <Card sx={{ maxWidth: 500 }}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
            {props.data.name}
          </Avatar>
        }
        action={
          <IconButton aria-label="settings">
            <MoreVertIcon />
          </IconButton>
        }
        title={props.data.winner}
        subheader={props.data.trade_date}
      />
      <CardMedia
        component="img"
        height="194"
        image="/static/images/cards/paella.jpg"
        alt="Paella dish"
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          {props.data.details[0].team_owner}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton aria-label="add to favorites">
          <FavoriteIcon />
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Typography paragraph>Best & Worst:</Typography>
          <Typography paragraph>
            AREA 2
          </Typography>
          <Typography paragraph>
            AREA 3
          </Typography>
          <Typography paragraph>
            AREA 4
          </Typography>
          <Typography>
            AREA 5
          </Typography>
        </CardContent>
              {/*          <FormControl component="fieldset">*/}
              {/*  <FormLabel component="legend">spacing</FormLabel>*/}
              {/*  <RadioGroup*/}
              {/*    name="spacing"*/}
              {/*    aria-label="spacing"*/}
              {/*    value={spacing.toString()}*/}
              {/*    onChange={handleChange}*/}
              {/*    row*/}
              {/*  >*/}
              {/*    {["worst", "best"].map((value) => (*/}
              {/*      <FormControlLabel*/}
              {/*        key={value}*/}
              {/*        value={value.toString()}*/}
              {/*        control={<Radio />}*/}
              {/*        label={value.toString()}*/}
              {/*      />*/}
              {/*    ))}*/}
              {/*  </RadioGroup>*/}
              {/*</FormControl>*/}
      </Collapse>
    </Card>
  )
}