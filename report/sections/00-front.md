<div class="title-page">
<p class="uni">National University of Computer and Emerging Sciences (FAST–NUCES)</p>
<h1 class="title">Breaking PsycoSupport</h1>
<p class="subtitle">Offline deployment, loopback interception and Al-Kindi cryptanalysis of an affine-encrypted LLM support app</p>
<p class="meta">Information Security · Assignment #1 · Fall 2026</p>
<p class="meta"><strong>Muhammad Rafique</strong> · Roll No. 23i-0747</p>
<p class="meta">21 October 2026</p>
<p class="meta">Repository: <a href="https://github.com/Rafique610/psycosupport-cryptanalysis">github.com/Rafique610/psycosupport-cryptanalysis</a></p>
</div>

# Introduction

PsycoSupport is a local mental-health support tool: a patient enters a username, a mood and a concern; a
server asks a local LLM (Ollama, `llama3.2`) for supportive advice; both directions are "protected" with an
affine cipher. This report deploys the app fully offline (Task 1), intercepts its loopback traffic (Task 2),
recovers the key and decrypts every session using only the intercepted ciphertext (Task 3), and analyses the
security failures with proper alternatives (Task 4).

![Figure 0.1: Lab architecture. Everything runs on one Kali machine; the capture point is the loopback interface.](../figures/architecture.svg)

All results come from real runs on 21 October 2026 and are reproducible with the commands in the Appendix.
