const fs=require('node:fs'),path=require('node:path');
const RealDate=Date;global.Date=class extends RealDate{constructor(...args){super(...(args.length?args:['2026-09-28T12:00:00.000Z']));}static now(){return RealDate.parse('2026-09-28T12:00:00.000Z');}};
const C=require('../operational/core.js');const w=C.empty('demo');
const seed=[
 ['Make the work report usable','Work','Unclear form labels prevent independent completion.','Complete the sample with the chosen access method.',['Identify one blocking field','Ask the template owner for a change','Retest the changed sample']],
 ['Build a small skills portfolio','Learning','Experience is not yet visible in one clear sample.','A reviewer can run and understand one example.',['Choose a small example','Build and document the example','Request a specific review']],
 ['Find a workable commute','Stability','Travel options have not been checked against the work schedule.','One route is feasible in time, cost, and access.',['Write down route requirements','Confirm service and accessibility','Try the route under agreed conditions']],
 ['Protect time for family care','Care','Responsibilities are unclear between people.','An agreed, acceptable care schedule can be used.',['List the necessary coverage','Ask participants about availability','Review the proposed arrangement']],
 ['Test a small business idea','Enterprise','The need and practical costs are uncertain.','Describe one tested need without assuming demand.',['Write the problem in one paragraph','Ask for a planning conversation','Record what the conversation changed']],
 ['Make a shared space usable','Community','The proposed activity lacks confirmed access.','Participants can use the space by agreement.',['List access requirements','Ask the space owner for permission','Review access with participants']]
];
for(let i=0;i<seed.length;i++){const [title,category,barrier,success,titles]=seed[i],g=C.addGoal(w,{title,category,barrier,success});let previous;
 for(let j=0;j<3;j++){let a=C.addAction(w,{goalId:g.id,title:titles[j],owner:j===1?'Potential helper — unassigned':'Person choosing the goal',due:'2026-10-'+String(1+i+j).padStart(2,'0'),cost:j===0?0:null,minutes:j===0?20:j===1?15:45,need:j===1?'An explicit response from the relevant person':'',provider:j===1?'Possible provider — not contacted':'',support:j===1?'requested':'not_needed',supportNote:j===1?'Fictional request status for demonstration only.':'',dependsOn:j===2?[previous.id]:[]});if(j===0&&i<3)C.completeAction(w,a.id,'Illustrative completion only. No real activity is claimed.');previous=a;}
 if(i<4)C.observe(w,{goalId:g.id,outcome:i===0?'improved':i===1?'no_change':i===2?'unknown':'harm',kind:'self_reported',note:['Fictional example: sample labels became clearer; usability still needs a check.','Fictional example: no reviewer response yet.','Fictional example: route information alone did not establish access.','Fictional example: the proposed schedule created an unacceptable burden.'][i],source:'Synthetic scenario authored for interface testing.'});
 if(i===3)C.reviseGoal(w,g.id,{title,category,barrier,success,state:'paused'},'Illustrative choice to stop and reconsider the burden.');
}
// Stable fixture identities and timestamps. These are scenario coordinates, not event reports.
const map=new Map();for(const [list,prefix] of [[w.goals,'g'],[w.actions,'a'],[w.observations,'o'],[w.events,'e']])list.forEach((v,i)=>map.set(v.id,prefix+'-demo-'+String(i+1).padStart(3,'0')));
const raw=JSON.stringify(w,(k,v)=>map.has(v)?map.get(v):v);const stable=JSON.parse(raw);function dates(o){for(const [k,v] of Object.entries(o)){if(['createdAt','reviewedAt','at'].includes(k)&&typeof v==='string')o[k]='2026-09-28T12:00:00.000Z';else if(v&&typeof v==='object')dates(v);}}dates(stable);
fs.writeFileSync(path.join(__dirname,'../data/demo.json'),JSON.stringify(C.validate(stable))+'\n');console.log(C.metrics(stable));
