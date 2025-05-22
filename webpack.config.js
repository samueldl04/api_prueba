// webpack.config.js
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const fs = require('fs');

// Directorios de origen y destino
const ASSET_PATH = process.env.ASSET_PATH || '/static/';
const SRC_DIR = path.resolve(__dirname, 'app/static');
const DIST_DIR = path.resolve(__dirname, 'app/static/dist');
const TEMPLATES_DIR = path.resolve(__dirname, 'app/templates');

// Encuentra todos los archivos JS que podrían ser puntos de entrada
const getEntryPoints = () => {
  const entries = {};
  
  // JS files
  const jsFiles = getAllFiles(path.join(SRC_DIR, 'js'), '.js');
  jsFiles.forEach(file => {
    const relativePath = path.relative(path.join(SRC_DIR, 'js'), file);
    const entryName = relativePath.replace('.js', '');
    entries[entryName] = file;
  });
  
  return entries;
};

// Función para encontrar todos los archivos con una extensión específica en un directorio (recursivamente)
function getAllFiles(dir, ext) {
  let files = [];
  const items = fs.readdirSync(dir);
  
  items.forEach(item => {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      const subFiles = getAllFiles(fullPath, ext);
      files = files.concat(subFiles);
    } else if (item.endsWith(ext)) {
      files.push(fullPath);
    }
  });
  
  return files;
}

// Generar plugins HTML para cada template
const getHtmlPlugins = () => {
  const templates = getAllFiles(TEMPLATES_DIR, '.html');
  
  return templates.map(template => {
    const filename = path.relative(TEMPLATES_DIR, template);
    return new HtmlWebpackPlugin({
      template,
      filename,
      inject: false, // No inyectar scripts automáticamente
      minify: {
        collapseWhitespace: true,
        removeComments: true,
        removeRedundantAttributes: true,
        removeScriptTypeAttributes: true,
        removeStyleLinkTypeAttributes: true,
        useShortDoctype: true
      }
    });
  });
};

module.exports = (env, argv) => {
  const isProduction = argv.mode === 'production';
  
  return {
    mode: isProduction ? 'production' : 'development',
    entry: getEntryPoints(),
    output: {
      path: DIST_DIR,
      filename: isProduction ? 'js/[name].[contenthash].js' : 'js/[name].js',
      assetModuleFilename: 'assets/[hash][ext][query]',
      publicPath: ASSET_PATH,
      clean: true // Limpiar el directorio dist antes de cada build
    },
    devtool: isProduction ? 'source-map' : 'eval-source-map',
    module: {
      rules: [
        // Reglas para JavaScript
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env']
            }
          }
        },
        // Reglas para CSS
        {
          test: /\.css$/,
          use: [
            MiniCssExtractPlugin.loader,
            'css-loader'
          ]
        },
        // Reglas para imágenes
        {
          test: /\.(png|svg|jpg|jpeg|gif)$/i,
          type: 'asset/resource',
          generator: {
            filename: 'img/[name].[hash][ext]'
          }
        },
        // Reglas para fuentes
        {
          test: /\.(woff|woff2|eot|ttf|otf)$/i,
          type: 'asset/resource',
          generator: {
            filename: 'fonts/[name].[hash][ext]'
          }
        }
      ]
    },
    optimization: {
      minimize: isProduction,
      minimizer: [
        new TerserPlugin({
          terserOptions: {
            format: {
              comments: false,
            },
          },
          extractComments: false,
        }),
        new CssMinimizerPlugin()
      ],
      splitChunks: {
        chunks: 'all',
        name: 'vendor'
      }
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: isProduction ? 'css/[name].[contenthash].css' : 'css/[name].css'
      }),
      new WebpackManifestPlugin({
        fileName: 'manifest.json',
        publicPath: ASSET_PATH
      }),
      // Añadir plugins HTML
      ...getHtmlPlugins()
    ]
  };
};