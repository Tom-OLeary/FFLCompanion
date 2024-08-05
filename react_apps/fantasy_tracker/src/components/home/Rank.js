import * as React from 'react';
import '../../css/LeaderBoard.scss';
import pseudoSwitch from "../../leaderCallback";

export default function Rank(props) {
    const setPct = (index) => { return pseudoSwitch(index); }
    let [barColor, widthValue] = setPct(props.index);

    return (
        <div>
            <dt>
                <article className="progress">
                    <section className="progress-bar"
                             style={{width: widthValue, backgroundColor: barColor}}></section>
                </article>
            </dt>
            <dd>
                <div className="leaderboard-name"><div style={{fontWeight: 'bold'}}>{props.team_name}</div> ({props.name})</div>
                <div
                    className="leaderboard-value"><div style={{fontWeight: 'bold'}}>{props.total}</div> <div style={{fontWeight: 'lighter'}}>({props.year})</div>
                </div>
            </dd>
        </div>
    )
}
