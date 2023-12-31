const vars = ["rate", "stock", "strike", "maturity", "volatility", "model"]
const initial_url = "/api/option?";

google.charts.load('current', {'packages': ['line']});

document.querySelector("#calculate").onclick = () => {
    let form = new FormData(document.querySelector("#inputs"))

    let url = initial_url;

    for (const var_ of vars) {
        url += `${var_}=${form.get(var_)}&`;
    }

    fetch(url)
        .then(response => response.json())
        .then(res => {
            console.log(res)
            let output = document.querySelector("#output");
            output.classList.remove("hidden");
            document.querySelector("#call").innerHTML = `$${res.call_prices.slice(-1)[0].toFixed(2)}`;
            document.querySelector("#put").innerHTML = `$${res.put_prices.slice(-1)[0].toFixed(2)}`;

            let array = [[...Array(parseInt(form.get("maturity").toString()) + 1).keys()].slice(1), res.call_prices, res.put_prices];
            output = array[0].map((_, colIndex) => array.map(row => row[colIndex]));

            let data = new google.visualization.DataTable();
            data.addColumn("number", "Years");
            data.addColumn("number", "Call Price");
            data.addColumn("number", "Put Price");
            data.addRows(output);

            let options = {
                title: form.get("model") + " Option Price against Maturity",
                legend: {position: "bottom"},
            };

            document.getElementById('graph').classList.remove("hidden")
            let chart = new google.charts.Line(document.getElementById('graph'));
            chart.draw(data, google.charts.Line.convertOptions(options));
        })
        .catch(error => console.error("Error fetching data:", error));
};
