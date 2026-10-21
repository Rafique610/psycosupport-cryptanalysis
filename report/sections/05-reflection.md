# Ethical Reflection

## 1. Scope — only our own instance

All traffic capture and testing were performed exclusively on the PsycoSupport instance running on my own
machine, in accordance with the lab brief, and were limited to that instance and its loopback traffic.
Performing the same activities on systems I do not own or have explicit permission to test would be unethical
and potentially illegal. Respecting the defined scope is essential to responsible security testing.

## 2. Synthetic data only

The five patients, named `tester01` to `tester05`, and all of their mental-health concerns were fictional,
created specifically for this lab. No real person's name, mood or private concern was entered, captured or
decrypted during the experiment. This mattered especially here because mental-health information is highly
sensitive and could cause harm or violate privacy if exposed; synthetic data let me demonstrate the
vulnerability without compromising anyone.

## 3. Responsible credential handling

The upstream application's API key was deliberately ignored and never used, because the entire setup ran
locally through Ollama. No secrets were committed to the GitHub repository: the capture files, the `.memory`
folder and any `.env` files were excluded with Git ignore rules. Real API keys, passwords and other
credentials should never be committed to a public or shared repository, and proper secret management is an
essential part of secure development.

## 4. Responsibility when using security tools

Packet-analysis and traffic-capture tools such as Wireshark, tcpdump and dumpcap are dual-use technologies
that can support both legitimate security research and harmful activity. In this lab they were used only on
the loopback interface of a machine under my control. Although the techniques showed how a weak encryption
scheme could be broken, applying them to another person's traffic without authorization could seriously
compromise their privacy and security. Learning these tools therefore demands not only technical skill but
also ethical judgement and respect for authorization boundaries.

## 5. What was really at stake

The experiment demonstrated that the application's weak encryption could be broken in approximately 0.14
seconds, allowing an eavesdropper on the same machine to read patient usernames, moods, private concerns and
the advice returned by the application. In a real deployment this would expose highly sensitive health
information and undermine users' trust in the service, and such information may receive special-category
protection under applicable data-protection laws. If a weakness like this were discovered in a real system,
it should be documented and reported responsibly rather than exploited to access private information.

## 6. Why we conducted the experiment

The purpose of this lab was to understand how the encryption mechanism failed and to identify appropriate
ways to improve security, not to defeat protection for its own sake. The fixes proposed in Task 4 — a UNIX
domain socket, or TLS 1.3 where appropriate — show concrete ways to protect the communication, and the right
choice depends on the deployment architecture and security requirements. Understanding how security controls
fail is what lets developers design, implement and verify stronger protections.
