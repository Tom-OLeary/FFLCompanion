import * as React from 'react';
import '../../css/LeaderBoard.scss';
import pseudoSwitch from "../../leaderCallback";

export default function Rank(props) {
    const setPct = (index) => { return pseudoSwitch(index); }
    let [barColor, widthValue] = setPct(props.index);

    return (
        <div>
            <dt>
                <span className="right-side">
                    <div>
                    <span className="leader-name">{props.team_name}</span>
                    <span style={{fontWeight: "light", display: "inline", marginLeft: 4}}>({props.name})</span>
                    </div>

                    <div
                        className="leaderboard-value">
                        {props.total}
                        <div style={{display: "inline", fontWeight: "lighter"}}> ({props.year})</div>
                    </div>
                </span>
                <article className="progress">

                    <section className="progress-bar"
                             style={{width: widthValue, backgroundColor: barColor}}></section>
                </article>
            </dt>

        </div>
    )
}
