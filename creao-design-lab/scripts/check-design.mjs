import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import ts from 'typescript';
import postcss from 'postcss';
import valueParser from 'postcss-value-parser';

const REQUIRED_IDS = ['DS-001','DS-002','LAY-001','A11Y-001','STATE-001','NAV-001','RESP-001','GOV-001','A11Y-002','VISUAL-001','CMP-001','CMP-002'];
const REQUIRED_LINKS = ['src/styles/tokens.css','src/styles/components.css','src/styles/layouts.css','governance/rules.json','governance/exceptions.json','scripts/check-design.mjs','tests/e2e/design.spec.ts','tests/e2e/accessibility.spec.ts','tests/e2e/visual.spec.ts','governance/page-states.json','tests/design/page-states.test.mjs'];
const namedColors = new Set(('aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white whitesmoke yellow yellowgreen').split(' '));
const colorFunctions = new Set(['rgb','rgba','hsl','hsla','hwb','lab','lch','oklab','oklch','color','device-cmyk']);
const controls = new Set(['button','input','select','textarea']);
const read = (root,file) => fs.readFileSync(path.join(root,file),'utf8');
const exists = (root,file) => fs.existsSync(path.join(root,file));
function files(root,dir) {
  if (!exists(root,dir)) return [];
  return fs.readdirSync(path.join(root,dir),{withFileTypes:true}).flatMap(entry => {
    const file = path.posix.join(dir,entry.name);
    return entry.isDirectory() ? files(root,file) : [file];
  });
}

