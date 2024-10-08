import * as React from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import '../../css/Header.css';
import '../../css/Notes.css';
import {ExpandMore} from "../layouts/layouts";


export default function NoteCard(props) {
  const [expanded, setExpanded] = React.useState(false);
  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  return (
      <div>
        <Card sx={{minWidth: 450, maxWidth: 350}} >
          <CardHeader/>
          <h1 className={"note-body"}>
            {props.title}
          </h1>
          <div className={"note-description"}>
            {props.description}
          </div>
          <CardContent>
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
                {props.items.map((item, index) => (
                    <Typography key={index} className="border-box">
                      <span className="note-expand-title">{item}</span>
                      <span className="bold-label">{props.descriptionLabel}:</span>
                      <span> {props.labels[index]}</span>
                      <span className="reason-description">
                        {
                          (props.reasonLabel === 'Link') ? <a href={props.urls[index]} target='_blank' rel="noreferrer">{props.reasons[index]}</a>
                              : <span> {props.reasonLabel}: {props.reasons[index]}</span>
                        }
                      </span>
                    </Typography>
                ))}
              </CardContent>
            </div>
          </Collapse>
        </Card>
      </div>
  )
}
