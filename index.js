const fs = require('fs');
const Papa = require('papaparse');
const ejs = require('ejs');

const template = fs.readFileSync('template/index.ejs', 'utf8');

const templateData = {
  
};

const file = 'csv/snowsuit.csv';
fs.readFile(file, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }

  Papa.parse(data, {
    delimiter: ',',
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,

    step: function (result) {
      console.log('All rows successfully processed.');
      console.log(result.data);
    },

    complete: function (result) {
      console.log('All rows successfully processed.');
    },
    error: function (error) {
      // Handle any errors
      console.error('Parsing error:', error.message);
    },
  });
});