export function checkDesign(root) {
  root = path.resolve(root);
  const violations=[]; const suppressed=[];
  const add=(ruleId,file,line,message)=>violations.push({ruleId,file,line:line||1,message});
  let registry, exemptions;
  for (const file of ['governance/rules.json','governance/exceptions.json']) {
    try { const parsed=JSON.parse(read(root,file)); if(file.endsWith('rules.json')) registry=parsed; else exemptions=parsed; }
    catch (error) { add('GOV-001',file,1,`Cannot read valid JSON: ${error.message}`); }
  }
  if (!registry || registry.version!==1 || !Array.isArray(registry.rules)) add('GOV-001','governance/rules.json',1,'Expected version:1 and rules array.');
  else {
    const ids=new Set();
    for(const rule of registry.rules) {
      const required=['id','title','severity','layer','source','check','scope','limitations'];
      if (!rule || required.some(key=>typeof rule[key]!=='string'||!rule[key].trim()) || !['error','warning'].includes(rule.severity)||!['static','browser','governance'].includes(rule.layer)) {
        add('GOV-001','governance/rules.json',1,'Invalid rule schema: required nonempty fields, severity and layer enums.'); continue;
      }
      if(ids.has(rule.id)||!REQUIRED_IDS.includes(rule.id)) add('GOV-001','governance/rules.json',1,`Duplicate or unknown rule: ${rule.id}`);
      ids.add(rule.id);
      if(!exists(root,rule.check)) add('GOV-001','governance/rules.json',1,`Missing check entry: ${rule.check}`);
    }
    for(const id of REQUIRED_IDS) if(!ids.has(id)) add('GOV-001','governance/rules.json',1,`Missing required rule ${id}`);
  }
  const validExceptions=[];
  if(!exemptions || Object.keys(exemptions).some(k=>k!=='exceptions') || !Array.isArray(exemptions.exceptions)) add('GOV-001','governance/exceptions.json',1,'Expected {exceptions:[]} and no additional fields.');
  else {
    const ids=new Set();
    for(const item of exemptions.exceptions) {
      const keys=['id','ruleId','path','reason','owner','approvedBy','expires'];
      if(!item || keys.some(k=>typeof item[k]!=='string'||!item[k].trim()) || Object.keys(item).some(k=>!keys.includes(k)) || ids.has(item.id) || !REQUIRED_IDS.includes(item.ruleId)||item.ruleId==='GOV-001') {add('GOV-001','governance/exceptions.json',1,'Invalid exception schema, duplicate id or non-exemptible GOV-001 rule.');continue;}
      ids.add(item.id);
      const parsed = new Date(item.expires+'T23:59:59Z');
      if(!/^\d{4}-\d{2}-\d{2}$/.test(item.expires)||!Number.isFinite(parsed.getTime())||parsed.toISOString().slice(0,10)!==item.expires||parsed.getTime()<Date.now()) add('GOV-001','governance/exceptions.json',1,`Expired/invalid exception date: ${item.id}`);
      else if(path.isAbsolute(item.path)||item.path.split('/').includes('..')||!exists(root,item.path)) add('GOV-001','governance/exceptions.json',1,`Exception must name an existing exact relative path: ${item.id}`);
      else if(!['DS-001','DS-002'].includes(item.ruleId)) add('GOV-001','governance/exceptions.json',1,`Browser exceptions require a separately reviewed test contract, unsupported here: ${item.id}`);
      else validExceptions.push(item);
    }
  }
  if(!exists(root,'design.md')) add('GOV-001','design.md',1,'Missing design.md.');
  else {
    const doc=read(root,'design.md');
    for(const id of REQUIRED_IDS) if(!doc.includes(id)) add('GOV-001','design.md',1,`Missing rule index ${id}`);
    const links=[...doc.matchAll(/\[[^\]]*\]\((?:<([^>]+)>|([^\s)]+))(?:\s+"[^"]*")?\)/g)].map(m=>m[1]||m[2]);
    const local=links.filter(link=>!/^([a-z]+:|#|\/)/i.test(link)).map(link=>decodeURIComponent(link.split('#')[0]));
    for(const file of local) if(!exists(root,file)) add('GOV-001','design.md',1,`Broken local link: ${file}`);
    for(const file of REQUIRED_LINKS) if(!local.some(link=>path.normalize(link)===file)) add('GOV-001','design.md',1,`Missing executable file link: ${file}`);
  }
  const allFiles=files(root,'src');
  const tokenFile='src/styles/tokens.css';
  const tokens=new Set();
  if(exists(root,tokenFile)) {
    try { postcss.parse(read(root,tokenFile),{from:tokenFile}).walkDecls(decl=>{if(decl.prop.startsWith('--'))tokens.add(decl.prop);}); }
    catch(error){add('GOV-001',tokenFile,error.line,`Invalid token CSS: ${error.reason}`);}
  } else add('GOV-001',tokenFile,1,'Token authority is missing.');
  for(const file of allFiles.filter(file=>file.endsWith('.css')&&file!==tokenFile)) {
    try {
      postcss.parse(read(root,file),{from:file}).walkDecls(decl=>{
        // URL and font-family words are not color declarations. Custom properties are governed too.
        const colorBearing=decl.prop.startsWith('--')||/^(color|background.*|border.*|outline.*|.*shadow|fill|stroke|caret-color|accent-color|text-decoration.*|.*column-rule.*)$/i.test(decl.prop);
        valueParser(decl.value).walk(node=>{
          if(node.type==='function'&&node.value.toLowerCase()==='url')return false;
          if(node.type==='function'&&node.value==='var') {
            const name=node.nodes.find(n=>n.type==='word')?.value;
            if(name&&!tokens.has(name))add('DS-001',file,decl.source.start.line,`Unregistered CSS token ${name}.`);
          }
          if((node.type==='word' && (/^#[\da-f]{3,8}$/i.test(node.value)||(colorBearing&&namedColors.has(node.value.toLowerCase())))) || (node.type==='function'&&colorFunctions.has(node.value.toLowerCase()))) add('DS-001',file,decl.source.start.line,`Literal color ${node.value}; use a registered token from ${tokenFile}.`);
        });
      });
    }catch(error){add('DS-001',file,error.line,`Cannot parse governed CSS: ${error.reason||error.message}`);}
  }
  const sourceFiles=allFiles.filter(file=>/\.[jt]sx?$/.test(file));
  // The compiler's symbol table resolves lexical scope. It avoids treating an unrelated,
  // shadowed identifier as a control just because another declaration shares its name.
  const program=ts.createProgram(sourceFiles.map(file=>path.join(root,file)),{allowJs:true,noResolve:true,noLib:true,noEmit:true,jsx:ts.JsxEmit.Preserve});
  const checker=program.getTypeChecker();
  function intrinsicControl(node, seen=new Set()) {
    if(ts.isStringLiteral(node)||ts.isNoSubstitutionTemplateLiteral(node))return controls.has(node.text)?node.text:undefined;
    if(ts.isParenthesizedExpression(node)||ts.isAsExpression(node)||ts.isTypeAssertionExpression(node)||ts.isSatisfiesExpression(node))return intrinsicControl(node.expression,seen);
    if(!ts.isIdentifier(node))return undefined;
    let symbol=checker.getSymbolAtLocation(node);
    if(symbol && symbol.flags & ts.SymbolFlags.Alias)symbol=checker.getAliasedSymbol(symbol);
    if(!symbol||seen.has(symbol))return undefined;
    seen.add(symbol);
    const declaration=symbol.valueDeclaration;
    if(declaration && ts.isVariableDeclaration(declaration) && declaration.initializer && declaration.parent.flags & ts.NodeFlags.Const)return intrinsicControl(declaration.initializer,seen);
    return undefined;
  }
  for(const file of sourceFiles.filter(file=>/^src\/(app|pages|features|components\/(patterns|features))\//.test(file))) {
    const source=program.getSourceFile(path.join(root,file));
    if(!source)throw new Error(`Compiler did not load ${file}`);
    for(const error of source.parseDiagnostics) add('DS-002',file,source.getLineAndCharacterOfPosition(error.start||0).line+1,ts.flattenDiagnosticMessageText(error.messageText,' '));
    const visit=node=>{
      if(ts.isJsxOpeningElement(node)||ts.isJsxSelfClosingElement(node)) {
        const tag=node.tagName.getText(source);
        const control=controls.has(tag)?tag:intrinsicControl(node.tagName);
        if(control)add('DS-002',file,source.getLineAndCharacterOfPosition(node.getStart()).line+1,`Raw <${control}>${tag!==control?` through const alias ${tag}`:''} bypasses approved src/components/ui components.`);
      }
      ts.forEachChild(node,visit);
    };visit(source);
  }
  const remaining=violations.filter(v=>{
    const exception=validExceptions.find(item=>item.ruleId===v.ruleId&&item.path===v.file);
    if(exception){suppressed.push({...v,exceptionId:exception.id});return false;}return true;
  });
  return {version:1,root,passed:remaining.length===0,violations:remaining,exceptions:suppressed};
}

if(process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  try {
    const args=process.argv.slice(2); const index=args.indexOf('--root');
    if(args.some((a,i)=>a!=='--root'&&(index<0||i!==index+1))||index>=0&&!args[index+1]) throw new Error('Usage: node scripts/check-design.mjs [--root <path>]');
    const result=checkDesign(index>=0?args[index+1]:process.cwd());
    process.stdout.write(JSON.stringify(result,null,2)+'\n'); process.exitCode=result.passed?0:1;
  }catch(error){process.stdout.write(JSON.stringify({version:1,passed:false,error:error.message,violations:[]})+'\n');process.exitCode=2;}
}
