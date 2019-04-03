 //genererar JSON fil.
let Papa = require('papaparse');//anropar packetet.
let csvFile = './trust17.csv'; //filnamnet 
let { data: jsonFile } = Papa.parse(csvFile, { header: true, delimiter: ',', 
skipEmptyLines: true }) //anger output för data med header och separering.
console.log(JSON.stringify(jsonFile, null, 2))
