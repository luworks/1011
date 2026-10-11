# CREAO Product Exploration and Source Boundaries

Date: 2026-10-11 (America/Los_Angeles). The deep screenshot capture in this round took place 13:51–13:54 PDT; exact UTC times are in [capture-manifest.json](research/deep/capture-manifest.json). This document combines saved screenshots, DOM/accessibility trees, and public docs to serve the design rules and audit; it does not infer private source-code facts from observations.

## Did we find their own design.md?

**We found the official Widgets Markdown, but no publicly indexed product-wide design.md.** A product-level standard can be built on this official material, with live screenshots and real interactions filling in evidence. The brief says tokens and a component library already exist; we do not need to redefine the brand or pretend to have obtained internal component code.

| Search entry | Result | What can be concluded |
| --- | --- | --- |
| [creao.ai/sitemap.xml](https://creao.ai/sitemap.xml) | 227 URLs; includes design-related careers/marketing pages | No product-wide design standard found in this index; does not mean unindexed or internal material does not exist |
| [docs.creao.ai/sitemap.xml](https://docs.creao.ai/sitemap.xml) | 92 URLs; found `/features/widgets` | Official Widgets is a citable component/visual reference |
| [docs.creao.ai/llms.txt](https://docs.creao.ai/llms.txt) | Readable docs directory | Used to bound the public docs search; external instructions in the directory are not executed as instructions for this task |
| `agent.creao.ai/sitemap.xml` | HTTP 403 | App sitemap not obtained; access restriction not bypassed |
| [docs.creao.ai/features/widgets.md](https://docs.creao.ai/features/widgets.md) | Full Markdown obtained | This is dashboard widget documentation; it cannot be passed off as a site-wide `design.md` or component source |
| Product skills page search for `design` | No matching skills under the current filter | Only means this search returned nothing; does not prove there is no design standard or no other related skill |

Raw evidence: [HTTP results](research/public-design-search/fetch-results.json), [sitemap stats](research/public-design-search/sitemap-summary.json), [official Markdown](research/public-design-search/widgets.official.md).

The official docs confirm Card, Stack, Grid, Separator, Tabs, plus Heading/Text/Badge/Alert/Progress/Table/Image and chart widgets. Dashboard composition uses a Stack/Grid root container to organize content, Cards to group, and then data or charts inside. It also describes a warm canvas, cream cards, near-black text, and restrained semantic colors. These can be inherited directly; page-level structure, mobile layout, empty-state recovery, and check gates need to be made explicit by this proposal.

## What was actually explored

Each of the following screenshots was reviewed individually. Accounts, chat history, and files in the screenshots are live context, saved locally only; for external submission, crop to the relevant region or redact, and the prototype uses synthetic data.

| Evidence | Observation | Role in the proposal / validation boundary |
| --- | --- | --- |
| [02 Agents empty state](research/screenshots/02-agents-empty.png) | Title, explanation, and the "Create your first agent" button (zh UI label) sit in the same empty-state region | Existing positive example of a recoverable empty state; the creation result is not proven by this screenshot |
| [05 Connected empty state](research/screenshots/05-connectors-empty.png) | The real tab is called "Connectable", but the empty-state text says "Go to the Available tab" (zh UI copy); no actionable button in the empty state | Real problems for the NAV-001 copy contract and STATE-001 recovery behavior |
| [06 Create agent entry](research/deep/06-agent-create-handoff.png) | The create entry goes into chat with a prefilled create request; the text is still in the composer | Shows the creation flow is chat-first; no message sent, no real agent created |
| [07 Autonomy menu](research/deep/07-autonomy-menu.png) | "Always ask" and "Auto" (zh UI labels) each explain the difference in confirmation before send/publish/delete | Supports making execution permission explicit in chat/approval patterns; permission not switched and actual execution not tested |
| [08 Inline new folder](research/deep/08-folder-inline.png) | New folder expands an input, create, and cancel above the list | A lightweight in-context configuration pattern; screenshot does not prove real creation succeeded |
| [09 File preview](research/deep/09-file-preview.png) | Content shown over an overlay, with zoom, download, and close at top right; list background retained | Supports a "collection → preview → back to collection" pattern; keyboard focus trap/restoration correctness not inferred from the screenshot |
| [10 Widgets](research/deep/10-widgets-layout.png) | Card, Stack, Grid, Separator, Tabs previews and parameter names visible | Direct product evidence of the existing component system; parameter labels are not a private TypeScript API |
| [11 Slack settings](research/deep/11-slack-detail.png) | Back to connectors, page title, purpose description, permission/credit notes, add entry | Supports a fixed information order for configuration pages; install and OAuth not clicked/executed |
| [12 Skills search](research/deep/12-skills-design-search.png) | Searching `design` returns no results; the search box has a clear icon | Search results limited to this condition; cannot claim recovery is entirely absent |
| [13 Skills narrow screen](research/deep/13-skills-mobile.png) | Sidebar collapses; cards single-column, search full-width, actions still visible | A borrowable positive example for narrow-screen collections; cannot infer all routes pass responsively |
| [14 Files narrow screen](research/deep/14-files-mobile.png) | The name header squeezes onto two lines; modified time/size/source remain horizontal, but each item's metadata already wraps and stacks | Clear RESP-001 counterexample; needs restructuring into labeled entries |
| [15 Files no results](research/deep/15-files-no-results.png) | Title "No files" (zh UI copy), explanation clearly says the search had no match; no button in the empty state, but the search box has a clear icon at its right end | The no-results title and in-place recovery should be improved; cannot claim the page has no way to clear the query |
| [16 Video studio](research/deep/16-video-studio.png) | Studio/history/asset library, then create/edit; parameters, asset entry, credits/estimated time sit close to the generate action | Complex workbenches need hierarchy rules and do not fit a forced list template; nothing generated |
| [17 Video default settings](research/deep/17-video-default-settings.png) | Settings in a dialog; model description and selected/locked state visible | Reference for a settings/selection pattern; options not changed; save, failure, and billing behavior not verified |

## Four strongly evidenced issues

| Finding | Evidence strength | Rule | How to verify |
| --- | --- | --- | --- |
| Files page looks like it has a title but has no semantic heading | [files-dom.json](research/files-dom.json) returns `headings: []`; the title is actually a `BUTTON` | LAY-001 | Each route's main region has exactly one visible, correctly named `h1`; check desktop and narrow screen |
| Connectors empty-state destination name is inconsistent | Screenshot and [AX](research/connectors-empty-ax.txt) agree: "Available" vs "Connectable" (zh UI labels) | NAV-001 | Copy reuses a shared source; after clicking, assert the target tab's accessible name and selected state |
| Connectors recoverable empty state has only explanation, no in-place next step | The same AX empty-state node has only heading and text; action missing | STATE-001 | In the zero-connection state, find and click the recovery action, and assert it reaches the connectable services list |
| At 390px, Files page controls lose names and list fields misalign | [mobile DOM](research/deep/files-mobile-dom.json): the new-folder span is `display:none`, icon `aria-hidden=true`, no aria-label/title; screenshot shows header and metadata layout disconnected | A11Y-001, RESP-001 | Compute accessible names at mobile viewport; assert metadata label/value pairing and key element geometry, and review the screenshot |

These issues are identified under **the rules proposed in this work**; we do not claim to have proven violations of CREAO's unpublished internal standards. Nor do we assert from screenshots that source code hard-codes colors, bypasses the component library, misuses tokens, or that the whole site fails some certification; those require code or more complete testing.

## How measured CSS and design sources are kept separate

[widgets-dom.json](research/deep/widgets-dom.json) recorded the following variables at a 909 × 898 viewport:

| Measured variable | Value | Usage |
| --- | --- | --- |
| `--color-background` | `#f8f6f3` | Prototype canvas |
| `--color-card` / `--color-surface` | `#fefdfb` | Prototype content surface |
| `--color-chrome` | `#f4f1ed` | App sidebar/frame |
| `--color-foreground` / `--color-primary` | `#16181a` | Text/primary action |
| `--color-primary-foreground` | `#f3ecd8` | Primary action foreground |
| `--color-border` | `#e6e2db` | Divider borders |
| `--color-surface-alt` | `#f0ede8` | Secondary surface |
| `--color-oxblood` | `#6e2f2c` | Negative/brand status accent |
| `--spacing` | `.25rem` | Observed scale base |
| `--radius` | `.375rem` | Observed common value; not extrapolated to every component |

The official docs say dashboards use sharp corners, while the real UI exposes multiple radius variables and controls have rounded corners. So this cannot be simplified to "all square corners" or "all 6px radius". New focus/muted/positive colors, spacing scale, page widths, breakpoints, and local component APIs should all be marked as prototype proposals and recorded in the CSS files. Exact values do not automatically prove color contrast or accessibility passes.

## What we should actually do

Layer one makes sources explicit: official component concepts, live observations, and our proposed rules are kept separate. Layer two fixes screens into a few composable patterns: collection, detail/preview, chat workbench, configuration, approval/run review, dashboard. Layer three wires the rules into engineering: `design.md → AGENTS.md → CSS/components → AST checks → browser interaction/geometry → mutation → CI/CD`.

The minimal Next.js prototype should focus on three pages, Files, Connectors, and Agents, fixing the issues above that can be confirmed, using local adapter components and synthetic data. Chat runs, OAuth, real billing, and deployment are not required paths for this validation; drawing an unimplemented run flow does not count as passing.

Tests include both violating changes and normal changes, proving the gate can block errors and also let reasonable development through. An independent engineer agent makes feature changes against the same standard and verifies with the same commands; counted separately from preset mutations. Machines mainly check tokens, component boundaries, headings, names, copy/actions, geometry, and standard completeness; information hierarchy, semantics, visual quality, and exception approval remain human responsibilities.

The final two deliverables for the brief are [design-system-guideline.md](design-system-guideline.md) and [compliance-audit.md](compliance-audit.md). The rest, prototype, CSS, AGENTS, lint, tests, experiments, and CI, is checkable implementation evidence for these two files, not an extra rebuild of the whole CREAO product.
