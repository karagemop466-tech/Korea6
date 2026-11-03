const {test}=require('node:test'); const assert=require('node:assert/strict');const {midnight,addDays,localDate,union,gaps}=require('../assets/core.js');
test('Pacific days handle DST transitions',()=>{assert.equal((midnight('2027-03-15')-midnight('2027-03-14'))/3600000,23);assert.equal((midnight('2027-11-08')-midnight('2027-11-07'))/3600000,25);assert.equal(localDate(midnight('2027-03-14')),'2027-03-14');});
test('date arithmetic crosses year and leap day',()=>{assert.equal(addDays('2028-02-28',1),'2028-02-29');assert.equal(addDays('2026-12-31',1),'2027-01-01');});
test('overlapping and adjacent intervals merge and clip',()=>{assert.deepEqual(union([[2,6],[4,8],[-1,2],[10,12]],0,11),[[0,8],[10,11]]);assert.deepEqual(gaps([[2,6],[4,8],[10,12]],0,11),[[0,2],[8,10]]);});
