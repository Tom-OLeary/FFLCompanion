import {styled} from "@mui/material/styles";
import Paper from "@mui/material/Paper";

const Item = styled(Paper)(({theme}) => ({
        backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        // textAlign: 'left',
        color: theme.palette.text.secondary,
        // marginLeft: 250,
        justifyContent: 'space-between',
        display: 'flex',
    }));

export default Item;