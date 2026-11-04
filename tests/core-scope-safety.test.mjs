import {test} from 'node:test';
import {readFileSync} from 'node:fs';
import {strict as assert} from 'node:assert';
test('scope page does not promote historical maximum or address reception to fact',()=>{
 const js=readFileSync('site/core-scope.js','utf8');
 assert.match(js,/annual maximum unknown/);
 assert.match(js,/Reception unverified/);
 assert.doesNotMatch(js,/esc\(row\.(coreFourScope|fullAmFmScope)\.longestGap\)/);
 assert.doesNotMatch(js,/0 scheduled games in Core/);
});
