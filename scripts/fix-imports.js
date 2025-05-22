const fs = require('fs');
const path = require('path');

// Lista de archivos con importaciones absolutas que necesitan ser corregidas
const filesToFix = [
  'app/static/js/admin/clock_in/overview.js',
  'app/static/js/components/widgets/clockIn.js',
  'app/static/js/components/widgets/clockInOverview.js'
];

// Procesar cada archivo
filesToFix.forEach(filePath => {
  console.log(`Procesando: ${filePath}`);
  
  // Leer el archivo
  const content = fs.readFileSync(filePath, 'utf8');
  
  // Verificar si el archivo tiene importaciones absolutas
  if (content.includes('from \'/static/js/')) {
    // Construir la ruta relativa
    const currentDir = path.dirname(filePath).replace('app/static/js/', '');
    const depth = currentDir.split('/').length;
    const relativePath = '../'.repeat(depth);
    
    // Reemplazar las importaciones absolutas con relativas
    const updatedContent = content.replace(/from ['"]\/static\/js\//g, `from '${relativePath}`);
    
    // Guardar el archivo modificado
    fs.writeFileSync(filePath, updatedContent);
    console.log(`  Rutas actualizadas en: ${filePath}`);
  } else {
    console.log(`  No se encontraron importaciones absolutas.`);
  }
});

console.log('Importaciones corregidas con éxito.');
