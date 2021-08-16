import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json'
// import { terser } from 'rollup-plugin-terser';
// import babel from '@rollup/plugin-babel';

export default {
  input: 'index.js',
  output: {
    file: 'dist/index.js',
    format: 'cjs',
  },
  plugins: [
    resolve(),
    commonjs(),
    json(),
    // terser(),
    // babel({ babelHelpers: 'bundled' })
  ]
};
