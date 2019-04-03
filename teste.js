function countyNames(names) {
    let countys = [];
    for(var i=0; i < names.length; i++) {
        countys.push(names[i].Enhetsnamn);
    } 
    return [countys]
};

function countyResults(results){
    let values 
    for(var i=0; i < results.length; i++) {
        values.push(results[i].Resultat);
    }
    return [values]
};


var countyResult1 = countyResults(costPerCare);
var countyCostName = countyNames(costPerCare);

//skapar en funktion för att ta bort sek. Och byter datatyp till INT.
function sliceSEK(sek) {  //namnger funktionen och sätter in ett random namn till den nya variabeln.
    for(var i=0; i < sek.length; i++) { 
        sek[i] = parseInt(sek[i].slice(0,4)); //varibeln omvandlas till INT och kortas ner från start 0 till position 4.
}   return sek //returnerar som int.
};

var countyResult2 = sliceSEK(countyResult1); //anropar funktionen och vilet värdet som ska skickas in.

console.log(countyResult2)


function nameResult(names) {
    let countys = []
    let years = [];
    for(var i=0; i < names.length; i++) {
        countys.push(names[i].Enhetsnamn);
        years.push(names[i].År);
    } 
    return [countys,years]
}

var tezt = nameResult(Enhetsnamn)
console.log(tezt)

var trustName = nameResult(["Enhtesnamn"])
 console.log(trustName)

 function filtrering17(trust){
    var trust2017 = trust.filter(function(trust17) {
        return (trust17.År == "2017");
    });
    return trust2017;
 }
   

    var trust2018 = trust.filter(function(trust17) {
        return (trust18.År == "2018");
    });
