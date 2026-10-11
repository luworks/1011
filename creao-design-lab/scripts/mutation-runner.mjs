#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import crypto from 'node:crypto';
import { spawn } from 'node:child_process';
import { mutations } from '../tests/mutations/cases.mjs';

const args = process.argv.slice(2);
const value = (key, fallback) => args.includes(key) ? args[args.indexOf(key) + 1] : fallback;
const root = path.resolve(value('--root', process.cwd()));
const suite = value('--suite', 'static');
if (!['static', 'browser', 'all'].includes(suite)) throw new Error('--suite must be static, browser, or all');
const ids = value('--ids', '').split(',').filter(Boolean);
const cases = mutations.filter(m => (suite === 'all' || suite === m.suite) && (!ids.length || ids.includes(m.id)));
if (!cases.length) throw new Error('No mutation cases selected');
const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const out = path.resolve(value('--out', path.join(root, 'reports', `mutations-${suite}-${stamp}`)));
await fs.mkdir(out, { recursive: true });
const ignore = new Set(['node_modules', '.next', '.git', 'reports', 'test-results', 'playwright-report', 'experiments', '.DS_Store']);
async function sourceHash(dir) {
  const hash = crypto.createHash('sha256');
  async function walk(folder) {
    for (const entry of (await fs.readdir(folder, { withFileTypes: true })).sort((a,b)=>a.name.localeCompare(b.name))) {
      if (ignore.has(entry.name) || entry.name.endsWith('.tsbuildinfo')) continue;
      const file = path.join(folder, entry.name);
      if (entry.isDirectory()) await walk(file);
      else if (entry.isFile()) { hash.update(path.relative(dir, file)); hash.update(await fs.readFile(file)); }
    }
  }
  await walk(dir); return hash.digest('hex');
}
async function clone() {
  const workspace = await fs.mkdtemp(path.join(os.tmpdir(), 'creao-mutation-'));
  const dir = path.join(workspace, 'creao-design-lab');
  try { await fs.access(path.join(root, '..', 'exam')); await fs.symlink(path.resolve(root, '..', 'exam'), path.join(workspace, 'exam'), 'dir'); } catch {}
  await fs.cp(root, dir, {recursive:true, filter: file => !path.relative(root,file).split(path.sep).some(p => ignore.has(p) || p.endsWith('.tsbuildinfo'))});
  await fs.mkdir(path.join(dir,'reports'),{recursive:true});
  await fs.symlink(path.join(root, 'node_modules'), path.join(dir,'node_modules'),'dir');
  return dir;
}
function run(command, argv, cwd, env = {}, timeout = 120000) {
  return new Promise(resolve => {
    const start = Date.now(); let stdout = '', stderr = '', timedOut = false;
    const proc = spawn(command, argv, {cwd, env:{...process.env,...env}, detached:true, stdio:['ignore','pipe','pipe']});
    proc.stdout.on('data',x=>stdout+=x); proc.stderr.on('data',x=>stderr+=x);
    const timer = setTimeout(()=>{timedOut=true; try {process.kill(-proc.pid,'SIGKILL');} catch{}},timeout);
    proc.on('error',error=>{clearTimeout(timer); resolve({command:[command,...argv],exit:null,stdout,stderr:stderr+error.message,error:true,durationMs:Date.now()-start});});
    proc.on('close',(code,signal)=>{clearTimeout(timer);resolve({command:[command,...argv],exit:code,signal,stdout,stderr,timedOut,durationMs:Date.now()-start});});
  });
}
async function preserveArtifacts(dir, destination) {
  const saved=[];
  for (const name of ['test-results','playwright-report']) {
    try { await fs.access(path.join(dir,name)); await fs.cp(path.join(dir,name),path.join(destination,name),{recursive:true}); saved.push(path.join(destination,name)); } catch {}
  }
  return saved;
}
async function freePort() {
  const server = net.createServer(); await new Promise((r,j)=>server.listen(0,'127.0.0.1',r).once('error',j));
  const port=server.address().port;await new Promise(r=>server.close(r));return port;
}
async function browser(dir, rule) {
  const port=await freePort(); const url=`http://127.0.0.1:${port}`;
  const proc=spawn(process.execPath,[path.join(dir,'node_modules/next/dist/bin/next'),'dev','--webpack','--hostname','127.0.0.1','--port',String(port)],{cwd:dir,detached:true,env:{...process.env,NEXT_TELEMETRY_DISABLED:'1'},stdio:['ignore','pipe','pipe']});
  let serverLog='';proc.stdout.on('data',x=>serverLog+=x);proc.stderr.on('data',x=>serverLog+=x);
  let serverError=null;proc.on('error',e=>serverError=e.message);
  try {
    const deadline=Date.now()+90000;let ready=false;
    while(Date.now()<deadline && !serverError && proc.exitCode===null) {
      try { const res=await fetch(url+'/files',{signal:AbortSignal.timeout(2000)}); if(res.status===200) {ready=true;break;} } catch {}
      await new Promise(r=>setTimeout(r,300));
    }
    if(!ready) return {command:['next','dev','--webpack'],exit:null,error:true,stderr:serverError||'Server failed readiness',serverLog};
    const healthScript = `const {chromium}=require('@playwright/test'); (async()=>{const browser=await chromium.launch(process.env.PW_CHANNEL?{channel:process.env.PW_CHANNEL}:{});const results=[];try{for(const route of ['/files','/connectors','/agents','/guidelines']){const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));const response=await page.goto(process.env.BASE_URL+route);await page.waitForLoadState('networkidle');results.push({route,status:response?.status(),pageErrors:errors});await page.close();}console.log(JSON.stringify(results));process.exitCode=results.some(r=>r.status!==200||r.pageErrors.length)?1:0;}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=2;});`;
    const health=await run(process.execPath,['-e',healthScript],dir,{BASE_URL:url},60000);
    if(health.exit!==0) return {...health,error:true,serverLog,reason:'Browser health check failed before rule assertions.'};
    const result=await run(process.execPath,[path.join(dir,'node_modules/@playwright/test/cli.js'),'test','--grep',`\\[(?:${rule})\\]`,'--reporter=json','--workers=1','--max-failures=1'],dir,{BASE_URL:url,PW_EXTERNAL_SERVER:'1',PLAYWRIGHT_JSON_OUTPUT_NAME:'',PLAYWRIGHT_JSON_OUTPUT_FILE:''},120000);
    result.browserHealth=health;
    result.serverLog=serverLog;
    if(/Failed to compile|Module not found|SyntaxError:/.test(serverLog)) result.error=true;
    return result;
  } finally {
    await new Promise(resolve=>{
      let done=false;
      const finish=()=>{if(!done){done=true;clearTimeout(timer);resolve();}};
      const timer=setTimeout(()=>{try{process.kill(-proc.pid,'SIGKILL');}catch{}finish();},5000);
      proc.once('close',finish);
      try{process.kill(-proc.pid,'SIGTERM');}catch{finish();}
      if(proc.exitCode!==null)finish();
    });
  }
}
function parseJson(output) { try { return JSON.parse(output); } catch {return null;} }
function testsFrom(report) {
  const result=[];const walk=s=>{for(const spec of s.specs||[])for(const test of spec.tests||[])result.push({title:spec.title,status:test.status,results:test.results||[]});for(const sub of s.suites||[])walk(sub);};
  if(report)walk(report);return result;
}
function classify(item, result, check) {
  if(result.error||result.timedOut||result.exit===null) return {classification:'error',reason:'Runner/server failure or timeout; not a design-rule kill.'};
  if(item.suite==='static') {
    if(!check||result.exit>1) return {classification:'error',reason:'Invalid checker output or execution failure.'};
    const hit=check.violations?.some(v=>v.ruleId===item.rule);
    if(item.kind==='positive')return {classification:result.exit===0?'passed':'false-positive',reason:result.exit===0?'Positive control accepted.':'Positive control rejected by the original checker.'};
    return {classification:result.exit===1&&hit?'killed':'survived',reason:hit?'Original checker reported target rule.':'Target rule did not reject the mutation.'};
  }
  if(!check) return {classification:'error',reason:'Missing Playwright JSON report.'};
  const tests=testsFrom(check);const targets=tests.filter(t=>t.title.includes(`[${item.rule}]`));
  const globalErrors=(check.errors||[]).filter(error=>!String(error.message||'').includes('Testing stopped early after 1 maximum allowed failures.'));
  if(!targets.length || globalErrors.length) return {classification:'error',reason:'No target tests executed, or Playwright global error.'};
  const failed=targets.filter(t=>t.status==='unexpected');
  const assertionFailure=failed.some(t=>t.results.some(r=>(r.errors||[]).some(e=>/expect\(/.test(e.message||e.stack||''))));
  if(failed.length&&!assertionFailure) return {classification:'error',reason:'Target failed without an assertion (navigation/compilation/runner failure).'};
  if(item.kind==='positive')return {classification:result.exit===0?'passed':'false-positive',reason:result.exit===0?'Positive control passed browser checks.':'Positive control rejected by browser assertions.'};
  return {classification:result.exit!==0&&assertionFailure?'killed':'survived',reason:assertionFailure?'Original browser assertion for target rule failed.':'Target rule passed or did not assert a violation.'};
}
async function executeCheck(dir,item) {
  if(item.suite==='browser')return browser(dir,item.rule);
  return run(process.execPath,[path.join(root,'scripts/check-design.mjs'),'--root',dir],dir);
}
const before=await sourceHash(root);
const report={version:1,startedAt:new Date().toISOString(),suite,baselineHash:before,sourceRoot:root,scope:'Predefined mutations only; independent engineer experiments excluded.',baselines:[],cases:[]};
const baselineDir=await clone();
try {
  const staticBaseline=await executeCheck(baselineDir,{suite:'static'});
  report.baselines.push({suite:'static',...staticBaseline});
  if(staticBaseline.exit!==0) throw new Error('Unchanged static baseline failed');
  const typeBaseline=await run(process.execPath,[path.join(baselineDir,'node_modules/typescript/bin/tsc'),'--noEmit','--incremental','false'],baselineDir);
  report.baselines.push({suite:'typecheck',...typeBaseline});
  if(typeBaseline.exit!==0)throw new Error('Unchanged typecheck baseline failed');
  const browserRules=[...new Set(cases.filter(c=>c.suite==='browser').map(c=>c.rule))];
  if(browserRules.length) {
    const result=await browser(baselineDir,browserRules.join('|'));report.baselines.push({suite:'browser',rules:browserRules,...result});
    if(result.exit!==0)throw new Error('Unchanged browser baseline failed');
    console.log('Unchanged browser baseline passed.');
  }
  for(const item of cases) {
    const dir=await clone();const caseOut=path.join(out,item.id);await fs.mkdir(caseOut,{recursive:true});
    const record={id:item.id,kind:item.kind,suite:item.suite,rule:item.rule,description:item.description,baselineHash:before,patches:[],startedAt:new Date().toISOString()};
    try {
      record.caseBaselineHash=await sourceHash(dir);
      if(record.caseBaselineHash!==before) throw new Error('Shared source changed since baseline; this case is invalid, not a rule kill.');
      for(const edit of item.edits) {
        const file=path.join(dir,edit.file);const original=await fs.readFile(file,'utf8');
        const changed=edit.transform?edit.transform(original):original.replace(edit.before,edit.after);
        if(changed===original)throw new Error(`Patch did not apply: ${edit.file}`);
        if(edit.before && original.split(edit.before).length!==2)throw new Error(`Patch anchor not unique: ${edit.file}`);
        await fs.writeFile(file,changed);record.patches.push({file:edit.file,before:original,after:changed});
      }
      record.mutatedHash=await sourceHash(dir);
      const typecheck=await run(process.execPath,[path.join(dir,'node_modules/typescript/bin/tsc'),'--noEmit','--incremental','false'],dir);
      record.typecheck={...typecheck};
      if(typecheck.exit!==0){record.classification=typecheck.timedOut||typecheck.error?'error':'invalid';record.reason='Mutation did not pass typecheck; not counted as a design-rule kill.';}
      else {const result=await executeCheck(dir,item);record.check=result;const parsed=parseJson(result.stdout);record.evidence=parsed;Object.assign(record,classify(item,result,parsed));}
    } catch(error) {record.classification='invalid';record.reason=error.message;}
    finally {record.artifacts=await preserveArtifacts(dir,caseOut);try{await fs.rm(path.dirname(dir),{recursive:true,force:true,maxRetries:10,retryDelay:300});}catch(error){record.cleanupError=error.message;record.classification='error';record.reason='Isolated runtime cleanup failed; original check evidence retained.';}}
    record.finishedAt=new Date().toISOString();await fs.writeFile(path.join(caseOut,'receipt.json'),JSON.stringify(record,null,2)+'\n');
    report.cases.push(record);console.log(`${item.id}: ${record.classification} (${item.rule})`);
  }
} catch(error) {report.baselineError=error.message;for(const item of cases)report.cases.push({id:item.id,kind:item.kind,suite:item.suite,rule:item.rule,classification:'invalid',reason:error.message});}
finally {report.baselineArtifacts=await preserveArtifacts(baselineDir,path.join(out,'baseline-artifacts'));try{await fs.rm(path.dirname(baselineDir),{recursive:true,force:true,maxRetries:10,retryDelay:300});}catch(error){report.cleanupError=error.message;}}
report.finalHash=await sourceHash(root);report.baselineUnchanged=before===report.finalHash;report.finishedAt=new Date().toISOString();
report.counts=Object.fromEntries(['killed','survived','passed','false-positive','invalid','error'].map(s=>[s,report.cases.filter(c=>c.classification===s).length]));
report.negativeDenominator=report.counts.killed+report.counts.survived;
report.killRate=report.negativeDenominator?report.counts.killed/report.negativeDenominator:null;
await fs.writeFile(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');
const md=`# Design mutation report\n\nGenerated: ${report.finishedAt}\n\nSuite: ${suite}. Baseline SHA-256: \`${before}\`. Shared source unchanged: **${report.baselineUnchanged}**.\n\n${report.scope}\n\n| Case | Kind | Rule | Result | Evidence |\n| --- | --- | --- | --- | --- |\n${report.cases.map(c=>`| ${c.id} | ${c.kind} | ${c.rule} | ${c.classification} | ${c.reason} |`).join('\n')}\n\nNegative kill denominator: ${report.counts.killed} / ${report.negativeDenominator}. Invalid: ${report.counts.invalid}; errors: ${report.counts.error}; positive passes: ${report.counts.passed}; false positives: ${report.counts['false-positive']}.\n\n${suite==='static'?'Runtime mutations were not executed in this run.':''}\n\nFull patches, command exits and rule-level evidence are in [report.json](report.json) and per-case receipts. A killed case means a target-rule assertion failed; process/server timeouts and type errors do not count. Browser route health is checked first; classification still requires review of the retained target assertion and server logs. Source hashes cover copied source/configuration, excluding dependencies/build outputs/reports/experiments.\n`;
await fs.writeFile(path.join(out,'report.md'),md);
console.log(`Report: ${out}`);
process.exitCode=report.baselineUnchanged&&!report.baselineError&&!report.cleanupError&&!report.counts.survived&&!report.counts['false-positive']&&!report.counts.invalid&&!report.counts.error?0:1;
