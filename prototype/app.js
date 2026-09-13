
'use strict';
(() => {
  const VERSION = '1.0';
  const APP = 'Dream to Action';
  const LIMIT = 4000, MAX_ENTRIES = 500, MAX_BYTES = 1048576;
  const ids = ['goal','barrier','action','evidence','readiness','owner','support','helper','supportStatus','constraints','reviewDate','kind'];
  const required = ['goal','barrier','action','evidence'];
  const labels = {
    goal:'Chosen life improvement',barrier:'Barrier',action:'Next action',evidence:'Observable sign of progress',readiness:'Self-assessed readiness',
    owner:'Proposed action owner',support:'Required support or external change',helper:'Proposed support provider',supportStatus:'Support confirmation',
    constraints:'Limits and stop conditions',reviewDate:'Review date (no reminder scheduled)',kind:'Record type'
  };
  const choices = {
    readiness:{unknown:'I do not know yet',ready:'I believe it is ready to try',blocked:'Support or a change is needed first',paused:'I choose to pause'},
    supportStatus:{unknown:'Unknown / not confirmed',requested:'Requested, awaiting an answer',confirmed:'Confirmed, according to my information',unavailable:'Not available',not_needed:'No outside support needed for this step'},
    kind:{self_reported:'My plan — self-reported',illustrative:'Illustrative example — not a real result'},
    outcome:{unresolved:'Still unresolved / not enough evidence',improved:'The barrier was reduced or access improved',achieved:'The chosen goal was reached',no_change:'No improvement observed',harm:'Harm or an unacceptable cost was observed',changed_goal:'I chose a different goal or direction'}
  };
  const $ = id => document.getElementById(id);
  let plans = [], observations = [], fileDirty = false, importBusy = false;
  const stamp = () => new Date().toISOString();
  const readDraft = () => Object.fromEntries(ids.map(id => [id, $(id).value]));
  const blank = () => Object.fromEntries(ids.map(id => [id, id === 'owner' ? 'Me' : id === 'readiness' || id === 'supportStatus' ? 'unknown' : id === 'kind' ? 'self_reported' : '']));
  const latest = () => plans[plans.length-1];
  const same = (a,b) => ids.every(id => a[id] === b[id]);
  const hasContent = () => plans.length > 0 || observations.length > 0 || !same(readDraft(),blank()) || $('observation').value.trim() !== '';
  const planIsDirty = () => !latest() || !same(readDraft(),latest().fields);
  const setDraft = fields => ids.forEach(id => { $(id).value = fields[id]; });
  function say(message) { $('status').textContent = message; }
  function clearErrors() {
    $('errors').replaceChildren(); $('errors').hidden = true;
    document.querySelectorAll('[aria-invalid]').forEach(el => el.removeAttribute('aria-invalid'));
  }
  function fail(messages) {
    clearErrors();
    const p = document.createElement('p'); p.textContent = 'Please address the following:';
    const ul = document.createElement('ul');
    messages.forEach(([id,message]) => {
      const li = document.createElement('li');
      if (id && $(id)) {
        const a = document.createElement('a'); a.href = '#' + id; a.textContent = message;
        a.addEventListener('click',event => {
          event.preventDefault(); const field = $(id); const details = field.closest('details');
          if (details) details.open = true; field.focus();
        });
        li.append(a); $(id).setAttribute('aria-invalid','true');
      } else li.textContent = message;
      ul.append(li);
    });
    $('errors').append(p,ul); $('errors').hidden = false; $('errors').focus();
  }
  function validDate(value) {
    if (!value) return true;
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value) || value.startsWith('0000')) return false;
    const date = new Date(value+'T00:00:00.000Z');
    return !Number.isNaN(date.getTime()) && date.toISOString().slice(0,10) === value;
  }
  function validateFields(fields, requireComplete) {
    const problems = [];
    ids.forEach(id => {
      if (typeof fields[id] !== 'string' || fields[id].length > LIMIT) problems.push([id,labels[id]+' must be text of at most '+LIMIT+' characters.']);
      else if (choices[id] && !Object.hasOwn(choices[id],fields[id])) problems.push([id,labels[id]+' has an unsupported value.']);
    });
    if (requireComplete) required.forEach(id => { if (typeof fields[id] === 'string' && !fields[id].trim()) problems.push([id,labels[id]+' is required.']); });
    if (typeof fields.reviewDate === 'string' && !validDate(fields.reviewDate)) problems.push(['reviewDate','Enter a valid review date or leave it blank.']);
    return problems;
  }
  function feasibility(fields) {
    if (fields.readiness === 'paused') return 'Paused by choice — no action is required by this tool.';
    if (fields.support.trim() && fields.supportStatus === 'not_needed') return 'Clarify support: a required dependency is listed, but marked not needed. The tool cannot resolve that contradiction.';
    if (fields.supportStatus === 'unavailable') return 'Needs a different support path — the listed support is not available.';
    if (fields.support.trim() && fields.supportStatus !== 'confirmed') return 'Required support is not confirmed. Do not count this step as available yet.';
    if (fields.readiness === 'blocked') return 'Support or a change is needed first. This is a condition of the step, not a personal failure.';
    if (fields.readiness === 'ready' && (fields.supportStatus === 'confirmed' || fields.supportStatus === 'not_needed')) return 'Ready to consider trying, by your report — feasibility and safety are not independently verified.';
    return 'Feasibility is still unconfirmed. Check time, cost, access, consent, and required support before acting.';
  }
  const display = (id,value) => choices[id] ? choices[id][value] : value || 'Not specified';
  function make(tag,text,className) { const el = document.createElement(tag); el.textContent = text; if (className) el.className = className; return el; }
  function fieldsDL(fields) {
    const dl = document.createElement('dl');
    ids.forEach(id => dl.append(make('dt',labels[id]),make('dd',display(id,fields[id]))));
    return dl;
  }
  function render() {
    const item = latest();
    $('empty-preview').hidden = Boolean(item); $('preview-content').hidden = !item;
    $('preview-content').replaceChildren();
    if (item) {
      $('preview-content').append(make('p',display('kind',item.fields.kind),'pill'),make('p',feasibility(item.fields),'notice'),make('p','Snapshot '+item.id+' · '+item.createdAt,'meta'),fieldsDL(item.fields));
      if (planIsDirty()) $('preview-content').prepend(make('p','Draft changes are not in this saved snapshot yet. Export includes the draft; printing does not.','warning'));
    }
    $('history-list').replaceChildren();
    // Preserve snapshot order and each snapshot's observation order rather than trusting imported clocks.
    for (const p of plans) {
      const li = document.createElement('li');
      li.append(make('p','Plan '+p.id+' · '+p.createdAt,'meta'),make('p',p.fields.goal),make('p','Action: '+p.fields.action));
      const details = document.createElement('details'); details.append(make('summary','Read this plan snapshot'),fieldsDL(p.fields)); li.append(details);
      $('history-list').append(li);
      for (const o of observations.filter(o => o.planId === p.id)) {
        const review = document.createElement('li');
        review.append(make('p','Observation '+o.id+' about '+o.planId+' · '+o.createdAt,'meta'),make('p',display('outcome',o.outcome)),make('p',o.note));
        $('history-list').append(review);
      }
    }
    $('empty-history').hidden = plans.length > 0;
  }
  function savePlan(event) {
    event.preventDefault(); clearErrors(); const fields = readDraft();
    const errors = validateFields(fields,true);
    if (plans.length >= MAX_ENTRIES) errors.push([null,'This journal has reached 500 plan snapshots. Export it and start a new journal.']);
    if (errors.length) return fail(errors);
    const id = 'p-'+String(plans.length+1).padStart(4,'0');
    plans.push({id,createdAt:stamp(),fields}); fileDirty = true; render(); say('Plan snapshot '+id+' recorded in this page. Export the journal to keep it.');
  }
  $('plan-form').addEventListener('submit',savePlan);
  $('plan-form').addEventListener('input',() => { fileDirty = true; render(); });
  $('plan-form').addEventListener('change',() => { fileDirty = true; render(); });
  $('observation').addEventListener('input',() => { fileDirty = true; });
  $('outcome').addEventListener('change',() => { fileDirty = true; });
  $('review-form').addEventListener('submit',event => {
    event.preventDefault(); clearErrors(); const errors = [];
    if (!latest()) errors.push([null,'Save a plan snapshot before adding an observation.']);
    else if (planIsDirty()) errors.push([null,'Your plan has unsaved changes. Save a snapshot first so this observation refers to the correct plan.']);
    if (!$('observation').value.trim()) errors.push(['observation','Describe what you observed.']);
    if ($('observation').value.length > LIMIT) errors.push(['observation','Keep the observation within 4000 characters.']);
    if (!Object.hasOwn(choices.outcome,$('outcome').value)) errors.push(['outcome','Select a supported outcome.']);
    if (observations.length >= MAX_ENTRIES) errors.push([null,'This journal has reached 500 observations. Export it and start a new journal.']);
    if (errors.length) return fail(errors);
    const id = 'o-'+String(observations.length+1).padStart(4,'0');
    observations.push({id,createdAt:stamp(),planId:latest().id,outcome:$('outcome').value,note:$('observation').value});
    $('observation').value = ''; $('outcome').value = 'unresolved'; fileDirty = true; render(); say('Observation '+id+' recorded as your report, not independently verified evidence. Export to keep it.');
  });
  $('example').addEventListener('click',() => {
    if (hasContent() && !window.confirm('Replace only the current draft with an illustrative example? Saved snapshots remain. Export first to preserve unsaved draft edits.')) return;
    clearErrors();
    setDraft({
      goal:'Complete a work report independently and keep control over my working time.',
      barrier:'The report template has unclear field labels, and the keyboard path has not been checked.',
      action:'Use a fictional sample report to check the required fields and keyboard path; record one blocking issue.',
      evidence:'The blocking field can be identified and completed using the chosen access method, and the completed output is checked against the sample.',
      readiness:'unknown',owner:'The person choosing this goal',
      support:'A blank sample template and an agreed route to the person who can change it.',
      helper:'Template owner — not contacted by this tool',supportStatus:'unknown',
      constraints:'Use fictional data. Do not submit real work or automate consequential decisions. Stop if the output is unreliable.',reviewDate:'',kind:'illustrative'
    });
    fileDirty = true; render(); say('Illustrative example loaded. No person has been contacted, and no real-world result is claimed.'); $('goal').focus();
  });
  function bundle() {
    return {app:APP,schemaVersion:VERSION,exportedAt:stamp(),draft:readDraft(),reviewDraft:{outcome:$('outcome').value,note:$('observation').value},plans,observations};
  }
  function download(content,type,name) {
    const blob = new Blob([content],{type});
    const url = URL.createObjectURL(blob); const a = document.createElement('a');
    a.href = url; a.download = name; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url),30000);
  }
  function makeText(data) {
    const lines = [APP+' — readable journal','Exported: '+data.exportedAt,'All entries are self-reported or explicitly illustrative. No independent verification.','Files are unencrypted. No messages or reminders have been sent.',''];
    const addFields = fields => { ids.forEach(id => lines.push(labels[id]+':',display(id,fields[id]),'')); lines.push('Feasibility note:',feasibility(fields),''); };
    lines.push('CURRENT DRAFT (may differ from the last saved snapshot)',''); addFields(data.draft);
    if (data.reviewDraft.note || data.reviewDraft.outcome !== 'unresolved') lines.push('UNSAVED OBSERVATION DRAFT',display('outcome',data.reviewDraft.outcome),data.reviewDraft.note,'');
    lines.push('PLAN SNAPSHOTS AND LINKED OBSERVATIONS','');
    for (const p of data.plans) {
      lines.push('PLAN '+p.id+' | '+p.createdAt,''); addFields(p.fields);
      for (const o of data.observations.filter(o => o.planId === p.id)) lines.push('OBSERVATION '+o.id+' | '+o.createdAt+' | Plan '+o.planId,display('outcome',o.outcome),o.note,'');
    }
    lines.push('LIMITS','The tool cannot provide services, funding, rights, or other people\'s agreement.','A date is a planning note, not a scheduled reminder.','Timestamps and imported records are unverified; this is not a tamper-proof audit log.','');
    return lines.join('\n');
  }
  $('export-json').addEventListener('click',() => {
    clearErrors(); const data = bundle();
    try { const checked = validateBundle(data); const text = JSON.stringify(checked,null,2)+'\n';
      if (new Blob([text]).size > MAX_BYTES) throw new Error('This journal exceeds the 1 MiB import limit. Export the readable report for preservation; then start a smaller journal.');
      download(text,'application/json','dream-to-action-journal.json'); fileDirty = false;
      say('Journal download requested. Verify the file was saved; it includes the draft and history and is not encrypted.');
    } catch (error) { fail([[null,error.message]]); }
  });
  $('export-text').addEventListener('click',() => {
    download(makeText(bundle()),'text/plain;charset=utf-8','dream-to-action-report.txt');
    say('Readable report download requested. This text report cannot be reimported as a journal; JSON preserves the editable structure.');
  });
  $('print').addEventListener('click',() => { if (!latest()) return fail([[null,'Save a plan snapshot before printing.']]); window.print(); });
  function object(value,name,keys) {
    if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).some(key => !keys.includes(key)) || keys.some(key => !Object.hasOwn(value,key))) throw new Error(name+' has a missing or unsupported field.');
  }
  function timestamp(value) {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/.test(value)) return false;
    const date = new Date(value); return !Number.isNaN(date.getTime()) && date.toISOString() === value;
  }
  function checkedFields(value,complete) {
    object(value,'Plan fields',ids); const problems = validateFields(value,complete);
    if (problems.length) throw new Error(problems[0][1]);
    return Object.fromEntries(ids.map(id => [id,value[id]]));
  }
  function validateBundle(data) {
    object(data,'Journal',['app','schemaVersion','exportedAt','draft','reviewDraft','plans','observations']);
    if (data.app !== APP || data.schemaVersion !== VERSION) throw new Error('Unsupported journal type or schema version.');
    if (!timestamp(data.exportedAt)) throw new Error('The journal export timestamp is invalid.');
    if (!Array.isArray(data.plans) || !Array.isArray(data.observations) || data.plans.length > MAX_ENTRIES || data.observations.length > MAX_ENTRIES) throw new Error('Journal arrays are invalid or exceed 500 entries each.');
    const draft = checkedFields(data.draft,false);
    object(data.reviewDraft,'Observation draft',['outcome','note']);
    if (!Object.hasOwn(choices.outcome,data.reviewDraft.outcome) || typeof data.reviewDraft.note !== 'string' || data.reviewDraft.note.length > LIMIT) throw new Error('The observation draft is invalid.');
    const cleanPlans = data.plans.map((p,index) => {
      object(p,'Plan snapshot',['id','createdAt','fields']);
      if (p.id !== 'p-'+String(index+1).padStart(4,'0') || !timestamp(p.createdAt)) throw new Error('Plan IDs or timestamps are invalid.');
      return {id:p.id,createdAt:p.createdAt,fields:checkedFields(p.fields,true)};
    });
    const existing = new Set(cleanPlans.map(p => p.id));
    let lastPlanNumber = 0;
    const cleanObservations = data.observations.map((o,index) => {
      object(o,'Observation',['id','createdAt','planId','outcome','note']);
      if (o.id !== 'o-'+String(index+1).padStart(4,'0') || !timestamp(o.createdAt) || !existing.has(o.planId)) throw new Error('Observation IDs, timestamps, or plan references are invalid.');
      const planNumber = Number(o.planId.slice(2));
      if (planNumber < lastPlanNumber) throw new Error('Observation order is inconsistent with forward-only plan revisions.');
      lastPlanNumber = planNumber;
      if (!Object.hasOwn(choices.outcome,o.outcome) || typeof o.note !== 'string' || !o.note.trim() || o.note.length > LIMIT) throw new Error('An observation has an invalid outcome or note.');
      return {id:o.id,createdAt:o.createdAt,planId:o.planId,outcome:o.outcome,note:o.note};
    });
    return {app:APP,schemaVersion:VERSION,exportedAt:data.exportedAt,draft,reviewDraft:{outcome:data.reviewDraft.outcome,note:data.reviewDraft.note},plans:cleanPlans,observations:cleanObservations};
  }
  $('import-file').addEventListener('change',async () => {
    const file = $('import-file').files[0]; if (!file || importBusy) return;
    clearErrors();
    const original = JSON.stringify(bundle(),(key,value) => key === 'exportedAt' ? undefined : value);
    try {
      if (file.size > MAX_BYTES) throw new Error('File is larger than 1 MiB. Nothing was imported.');
      importBusy = true;
      const data = validateBundle(JSON.parse(await file.text()));
      const current = JSON.stringify(bundle(),(key,value) => key === 'exportedAt' ? undefined : value);
      if (original !== current) throw new Error('The open journal changed while the file was read. Import again after finishing those edits.');
      if (hasContent() && !window.confirm('Replace this open journal with the imported one? Export first to preserve your current work.')) { say('Import cancelled. Current work is unchanged.'); return; }
      plans = data.plans; observations = data.observations; setDraft(data.draft);
      $('outcome').value = data.reviewDraft.outcome; $('observation').value = data.reviewDraft.note;
      fileDirty = false; render(); say('Journal restored. Imported entries and timestamps are unverified user data.');
    } catch (error) { fail([[null,'Import rejected: '+(error instanceof SyntaxError ? 'The file is not valid JSON.' : error.message)]]); }
    finally { $('import-file').value = ''; importBusy = false; }
  });
  $('clear').addEventListener('click',() => {
    if (hasContent() && !window.confirm('Clear the open draft and journal? Export first to keep them. Exported files and browser/device traces are not deleted.')) return;
    plans = []; observations = []; setDraft(blank()); $('review-form').reset(); fileDirty = false; clearErrors(); render(); say('Open journal cleared. Existing exported files and browser/device traces were not deleted.'); $('goal').focus();
  });
  window.addEventListener('beforeunload',event => { if (fileDirty) { event.preventDefault(); event.returnValue = ''; } });
  setDraft(blank()); render();
})();
