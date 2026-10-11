import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { checkDesign } from '../../scripts/check-design.mjs';
const project=path.resolve(import.meta.dirname,'../..');
function fixture(t) {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'creao-check-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const put=(file,text)=>{fs.mkdirSync(path.dirname(path.join(root,file)),{recursive:true});fs.writeFileSync(path.join(root,file),text);};
  const linked=['src/styles/tokens.css','src/styles/components.css','src/styles/layouts.css','governance/rules.json','governance/exceptions.json','scripts/check-design.mjs','tests/e2e/design.spec.ts','tests/e2e/accessibility.spec.ts','tests/e2e/visual.spec.ts','governance/page-states.json','tests/design/page-states.test.mjs'];
  for(const file of linked)put(file,'');
  put('governance/rules.json',fs.readFileSync(path.join(project,'governance/rules.json'),'utf8'));
  put('governance/exceptions.json','{"exceptions":[]}');
  put('src/styles/tokens.css',':root { --text: #111; --surface: #fff; }');
  put('src/styles/components.css','.card { color: var(--text); background: var(--surface); }');
  put('design.md','DS-001 DS-002 LAY-001 A11Y-001 STATE-001 NAV-001 RESP-001 GOV-001 A11Y-002 VISUAL-001\n'+linked.map(file=>`[${file}](${file})`).join('\n'));
  return {root,put};
}
test('compliant AST baseline ignores comments and source strings',t=>{
  const {root,put}=fixture(t);
  put('src/app/page.tsx','const sample = "<button>red</button>"; /* <input/> */ export default function Page(){ return <Button>{sample}</Button> }');
  put('src/components/ui/index.tsx','export const Button=()=> <button>Open</button>');
  put('src/styles/layouts.css','/* #ff0000 */ .card { background-image: url("/red.png"); color: var(--text); }');
  assert.deepEqual(checkDesign(root).violations,[]);
});
test('CSS AST rejects color fallbacks, named colors, functions and unknown tokens',t=>{
  const {root,put}=fixture(t);
  put('src/styles/layouts.css','.a { color: var(--text, #f00); border: 1px solid red; background: rgb(1 2 3); box-shadow: 0 1px var(--unknown); }');
  const errors=checkDesign(root).violations;
  assert.equal(errors.length,4);assert(errors.every(e=>e.ruleId==='DS-001'));assert(errors.every(e=>e.line===1));
});
test('JSX AST flags native controls in governed composition scopes',t=>{
  const {root,put}=fixture(t);
  put('src/app/page.tsx','export default function Page(){ return <><button>Open</button><input /><textarea /><select /></> }');
  assert.equal(checkDesign(root).violations.filter(e=>e.ruleId==='DS-002').length,4);
});
test('GOV detects stale exception, missing IDs, broken links',t=>{
  const {root,put}=fixture(t);
  put('governance/rules.json','{"version":1,"rules":[]}');
  put('governance/exceptions.json',JSON.stringify({exceptions:[{id:'x',ruleId:'DS-001',path:'src/styles/layouts.css',reason:'temporary migration',owner:'design',approvedBy:'review receipt',expires:'2000-01-01'}]}));
  fs.appendFileSync(path.join(root,'design.md'),'\n[broken](missing.css)');
  const errors=checkDesign(root).violations;
  assert(errors.some(e=>e.message.includes('Expired')));assert(errors.some(e=>e.message.includes('Broken')));assert.equal(errors.filter(e=>e.message.includes('Missing required rule')).length,10);
});
test('exceptions are exact-file, valid dates and visible in output',t=>{
  const {root,put}=fixture(t);
  put('src/styles/layouts.css','.a { color: red }');
  put('src/styles/components.css','.b { color: blue }');
  put('governance/exceptions.json',JSON.stringify({exceptions:[{id:'migration',ruleId:'DS-001',path:'src/styles/layouts.css',reason:'scheduled repair',owner:'design',approvedBy:'test fixture only',expires:'2999-01-01'}]}));
  const result=checkDesign(root);
  assert.equal(result.exceptions.length,1);assert.equal(result.violations.length,1);assert.equal(result.violations[0].file,'src/styles/components.css');
});
test('invalid calendar expiry is rejected rather than normalized silently',t=>{
  const {root,put}=fixture(t);
  put('governance/exceptions.json',JSON.stringify({exceptions:[{id:'bad-date',ruleId:'DS-001',path:'src/styles/layouts.css',reason:'fixture',owner:'design',approvedBy:'test',expires:'2999-02-31'}]}));
  assert(checkDesign(root).violations.some(e=>e.ruleId==='GOV-001'&&e.message.includes('date')));
});
test('const intrinsic aliases and alias chains are rejected through lexical symbols',t=>{
  const {root,put}=fixture(t);
  put('src/app/page.tsx', `const Native = ('button' as const); const Chained=Native; export default function Page(){ return <Chained>Open</Chained>; }`);
  const errors=checkDesign(root).violations;
  assert.equal(errors.length,1);assert.equal(errors[0].ruleId,'DS-002');assert(errors[0].message.includes('const alias Chained'));
});
test('shadowed identifiers use their local declarations rather than matching a name',t=>{
  const {root,put}=fixture(t);
  put('src/app/page.tsx', `const Native = 'button'; export default function Page(){ const Native='div' as const; return <Native>Content</Native>; }`);
  assert.deepEqual(checkDesign(root).violations,[]);
});
