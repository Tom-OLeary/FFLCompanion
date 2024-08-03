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
                <div className="leaderboard-name">{props.name}</div>
                <div className="leaderboard-value">{props.total}</div>
            </dd>
        </div>
    )
}
