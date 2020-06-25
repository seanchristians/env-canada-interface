var days = 0;
var temps = [
	0,// x < -10
	0,// -10 < x < 0
	0,// 0 < x < 10
	0// 10 < x
];

function get_data(id, year) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", `https://cors-anywhere.herokuapp.com/https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=xml&stationID=${id}&Year=${year}&timeframe=2&submit= Download+Data`);
	xhr.send();
	xhr.onload = function() {
		var data = xhr.responseXML;

		data.querySelector(`stationdata[day="${d}"][month="${m}"][year="${y}"]`)
	}
};

function render_data() {
	var id = document.querySelector("input[name=\"station\"]:checked").value;
	var start = document.querySelector("input[name=\"start-date\"]").value;
	var end = document.querySelector("input[name=\"end-date\"]").value;

	get_data(id, start.slice(0,4));
	get_data(id, end.slice(0,4));
};

function search_table() {
	var input = document.getElementById("search").value.toUpperCase();
	var table = document.getElementById("stations").getElementsByTagName("tr");

	for (var i in table) {
		td = table[i].getElementsByTagName("td")[0];
		if (td) {
			txtValue = td.textContent || td.innerText;
			if (txtValue.toUpperCase().indexOf(input) > -1) {
				table[i].style.display = "";
			} else {
				table[i].style.display = "none";
			}
		}
	}
};

window.onload = function() {
	for (var i in stations) {
		var row = document.getElementById("stations").insertRow();
		var radio = document.createElement("input");
		radio.setAttribute("type", "radio");
		radio.setAttribute("name", "station");
		radio.setAttribute("value", stations[i]["Station ID"]);
		var name = document.createElement("td"); name.innerHTML = stations[i].Name;
		var prov = document.createElement("td"); prov.innerHTML = stations[i].Province;

		row.appendChild(radio); row.appendChild(name); row.appendChild(prov);
	}
};
