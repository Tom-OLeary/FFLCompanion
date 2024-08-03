let callbacks = {};

function add(_case, fn) {
    callbacks[_case] = callbacks[_case] || [];
    callbacks[_case].push(fn);
}

export default function pseudoSwitch(value) {
    let barColor, widthValue;
    if (callbacks[value]) {
        callbacks[value].forEach(function (fn) {
            [barColor, widthValue] = fn();
        });
    }
    return [barColor, widthValue];
}

let ownerCount = [...Array(23).keys()];  // TODO integrate true owner count
let iterRate = Math.floor(100 / ownerCount.length);

if (!callbacks.length) {
    ownerCount.map((item, i) => {
        add(item, function () {
            let i1, barColor, widthValue;
            if (item <= ownerCount.length / 2) {
                // generate green range
                i1 = (item + 1) * 18;
                barColor = "#" + (i1).toString(16) + (186).toString(16) + (i1).toString(16);
                widthValue = (100 - (iterRate * item)).toString() + "%";
            } else {
                // generate red range
                i1 = (item - (item - 1)) * 30;
                barColor = "#" + (230).toString(16) + (i1).toString(16) + (i1).toString(16);
                widthValue = (iterRate * item).toString() + "%";
            }
            return [barColor, widthValue];
        });
    })
}