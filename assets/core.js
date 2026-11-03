/* Pure time/interval helpers. All calendar days use America/Los_Angeles, including DST. */
const zone = 'America/Los_Angeles';
function parts(ms, options={}) { return new Intl.DateTimeFormat('en-CA',{timeZone:zone,year:'numeric',month:'2-digit',day:'2-digit',...options}).formatToParts(new Date(ms)).reduce((a,p)=>(a[p.type]=p.value,a),{}); }
function localDate(ms){let p=parts(ms);return `${p.year}-${p.month}-${p.day}`;}
function addDays(date,n){let d=new Date(date+'T12:00:00Z'); d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10);}
function midnight(date) { // Convert a Pacific civil midnight to UTC; DST shifts are not hard-coded.
  const [y,m,d]=date.split('-').map(Number); const target=Date.UTC(y,m-1,d); let t=target;
  for(let i=0;i<4;i++){const p=parts(t,{hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}); const represented=Date.UTC(+p.year,+p.month-1,+p.day,+p.hour,+p.minute,+p.second); t+=target-represented;}
  return t;
}
function union(intervals,lo,hi){const sorted=intervals.map(([a,b])=>[Math.max(a,lo),Math.min(b,hi)]).filter(([a,b])=>a<b).sort((a,b)=>a[0]-b[0]); const merged=[]; for(const pair of sorted){let last=merged[merged.length-1];if(last && pair[0]<=last[1])last[1]=Math.max(last[1],pair[1]); else merged.push(pair.slice());}return merged;}
function gaps(intervals,lo,hi){let cursor=lo;const out=[];for(const [a,b] of union(intervals,lo,hi)){if(cursor<a)out.push([cursor,a]);cursor=b;}if(cursor<hi)out.push([cursor,hi]);return out;}
if(typeof module!=='undefined')module.exports={localDate,addDays,midnight,union,gaps};
