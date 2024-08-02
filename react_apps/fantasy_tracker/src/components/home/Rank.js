import * as React from 'react';
import '../../css/LeaderBoard.scss';

export default function Rank(props) {
    let barColor = null;
    const getPct = (index) => {
        switch (index) {
            case 0:
                barColor = '#14a103'
                return "100%";
            case 1:
                barColor = '#42cf30'
                return "90%";
            case 2:
                barColor = '#88d87e'
                return "80%";
            case 3:
                barColor = '#a3dc9c'
                return "70%";
            case 4:
                barColor = '#d0e8cd'
                return "60%";
            case 5:
                barColor = 'rgba(200,204,200,0.96)'
                return "50%";
            case 6:
                barColor = '#f1bbbb'
                return "50%";
            case 7:
                barColor = '#dd6f6f'
                return "50%";
            case 8:
                barColor = '#d85c5c'
                return "60%";
            case 9:
                barColor = '#da4242'
                return "70%";
            case 10:
                barColor = '#dc2222'
                return "80%";
            case 11:
                barColor = '#c80303'
                return "90%";
            default:
                barColor = '#c80303'
                return "100%"
        }
    }
    let widthValue = getPct(props.index);

    return (
        <div>
            <dt>
                <article className="progress">
                    <section className="progress-bar"
                             style={{width: widthValue, backgroundColor: barColor }}></section>
                </article>
            </dt>
            <dd>
                <div className="leaderboard-name">{props.name}</div>
                <div className="leaderboard-value">{props.total}</div>
            </dd>
        </div>
    )
}
