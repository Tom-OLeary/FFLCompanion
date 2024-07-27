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

export default function TeamCard(props) {
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };
  // const [spacing, setSpacing] = React.useState(2);
  // const handleChange = (event) => {
  //   setSpacing(Number(event.target.value));
  // };

  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe">
            DL
          </Avatar>
        }
        action={
          <IconButton aria-label="settings">
            <MoreVertIcon />
          </IconButton>
        }
        title={props.team_name}
        subheader="September 14, 2016"
      />
      <CardMedia
        component="img"
        height="194"
        image="/static/images/cards/paella.jpg"
        alt="Paella dish"
      />
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          AREA 1
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
  );
}