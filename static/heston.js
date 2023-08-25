const vars = ["initial_asset", "initial_variance", "Rate_of_return", "theta", "k", "dt", "sigma", "correlation_with_asset", "simulation_time"]
const initial_url = "/api/heston?";

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
            let output = document.querySelector("#output");
            output.classList.remove("hidden");
            document.querySelector("#vol").innerHTML = `${res.stochastic_volatility.slice(-1)[0].toFixed(2)}%`;

            let array = [[...Array(parseInt(res.stochastic_volatility.length) + 1).keys()].slice(1), res.stochastic_volatility];
            output = array[0].map((_, colIndex) => array.map(row => row[colIndex]));

            let data = new google.visualization.DataTable();
            data.addColumn("number", "T");
            data.addColumn("number", "Stochastic Volatility");
            data.addRows(output);

            let options = {
                title: form.get("model") + "Stochastic Volatility through Simulation Time",
                legend: {position: "bottom"},
            };

            document.getElementById('graph').classList.remove("hidden")
            let chart = new google.charts.Line(document.getElementById('graph'));
            chart.draw(data, google.charts.Line.convertOptions(options));
        })
        .catch(error => console.error("Error fetching data:", error));
};
