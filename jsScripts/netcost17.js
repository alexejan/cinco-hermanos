var netcost = [
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Blekinge",
    "År": "2017",
    "Resultat": "4267 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Dalarna",
    "År": "2017",
    "Resultat": "4358 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Gotland",
    "År": "2017",
    "Resultat": "4045 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Gävleborg",
    "År": "2017",
    "Resultat": "5370 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Halland",
    "År": "2017",
    "Resultat": "4372 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Jämtland Härjedalen",
    "År": "2017",
    "Resultat": "5054 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Jönköpings län",
    "År": "2017",
    "Resultat": "4210 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Kalmar län",
    "År": "2017",
    "Resultat": "4582 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Kronoberg",
    "År": "2017",
    "Resultat": "4273 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Norrbotten",
    "År": "2017",
    "Resultat": "4903 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Riket",
    "År": "2017",
    "Resultat": "4391 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Skåne",
    "År": "2017",
    "Resultat": "4203 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Stockholms län",
    "År": "2017",
    "Resultat": "4330 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Sörmland",
    "År": "2017",
    "Resultat": "4486 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Uppsala län",
    "År": "2017",
    "Resultat": "3843 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Värmland",
    "År": "2017",
    "Resultat": "4376 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Västerbotten",
    "År": "2017",
    "Resultat": "4407 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Västernorrland",
    "År": "2017",
    "Resultat": "3899 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Västmanland",
    "År": "2017",
    "Resultat": "4235 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Västra Götaland",
    "År": "2017",
    "Resultat": "4709 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Örebro län",
    "År": "2017",
    "Resultat": "4249 SEK"
},
{
    "tel": "Nettokostnad per invånare för primärvård exklusive hemsjukvård och läkemedel inom läkmedelsförmånen.",
    "Enhetsnamn": "Östergötland",
    "År": "2017",
    "Resultat": "4037 SEK"
}
];

var netcostCounty = countyNames(netcost); //anropar funktionen enhetsnamn till variabeln
var netcostResult1 = countyResults(netcost);//anropar funktionen resultat till variabeln
var netcostResult = sliceSEK(netcostResult1);//anropar funktionen för att korta ner resultat properties och omvandlas till int.


var trace1 = {
  x0: ' ', 
  y: netcostResult,
  type: 'bar',
  text: netcostCounty,
  textposition: 'inside',
  hoverinfo: netcostResult,
  marker: {
    color: 'rgb(158,202,225)',
    opacity: 0.6,
    line: {
      color: 'rbg(8,48,107)',
      width: 1.5
    }
  }
};

var data = [trace1];

var layout = {
  title: 'Nettokostnad per invånare för primärvård (2017)',
    xaxis: {
        title: {
            text: 'Källa: Statistiska centralbyrån och Sveriges Kommuner och Landsting',
    },
        titlefont: {
            size: 12,
        },
    },
};
Plotly.newPlot('netcost', data, layout, {showSendToCloud:true});

