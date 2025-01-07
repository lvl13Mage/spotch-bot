import type { Configuration } from 'webpack';
import { rules } from './webpack.rules';
import { plugins } from './webpack.plugins';
import path from 'path';
const tailwindcss = require('tailwindcss');

rules.push({
  test: /\.css$/,
  use: [{ loader: 'style-loader' }, { loader: 'css-loader' }],
});
export const rendererConfig: Configuration = {
  module: {
    rules,
  },
  plugins: [
    tailwindcss,
  ],
  resolve: {
    extensions: ['.js', '.ts', '.jsx', '.tsx', '.css'],
    alias: { '@': path.join(__dirname, './src') },
    fallback: {
      "path": require.resolve("path-browserify"),
      "fs": false
    }
  },
};