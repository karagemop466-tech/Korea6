const fs=require('fs');const assert=require('assert');
const targets={index:'index',scoreboard:'schedule',vacation:'vacations',calendar:'schedule',windows:'vacations',summary:'index','data-mlb':'schedule','data-nfl':'schedule','data-ncaaf':'schedule',radio:'radio',methodology:'sources',flagged:'review'};
for(const [page,target] of Object.entries(targets)){
 const content=fs.readFileSync(page+'.html','utf8');
 assert(content.includes(`url=site/${target}.html`),page);
 assert(content.includes(`href="site/${target}.html"`),page+' fallback link');
 assert(fs.existsSync(`site/${target}.html`),page+' target');
 assert(!/VERIFIED anchors|FREE — no live radio sports|no 7-day all-clear window exists/i.test(content),page+' unsafe historical claim');
}
console.log('Legacy entry points resolve to evidence dashboard with a fallback link.');
