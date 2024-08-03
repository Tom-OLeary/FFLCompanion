import * as React from 'react';
import '../../css/LeaderBoard.scss';

export default function Rank(props) {
    let callbacks = {};

    function add(_case, fn) {
        callbacks[_case] = callbacks[_case] || [];
        callbacks[_case].push(fn);
    }

    function pseudoSwitch(value) {
        if (callbacks[value]) {
            callbacks[value].forEach(function (fn) {
                fn();
            });
        }
    }
    let barColor;
    let widthValue;
    let ownerCount = [...Array(23).keys()];
    let iterRate = Math.floor(100 / ownerCount.length);

    ownerCount.map((item, i) => {
        add(item, function() {
            let i1;
            if (item <= ownerCount.length / 2){
                i1 = (item+1) * 18;
                barColor = "#" + (i1).toString(16)+(186).toString(16)+(i1).toString(16);
                widthValue = (100 - (iterRate*item)).toString() + "%";
            } else {
                i1 = (item - (item-1)) * 30;
                barColor = "#" + (230).toString(16)+(i1).toString(16)+(i1).toString(16);
                widthValue = (iterRate*item).toString() + "%";
            }
        });
    })
    const getPct = (index) => {
        return pseudoSwitch(index);
    }

    getPct(props.index)

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
