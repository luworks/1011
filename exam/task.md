Policy-Grounded Agent Workflow Prototype
Cresta logo
Cresta
Due
Oct 11, 3:30 PM PDT
Build a runnable agent workflow prototype that applies the right layered policy and refuses to guess when the knowledge base doesn't cover a question.

Context
A Cresta enterprise customer on Agentic Assist has flagged two incidents from the same week: one customer conversation where the agent workflow quoted a general refund limit instead of a narrower service-outage credit exception that actually applied, and a second where it answered a billing question the knowledge base never actually covered. Both responses reached the customer before anyone reviewed them.

A product lead on the Agentic Assist team wants a focused prototype proving the next workflow version would not repeat either failure, against a provided billing-dispute policy set and knowledge-base excerpt, before committing further engineering time to a full rebuild.

Your Role
You are the Senior Machine Learning Engineer on the Agentic Assist initiative within Product, architecting the multi-step agent workflows that combine real-time guidance, knowledge retrieval, reasoning, and automated actions for live customer conversations.

You own how the workflow retrieves evidence, applies policy, and decides when to answer versus escalate; the product lead owns which policies and conversation scenarios matter, not how the workflow is built.

Deliverables
Submit `policy-grounded-agent-prototype.zip`.

Must include:

• agent_prototype.zip: a runnable project archive, with a run script or README at the root; A working agent workflow that takes the provided billing-dispute policy set and knowledge-base excerpt, handles the provided multi-turn customer conversation, applies the policy layer that actually governs each question (including the narrow exception), and explicitly declines or escalates rather than answering when the retrieved evidence does not support a response. A reviewer can run it against the provided conversation and see, per turn, which policy and which retrieved article drove each reply.

• design_memo.md: a one-page Markdown memo; States which of the workflow's replies are fully grounded in the provided evidence versus not, identifies the point in the policy hierarchy that was hardest to enforce correctly, and sketches a concrete next step for measuring instruction-adherence and hallucination rate on this workflow going forward.

