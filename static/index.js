document.querySelector("#calculate").onclick = () => {
    let form = new FormData(document.querySelector("#inputs"))
    let r = form.get("r")
    let S = form.get("S")
    let K = form.get("K")
    let T = form.get("T")
    let volatility = form.get("volatility")
    let model = form.get("model")
    fetch(`/api?r=${r}&S=${S}&K=${K}&T=${T}&volatility=${volatility}&model=${model}`).then(async (response) => {
        let res = await response.json()
        let call_prices = res[0]
        let put_prices = res[1]

        let output = document.querySelector("#output")
        output.classList.remove("hidden")
        document.querySelector("#call").innerHTML = call_prices
        document.querySelector("#put").innerHTML = put_prices
    })
}