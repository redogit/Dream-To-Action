'use strict';
const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');
const path=require('node:path');const file=path.join(__dirname,'../operational/core.js');
const exists=fs.existsSync(file);const C=exists?require(file):{};
test('operational state module exists',()=>assert.ok(exists,'operational/core.js is not implemented'));
if(exists){
 const fresh=()=>C.empty();
 const goal=w=>C.addGoal(w,{title:'Chosen direction',barrier:'A barrier',success:'An observable change',category:'Learning'});
 const action=(w,g,extra={})=>C.addAction(w,{goalId:g.id,title:'One chosen action',owner:'Me',due:'',minutes:null,cost:null,need:'',provider:'',support:'unknown',supportNote:'',dependsOn:[],...extra});
 test('personal workspace starts empty',()=>{let w=fresh();assert.equal(w.mode,'personal');assert.equal(w.goals.length,0);assert.equal(C.metrics(w).done,0);});
 test('unknown support never becomes ready',()=>{let w=fresh(),g=goal(w),a=action(w,g);assert.equal(C.status(w,a),'blocked');});
 test('no external support is an explicit declaration',()=>{let w=fresh(),g=goal(w),a=action(w,g,{support:'not_needed'});assert.equal(C.status(w,a),'ready');});
 test('unconfirmed named helper remains blocked',()=>{let w=fresh(),g=goal(w),a=action(w,g,{provider:'Possible helper',need:'A ride',support:'requested'});assert.equal(C.status(w,a),'blocked');});
 test('contradictory support cannot be marked ready',()=>{let w=fresh(),g=goal(w);assert.throws(()=>action(w,g,{need:'Transport',support:'not_needed'}));});
 test('confirmed support requires provider and confirmation note',()=>{let w=fresh(),g=goal(w);assert.throws(()=>action(w,g,{support:'confirmed'}));});
 test('dependencies must complete first',()=>{let w=fresh(),g=goal(w),a=action(w,g,{support:'not_needed'}),b=action(w,g,{support:'not_needed',dependsOn:[a.id]});assert.equal(C.status(w,b),'blocked');C.completeAction(w,a.id,'Observed completion');assert.equal(C.status(w,b),'ready');});
 test('blocked action cannot silently complete',()=>{let w=fresh(),g=goal(w),a=action(w,g);assert.throws(()=>C.completeAction(w,a.id,'Done'));assert.equal(a.state,'todo');});
 test('completion requires a note and does not count as improvement',()=>{let w=fresh(),g=goal(w),a=action(w,g,{support:'not_needed'});assert.throws(()=>C.completeAction(w,a.id,''));C.completeAction(w,a.id,'Task done');assert.equal(C.metrics(w).improved,0);assert.equal(C.metrics(w).done,1);});
 test('goal revision preserves old text and invalidates unfinished action',()=>{let w=fresh(),g=goal(w),a=action(w,g,{support:'not_needed'});C.reviseGoal(w,g.id,{title:'Revised direction',barrier:g.barrier,success:g.success,category:g.category,state:'active'},'Changed scope');assert.equal(g.history[0].title,'Chosen direction');assert.equal(C.status(w,a),'review');C.reviewAction(w,a.id,'Checked fit with the revised goal');assert.equal(C.status(w,a),'ready');});
 test('paused goals do not produce ready actions',()=>{let w=fresh(),g=goal(w),a=action(w,g,{support:'not_needed'});C.reviseGoal(w,g.id,{title:g.title,barrier:g.barrier,success:g.success,category:g.category,state:'paused'},'My choice');assert.equal(C.status(w,a),'paused');});
 test('evidence is linked to the actual revision',()=>{let w=fresh(),g=goal(w);C.observe(w,{goalId:g.id,outcome:'no_change',kind:'self_reported',note:'No change observed',source:''});assert.equal(w.observations[0].revision,1);assert.equal(C.metrics(w).improved,0);});
 test('invalid imported references are rejected atomically',()=>{let w=fresh(),g=goal(w);action(w,g);let s=JSON.stringify(w),bad=JSON.parse(s);bad.actions[0].goalId='g-missing';assert.throws(()=>C.validate(bad));assert.equal(JSON.stringify(w),s);});
 test('import rejects cycles',()=>{let w=fresh(),g=goal(w),a=action(w,g),b=action(w,g);a.dependsOn=[b.id];b.dependsOn=[a.id];assert.throws(()=>C.validate(w));});
 test('import rejects invalid date, oversized text and unknown fields',()=>{for(const patch of [{due:'2026-02-30'},{title:'x'.repeat(4001)},{extra:'hidden'}]){let w=fresh(),g=goal(w),a=action(w,g);Object.assign(a,patch);assert.throws(()=>C.validate(w));}});
 test('unknown cost stays unknown rather than zero',()=>{let w=fresh(),g=goal(w);action(w,g);action(w,g,{cost:0});action(w,g,{cost:25});assert.equal(C.metrics(w).cost,25);assert.equal(C.metrics(w).unknownCost,1);});
 test('CSV neutralizes leading spreadsheet formulas',()=>{let w=fresh(),g=goal(w);action(w,g,{title:' =HYPERLINK("bad")',owner:'+formula'});let csv=C.csv(w);assert.ok(csv.includes("' =HYPERLINK"));assert.ok(csv.includes("'+formula"));});
 test('JSON round trip preserves evidence and history',()=>{let w=fresh(),g=goal(w);action(w,g);C.observe(w,{goalId:g.id,outcome:'improved',kind:'self_reported',note:'My observation',source:''});assert.deepEqual(C.importData(JSON.stringify(w)),w);});
 test('v0.1 import retains exact parsed payload and original source ID',()=>{let old=JSON.parse(fs.readFileSync(path.join(__dirname,'../prototype/example-journal.json'),'utf8'));let w=C.importData(JSON.stringify(old));assert.deepEqual(w.legacy,old);assert.equal(w.mode,'demo');assert.equal(w.goals.length,1);assert.equal(w.actions[0].support,'unknown');});
 test('unsupported schema is rejected',()=>assert.throws(()=>C.importData('{"schema":"future"}')));
 test('support changes retain previous value in history',()=>{let w=fresh(),g=goal(w),a=action(w,g);C.updateSupport(w,a.id,{support:'confirmed',need:'Sample',provider:'Template owner',supportNote:'Reported agreement; not independently verified'});assert.equal(C.status(w,a),'ready');assert.ok(w.events.at(-1).detail.includes('unknown'));});
 test('action revisions preserve former estimates and require a reason',()=>{let w=fresh(),g=goal(w),a=action(w,g,{support:'not_needed'});assert.equal(typeof C.reviseAction,'function');assert.throws(()=>C.reviseAction(w,a.id,{title:a.title,owner:a.owner,due:'2026-10-05',minutes:30,cost:5,dependsOn:[]},''));C.reviseAction(w,a.id,{title:'Revised next action',owner:a.owner,due:'2026-10-05',minutes:30,cost:5,dependsOn:[]},'Updated estimate');assert.equal(a.minutes,30);assert.ok(w.events.at(-1).detail.includes('before'));});
 test('editing a completed action is rejected',()=>{let w=fresh(),g=goal(w),a=action(w,g,{support:'not_needed'});C.completeAction(w,a.id,'Finished');assert.equal(typeof C.reviseAction,'function');assert.throws(()=>C.reviseAction(w,a.id,{title:a.title,owner:a.owner,due:'',minutes:30,cost:5,dependsOn:[]},'Reconsider'));});

}
