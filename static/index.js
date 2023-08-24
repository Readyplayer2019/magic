/*
google.charts.load('current', {'packages':['line']});

document.querySelector("#calculate").onclick = () => {
    let form = new FormData(document.querySelector("#inputs"))
    let r = form.get("r") / 100
    let S = form.get("S")
    let K = form.get("K")
    let T = form.get("T")
    let volatility = form.get("volatility") / 100
    let model = form.get("model")
    fetch(`/api?r=${r}&S=${S}&K=${K}&T=${T}&volatility=${volatility}&model=${model}`).then((response) => {
        response.json().then(res => {
            let call_prices = res[0]
            let put_prices = res[1]

            let output = document.querySelector("#output")
            output.classList.remove("hidden")
            document.querySelector("#call").innerHTML = call_prices
            document.querySelector("#put").innerHTML = put_prices
            let array = [[...Array(parseInt(T)+1).keys()].slice(1), call_prices, put_prices]


            output = array[0].map((_, colIndex) => array.map(row => row[colIndex]));


            let data = new google.visualization.DataTable()
            data.addColumn("number", "Years")
            data.addColumn("number", "Call Price")
            data.addColumn("number", "Put Price")
            data.addRows(output)

            let options = {
                title: model + " Option Price against Maturity",
                legend: { position: "botttom" },
                backgroundColor: "#c1d9ff",
                chartArea: {
                    backgroundColor: "#c1d9ff"
                }
            }

            let chart = new google.charts.Line(document.getElementById('graph'))
            chart.draw(data, google.charts.Line.convertOptions(options))
        })
    })
}
*/
google.charts.load('current', {'packages':['line']});

document.querySelector("#calculate").onclick = () => {
    let form = new FormData(document.querySelector("#inputs"))
    let r = form.get("r") / 100;
    let S = form.get("S");
    let K = form.get("K");
    let T = form.get("T");
    let volatility = form.get("volatility") / 100;
    let model = form.get("model");

    fetch(`/api?r=${r}&S=${S}&K=${K}&T=${T}&volatility=${volatility}&model=${model}`)
    .then(response => response.json())
    .then(res => {
        let output = document.querySelector("#output");
        output.classList.remove("hidden");
        document.querySelector("#call").innerHTML = res.call_prices;
        document.querySelector("#put").innerHTML = res.put_prices;

        let array = [[...Array(parseInt(T) + 1).keys()].slice(1), res.call_prices, res.put_prices];
        output = array[0].map((_, colIndex) => array.map(row => row[colIndex]));

        let data = new google.visualization.DataTable();
        data.addColumn("number", "Years");
        data.addColumn("number", "Call Price");
        data.addColumn("number", "Put Price");
        data.addRows(output);

        let options = {
            title: model + " Option Price against Maturity",
            legend: { position: "bottom" },
            backgroundColor: "#c1d9ff",
            chartArea: { backgroundColor: "#c1d9ff" }
        };

        let chart = new google.charts.Line(document.getElementById('graph'));
        chart.draw(data, google.charts.Line.convertOptions(options));
    })
    .catch(error => console.error("Error fetching data:", error));
};
