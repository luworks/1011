# Design and Enforce CREAO’s Product Design Guidelines

- **Company:** Creao AI
- **Due:** October 11, 3:30 PM PDT
- **Company logo:** [Creao AI logo](https://qlxjnqevmgetfexxayem.supabase.co/storage/v1/object/public/workspace-avatars/org/f9d7b241-8dc3-4374-a880-e8932e094bd9?v=1789378593026)

Creao already has a design system — turn it into rules that actually get followed, and add the layout-level guideline that sits on top of it.

## Context

Creao is an AI agent operating system company — chat-first, with engineers and their own coding agents shipping new UI continuously. Creao already has a design system: tokens and a component library exist. But nothing enforces it. Engineers make their own layout and interaction calls feature by feature, and nothing above the component level says how a whole screen should be structured.

You're Creao's first dedicated product designer, reporting to the CTO. The provided screens and the upcoming feature brief make the problem concrete: some component usage already looks inconsistent, and nobody has decided how new feature layouts should be composed. Your job here is to fix both halves at once — the rule, and the enforcement that keeps it followed.

## Your Role

You own the product-layer design guideline and the enforcement mechanism that gets the existing system actually followed — full ownership of both. You decide how prescriptive the rules get, which layout patterns become canon versus one-offs, and what an engineer's work (or a coding agent's output) must satisfy before it ships.

You are not expected to rewrite or redesign the existing token/component library itself within this task — you're building on top of it.

## Deliverables

Two files, each doing a different job: one sets the rules, the other proves they catch something real.

### 1. `design-system-guideline.md`

**Format:** Markdown

The product-layer design guideline (reusable layout patterns for the kinds of screens Creao builds, composed from the existing component library) plus a concrete, checkable enforcement mechanism — written so an engineer or a coding agent could load it and follow it without a follow-up question.

### 2. `compliance-audit.md`

**Format:** Markdown

A worked audit applying your guideline to the provided screens: the specific violations you find, which guideline rule each one breaks, and exactly how your enforcement mechanism would have caught it before it shipped.

## Resources

### Reference Links

| Resource | URL | Description |
| --- | --- | --- |
| CREAO live product | [agent.creao.ai](https://agent.creao.ai) | CREAO’s live product for creating and managing AI agents and automations through chat. Explore the current screens, layouts, and component usage to inform your design guidelines and compliance audit. |

## Editor's note (not part of the original brief)

The original brief mentions "provided screens" and an "upcoming feature brief", but the text provided for this task did not include separate screenshots or a feature brief; the reference resources provided are the product links above.
