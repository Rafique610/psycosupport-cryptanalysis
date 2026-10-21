# Ethical Reflection

> **To be written by the student in their own words (academic integrity).** This section is intentionally
> left as a prompt. Cover each point below in a short paragraph of your own; the facts in brackets are from
> this lab so you can refer to them accurately.

- **Scope.** Why the analysis was limited to our own PsycoSupport instance, and why attacking a system you do
  not own or have permission to test is wrong (and usually illegal).
- **Synthetic data only.** We invented five patients (`tester01`–`tester05`) and their concerns; no real
  person's mental-health information was ever used or exposed.
- **Credentials.** The upstream app's API key was ignored and never committed; nothing secret was pushed to
  the repository (the capture, memory and any `.env` files are git-ignored).
- **Tool responsibility.** Packet capture and MITM tools are dual-use. Here they ran only on the lab loopback
  interface of a machine we control; the same tools aimed at someone else's traffic would be an attack.
- **What was really at stake.** If PsycoSupport were real, this exercise shows an eavesdropper could read
  every patient's username, mood and private concern, plus the advice they received — special-category
  mental-health data. Reflect on the duty to disclose such a weakness responsibly rather than exploit it.
- **Why we did this.** The point of breaking the cipher was to understand the failure and recommend a proper
  fix (Task 4), not to defeat protection for its own sake.
