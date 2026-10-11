import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Intended installed path: tests/design/page-states.test.mjs.
// Staging verification uses explicit PAGE_STATE_PROJECT_ROOT and PAGE_STATE_CATALOG.
const root = process.env.PAGE_STATE_PROJECT_ROOT || path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const catalogPath = process.env.PAGE_STATE_CATALOG || path.join(root, 'governance/page-states.json');
const nonempty = value => typeof value === 'string' && value.trim().length > 0;
const readJSON = file => JSON.parse(fs.readFileSync(file, 'utf8'));
function routeFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => entry.isDirectory() ? routeFiles(path.join(dir, entry.name)) : /^page\.[cm]?[jt]sx?$/.test(entry.name) ? [path.join(dir, entry.name)] : []);
}
function declaredRoute(file) {
  const parts = path.relative(path.join(root, 'src/app'), path.dirname(file)).split(path.sep);
  // Route groups and parallel-slot folder names do not add URL segments.
  return '/' + parts.filter(part => part && !/^\(.*\)$/.test(part) && !part.startsWith('@')).join('/');
}
function allSpecs(report) {
  return [...(report.specs || []), ...(report.suites || []).flatMap(allSpecs)];
}
export function validateCatalog(catalog) {
  const errors = [];
  if (catalog.version !== 1) errors.push('Unsupported catalog version');
  if (!Array.isArray(catalog.routes) || !Array.isArray(catalog.states) || !catalog.viewports) return ['Missing routes/states/viewports'];
  const routePaths = catalog.routes.map(route => route.path);
  if (new Set(routePaths).size !== routePaths.length) errors.push('Duplicate route');
  for (const file of routeFiles(path.join(root, 'src/app'))) {
    const route = declaredRoute(file);
    if (!routePaths.includes(route)) errors.push(`Uncatalogued source route: ${route}`);
    if (!catalog.routes.some(item => item.path === route && item.source === path.relative(root, file).split(path.sep).join('/'))) errors.push(`Route source mismatch: ${route}`);
  }
  for (const route of catalog.routes) {
    if (!nonempty(route.scope) || !nonempty(route.source) || !fs.existsSync(path.join(root, route.source))) errors.push(`Invalid route scope/source: ${route.path}`);
    if (!catalog.states.some(state => state.route === route.path)) errors.push(`Route lacks state coverage entry: ${route.path}`);
  }
  for (const [id, viewport] of Object.entries(catalog.viewports)) {
    if (!Number.isInteger(viewport.width) || viewport.width < 1 || !Number.isInteger(viewport.height) || viewport.height < 1) errors.push(`Invalid viewport: ${id}`);
  }
  const knownRules = new Set(readJSON(path.join(root, 'governance/rules.json')).rules.map(rule => rule.id));
  const seen = new Set();
  for (const state of catalog.states) {
    if (!nonempty(state.id) || seen.has(state.id)) errors.push(`Missing/duplicate state id: ${state.id}`);
    seen.add(state.id);
    if (!routePaths.includes(state.route)) errors.push(`Unknown state route: ${state.id}`);
    if (!['implemented', 'notImplemented'].includes(state.implementation)) errors.push(`Invalid state implementation: ${state.id}`);
    if (!nonempty(state.description) || !state.setup?.length || !state.setup.every(nonempty)) errors.push(`Missing reproducible setup: ${state.id}`);
    if (!state.scope?.assertions?.length || !state.scope.assertions.every(nonempty) || !nonempty(state.scope.limitations)) errors.push(`Missing state scope: ${state.id}`);
    if (!state.viewports?.length || state.viewports.some(id => !catalog.viewports[id])) errors.push(`Invalid viewport references: ${state.id}`);
    if (!state.rules?.length || state.rules.some(id => !knownRules.has(id))) errors.push(`Invalid rule references: ${state.id}`);
    if (!Array.isArray(state.checks) || !state.checks.length) errors.push(`Missing check coverage: ${state.id}`);
    for (const check of state.checks || []) {
      if (!['behavior', 'axe', 'visual', 'manual'].includes(check.kind) || !['implemented', 'planned', 'manual', 'notImplemented'].includes(check.implementation) || !['notVerified', 'passed', 'failed', 'notApplicable'].includes(check.execution)) errors.push(`Invalid check status: ${state.id}`);
      if (state.implementation === 'notImplemented' && check.execution !== 'notApplicable') errors.push(`Unimplemented state claims execution: ${state.id}`);
      if (check.implementation === 'implemented' && (!nonempty(check.checkRef) || !fs.existsSync(path.join(root, check.checkRef)))) errors.push(`Missing implemented check path: ${state.id}`);
      if (check.expectedRuns !== undefined && (!Number.isInteger(check.expectedRuns) || check.expectedRuns < 1)) errors.push(`Invalid expected run count: ${state.id}`);
      if (check.implementation === 'implemented' && ['behavior','axe','visual'].includes(check.kind) && !nonempty(check.testTitle)) errors.push(`Implemented browser check needs an exact test title: ${state.id}`);
      if (check.executedViewports && (!Array.isArray(check.executedViewports) || check.executedViewports.some(v => typeof v === 'string' ? !catalog.viewports[v] : !v || !Number.isInteger(v.width) || v.width < 1 || !Number.isInteger(v.height) || v.height < 1))) errors.push(`Invalid executed viewport: ${state.id}`);
      if (['passed', 'failed'].includes(check.execution)) {
        if (!['implemented', 'manual'].includes(check.implementation) || !nonempty(check.coverageScope) || !check.evidence?.length) errors.push(`Execution needs scope and evidence: ${state.id}`);
        for (const evidence of check.evidence || []) {
          const file = path.resolve(root, evidence);
          if (!fs.existsSync(file)) { errors.push(`Missing execution evidence: ${state.id}: ${evidence}`); continue; }
          if (['behavior','axe','visual'].includes(check.kind) && check.testTitle && evidence.endsWith('.json')) {
            const report = readJSON(file);
            const specs = allSpecs(report).filter(item => item.title === check.testTitle);
            if (specs.length !== (check.expectedRuns || 1)) errors.push(`Receipt lacks exact claimed test count/title: ${state.id}`);
            else if (check.execution === 'passed' && !specs.every(spec => spec.tests?.length && spec.tests.every(item => item.results?.length && item.results.every(result => result.status === 'passed')))) errors.push(`Receipt does not prove pass: ${state.id}`);
          }
        }
      }
    }
  }
  return errors;
}
const catalog = readJSON(catalogPath);
test('page-state catalog covers source routes and validates state/check/evidence links', () => assert.deepEqual(validateCatalog(catalog), []));
test('catalog rejects duplicate state ids', () => {
  const invalid = structuredClone(catalog); invalid.states.push(structuredClone(invalid.states[0]));
  assert.ok(validateCatalog(invalid).some(error => error.includes('duplicate state id')));
});
test('catalog rejects missing source routes', () => {
  const invalid = structuredClone(catalog); invalid.routes = invalid.routes.filter(route => route.path !== '/files');
  assert.ok(validateCatalog(invalid).some(error => error.includes('Uncatalogued source route: /files')));
});
test('catalog rejects states without an explicit assertion scope', () => {
  const invalid = structuredClone(catalog); delete invalid.states[0].scope;
  assert.ok(validateCatalog(invalid).some(error => error.includes('Missing state scope')));
});
test('catalog rejects fabricated passes without execution evidence', () => {
  const invalid = structuredClone(catalog); invalid.states[0].checks[0].execution = 'passed';
  assert.ok(validateCatalog(invalid).some(error => error.includes('Execution needs scope and evidence')));
});
