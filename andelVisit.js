var visits = 
[
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Blekinge",
    "År": "2017",
    "Resultat": "1256"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Dalarna",
    "År": "2017",
    "Resultat": "1111"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Gotland",
    "År": "2017",
    "Resultat": "1340"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Gävleborg",
    "År": "2017",
    "Resultat": "1488"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Halland",
    "År": "2017",
    "Resultat": "1604"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Jämtland Härjedalen",
    "År": "2017",
    "Resultat": "1273"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Jönköpings län",
    "År": "2017",
    "Resultat": "1852"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Kalmar län",
    "År": "2017",
    "Resultat": "1412"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Kronoberg",
    "År": "2017",
    "Resultat": "1272"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Norrbotten",
    "År": "2017",
    "Resultat": "1234"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Riket",
    "År": "2017",
    "Resultat": "1406"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Skåne",
    "År": "2017",
    "Resultat": "1326"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Stockholms län",
    "År": "2017",
    "Resultat": "1735"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Sörmland",
    "År": "2017",
    "Resultat": "1284"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Uppsala län",
    "År": "2017",
    "Resultat": "1267"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Värmland",
    "År": "2017",
    "Resultat": "1135"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Västerbotten",
    "År": "2017",
    "Resultat": "1100"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Västernorrland",
    "År": "2017",
    "Resultat": "1092"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Västmanland",
    "År": "2017",
    "Resultat": "1320"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Västra Götaland",
    "År": "2017",
    "Resultat": "1345"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Örebro län",
    "År": "2017",
    "Resultat": "1161"
},
{
    "tel": "Antal besök hos läkare i primärvården per 1 000 invånare",
    "Enhetsnamn": "Östergötland",
    "År": "2017",
    "Resultat": "1004"
}
]

let visitCounty = countyNames(visits);
let visitResult1 = countyResults(visits);
let visitResult = sliceSEK(visitResult1)

var trace1 = {
    x: visitCounty,
    y: visitResult,
    fill: 'tozeroy',
    type: 'scatter',
    mode:'lines+markers',
};

var layout = {
    title: 'Antal besök hos läkare i primärvården per 1 000 invånare (2017)',
    margin: {
        b: 90,
    },
    xaxis: {
        title:{
            text: 'Källa: Verksamhetsstatistik, Sveriges Kommuner och Landsting',
        },
            titlefont: {
                size: 12,
        },
    },
    tickfont: {
        size: 12, 
        color: 'rgb(107, 107, 107)'
    },
};

var data = [trace1];



Plotly.newPlot('visits', data, layout, {}, {showSendToCloud:true});