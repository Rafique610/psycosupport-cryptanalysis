  
National University of Computer and Emerging  
Sciences (FAST–NUCES)  
Assignment \#1  
Information Security  
Semester: Fall 2026  
Total Marks: 100   
Submission Deadline: As Per GCR  
Repository / Release: https\://github.com/maadilrehman/PsycoSupport

|  Grading Rubric \[CLO-2, CLO-3\] Objective  | Marks  | Excellent (8–10 marks)  | Good (4–7 marks)  | Poor/None (0–3 marks)  |
| :---- | :---- | :---- | :---- | :---- |
| **Ciphertext Collection & Evidence**  | **20** | ≥5 ciphertexts with clear capture evidence  | 3–4 ciphertexts; partial evidence  | \<3 ciphertexts or no evidence  |
| **Frequency Analysis**  | **40** | Accurate tables and charts; correct reasoning compared with English frequency; correct key mapping identified with clear justification  | Minor errors or incomplete reasoning; some/partial correct mappings  | No, incorrect, or unjustified analysis  |
| **Decryption Results**  | **20** | Correct decryption of 3–5 ciphertexts  | 1–2 partial decryptions  | No valid decryption  |
| **Clarity & Reflection**  | **20** | Well-structured report; input analysis and ethical reflection included  | Partial clarity and/or reflection  | Poor writing; missing reflection; plagiarism  |

 **Ethics & responsible conduct**   
1\. Scope limitation: Only analyze ciphertexts from the provided PsycoSupport instance.   
2\. No personal data: Use synthetic messages; do not submit real personal data.   
3\. API keys: Use a throwaway API key; do not share keys in submissions or commit them.   
4\. Tool responsibility: Packet capture and MITM tools can be misused, operate only on lab VMs/networks you control.   
5\. Academic integrity: Document your own work. Cite sources. No plagiarism.

**Deliverables**   
Submit a single ZIP file on GCR containing:   
• report.pdf — your main report (tasks, tables, charts, decrypted texts, reflections).   
• ciphertexts.csv — list of intercepted ciphertexts.   
• scripts/ — any Python/R scripts for analysis and plotting.   
• evidence/ — optional screenshots/pcap snippets of network captures.

**Important Notes:**

1. **Client server executable should be used for linux platform only**  
2. **For host file- give your own name**  
3. **Server.py: Do not change the functionality. The Groq file is changed to the local file.**   
4. **Ignore the API key. As the entire process is done locally** 

PsycoSupport is a secure mental health logging utility designed to run entirely within a localized environment. Patients submit their username, active mood, and emotional concerns through a client utility. The backend microservice processes these inputs securely by communicating with a local open-source Large Language Model (LLM) managed by Ollama, ensuring complete data privacy with no external cloud routing.

To replicate historical software security vulnerabilities, this application uses a classical encryption wrapper (an Affine Cipher variant) to obscure data sent over the local network loop. In this lab, you will act as a system developer and tester-cryptanalyst: deploying the offline pipeline, capturing the local transit data, and using classical cryptanalysis techniques to break the encryption layer.

The entire infrastructure runs on a single local machine or within an isolated Linux Virtual Machine (VM) using the loopback interface (127.0.0.1):

psycare\_lab/

├── server.py          \# Local HTTP server receiving traffic & calling Ollama

├── client.py          \# Terminal client encrypting and transmitting data

└── requirements.txt   \# Free Python library references (ollama, requests)

**Task 1: Offline Environment Deployment — 20**

You must configure a completely free, local pipeline that functions without an active internet connection.

• Ollama Installation: Install Ollama on your local machine or VM using the official automated script 

(curl \-fsSL https\://ollama.com | sh).

• Model Provisioning: Pull a lightweight model optimized for local consumer hardware (such as llama3.2 or phi3) to run background inference locally.

• Server Binding: Run your custom Python script (server.py) to handle incoming payload processing and manage the local LLM system prompt restrictions.

**Task 2: Local Network Traffic Interception — 20**

Because all application data passes over the local loopback adapter, you can sniff the data packets natively.

• Execute server.py and client.py concurrently on your machine.

• Open Wireshark or tcpdump and bind the packet capture exclusively to your Loopback (lo) network interface.

• Apply a port filter (e.g., tcp.port \== 5000\) to isolate the traffic.

• Deliverable: Generate five distinct test cases with varying concerns. Export the exact raw text ciphertexts passing from Client → Server and Server → Client by utilizing Wireshark's Follow TCP Stream feature.

**Task 3: Al-Kindi Classical Cryptanalysis — 40**

Modern LLM outputs exhibit highly predictable linguistic distributions (such as structured syntax, repeating punctuation layouts, and mandatory boilerplate disclaimers). You will exploit these structural patterns to break the application layer's security wrapper.

• Map out the character frequency distribution of your intercepted ciphertexts.

• Perform a Frequency Analysis (Al-Kindi Method) by cross-referencing your captured ciphertext distributions against standard English character frequencies.

• Mathematically deduce the modular multiplicative inverse to discover the Affine transformation key pair (a, b) running in the scripts.

• Deliverable: Provide full mathematical proofs showing your key recovery calculations, and supply the decrypted plaintext translations for all five captured sessions.

**Task 4: Security Engineering Analysis — 20**

Draft a technical summary explaining the security failures observed during this local exercise.

• Explain how the predictable structural behaviors of local LLMs (like repetitive disclaimer sentences) make classical substitution ciphers highly vulnerable to known-plaintext and frequency distribution attacks.

• Outline at least two industry-standard local security alternatives (such as binding the server to local UNIX domain sockets or using self-signed TLS 1.3 certificates) to properly protect inter-process communication traffic.