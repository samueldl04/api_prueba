const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Encuentra todos los archivos de plantilla
const templates = glob.sync('app/templates/**/*.html');

templates.forEach(template => {
  let content = fs.readFileSync(template, 'utf8');
  
  // Busca y reemplaza las referencias estáticas con asset_path
  content = content.replace(
    /(href|src)=["']\/static\/(.*?)["']/g, 
    '$1="{{ asset_path(\'$2\') }}"'
  );
  
  fs.writeFileSync(template, content);
  console.log(`Updated: ${template}`);
});