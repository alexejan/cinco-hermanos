var costPerCare = [

{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Blekinge",
    "År": "2016",
    "Resultat": "1576 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Dalarna",
    "År": "2016",
    "Resultat": "1826 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Gotland",
    "År": "2016",
    "Resultat": "1604 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Gävleborg",
    "År": "2016",
    "Resultat": "1880 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Halland",
    "År": "2016",
    "Resultat": "1494 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Jämtland Härjedalen",
    "År": "2016",
    "Resultat": "2121 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Jönköpings län",
    "År": "2016",
    "Resultat": "1658 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Kalmar län",
    "År": "2016",
    "Resultat": "1837 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Kronoberg",
    "År": "2016",
    "Resultat": "1796 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Norrbotten",
    "År": "2016",
    "Resultat": "1875 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Riket",
    "År": "2016",
    "Resultat": "1706 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Skåne",
    "År": "2016",
    "Resultat": "1349 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Stockholms län",
    "År": "2016",
    "Resultat": "1503 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Sörmland",
    "År": "2016",
    "Resultat": "1707 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Uppsala län",
    "År": "2016",
    "Resultat": "1484 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Värmland",
    "År": "2016",
    "Resultat": "1730 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Västerbotten",
    "År": "2016",
    "Resultat": "1828 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Västernorrland",
    "År": "2016",
    "Resultat": "1766 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Västmanland",
    "År": "2016",
    "Resultat": "1410 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Västra Götaland",
    "År": "2016",
    "Resultat": "1808 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Örebro län",
    "År": "2016",
    "Resultat": "1742 SEK"
},
{
    "tel": "Kostnad per vårdkontakt i primärvården",
    "Enhetsnamn": "Östergötland",
    "År": "2016",
    "Resultat": "1828 SEK"
}
];
//skapar en fuktion för att ta fram enhetsnamn och resultat. I fortsättningen anropar jag endast funktionen.
function countyNames(names) { //deklarerar variablen för funktionen.
    let countys = []; //skapar en lokal variabel i funktionen som en array.
    for(var i=0; i < names.length; i++) { //loopar igenom array så länge variablens längd är större och lägger på 1.
        countys.push(names[i].Enhetsnamn); //laddar in properties i min lokala variabel.
    } 
    return countys //returnerar variablen.
};

//samma process som ovan.
function countyResults(results){ 
    let values = [];
    for(var i=0; i < results.length; i++) {
        values.push(results[i].Resultat);//laddar in lokala variablen.
    }
    return values //returnerar array properties.
}; 


var countyResult1 = countyResults(costPerCare); //anropar funktionen
var countyCostName = countyNames(costPerCare); //--

//skapar en funktion för att ta bort sek. Och byter datatyp till INT.
function sliceSEK(sek) {  //definierar funktionens variabel. och sätter in ett random namn till den nya variabeln.
    for(var i=0; i < sek.length; i++) { //loppar igenom array.
        sek[i] = parseInt(sek[i].slice(0,4)); //varibeln omvandlas till INT och kortas ner från start 0 till position 4.
}   return sek //returnerar variablens properties som int.
};

var countyResult = sliceSEK(countyResult1); //anropar funktionen och vilet värdet som ska skickas in.

var data = [{
    type: 'bar',
    x: countyResult,
    y: countyCostName,
    marker: {
        color: 'rgb(51, 153, 102)'
    },
    transforms: [{  //sorterar efter x
        type: "sort",
        target: countyResult,  
}],
    orientation: 'h',
}];


    var layout = {
        title: 'Kostnad i kronor per vårdkontakt i primärvården (2016)',
        height: 600,
        margin:{
            l: 150, //margin vänster 150px
        },
        yaxis: {
            
            tickfont:{ //fonten på y-texten.
                family: 'Arial sans-serif',
                size: 15,
            },
        },
        xaxis: {
            title:{
                text: 'Källa: Verksamhetsstatistik, Sveriges Kommuner och Landsting',
            },
                titlefont: {
                    size: 12,
            },
        },
};
  
Plotly.newPlot('costPerCare', data, layout);