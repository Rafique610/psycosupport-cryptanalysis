## 3.3 Decrypting all five sessions

With the recovered key (a, b) = (17, 8), every ciphertext is decrypted with D(y) = 23·(y − 8) mod 26.
`task decrypt` (`scripts/cipher/decrypt_all.py`) processes all 20 rows of `ciphertexts.csv` and writes
`report/figures/decrypted.csv` (case_id, direction, field, ciphertext, plaintext). JSON escapes are undone
before decrypting, so the `n` of an escaped newline is never treated as a cipher letter.

### 3.3.1 Verification against ground truth

Two independent references exist for every row:

- **Client→Server:** the original inputs in `scripts/capture/test_cases.csv`. Each decrypted field must be identical.
- **Server→Client:** the reply the real PsycoSupport client printed during the capture
  (`evidence/task2/client_runs.txt`). Each decrypted reply must appear there character for character.

```
$ task decrypt
case 1: client_to_server PASS (vs test_cases.csv) | server_to_client PASS (vs client output in client_runs.txt)
case 2: client_to_server PASS (vs test_cases.csv) | server_to_client PASS (vs client output in client_runs.txt)
case 3: client_to_server PASS (vs test_cases.csv) | server_to_client PASS (vs client output in client_runs.txt)
case 4: client_to_server PASS (vs test_cases.csv) | server_to_client PASS (vs client output in client_runs.txt)
case 5: client_to_server PASS (vs test_cases.csv) | server_to_client PASS (vs client output in client_runs.txt)
identical disclaimer ciphertext in 5/5 replies
wrote 20 rows to report/figures/decrypted.csv
```

**Result: 20/20 ciphertexts decrypted correctly: 5/5 sessions in both directions.**

### 3.3.2 Session by session

#### Session 1: exam stress (stream 0) · PASS

| Direction | Field | Ciphertext | Plaintext |
| --- | --- | --- | --- |
| Client→Server | username | `tyctyl01` | tester01 |
| Client→Server | mood | `ivjomkc` | anxious |
| Client→Server | concern | `O xiby txlyy povin yjiec vyjt syyw ivh ybyla toey O cot hmsv…` | I have three final exams next week and every time I sit down to study my heart starts racing and I cannot focus on anything for more than a few minutes. I am worried that I will fail and disappoint my family. |
| Server→Client | reply | `Ot cmkvhc nowy amk'ly pyynovg i nmt mp dlycckly ivh ivjoyta …` | (full text below) |

Decrypted reply:

> It sounds like you're feeling a lot of pressure and anxiety about your exams. It's normal to feel this way, especially when there's a lot at stake. Here are a few things that might help:
>
> Try taking short breaks every 20-30 minutes to stretch, move around, and do something that relaxes you. Deep breathing exercises can also help calm your nerves. Consider making a study plan and breaking it down into smaller, manageable chunks. This can help you feel more in control and focused.
>
> Also, remind yourself that it's okay to make mistakes - it's a learning experience, and your family loves and supports you regardless of the outcome.
>
> This is not a substitute for professional help. If you are in crisis, please contact your local emergency services.

#### Session 2: poor sleep (stream 1) · PASS

| Direction | Field | Ciphertext | Plaintext |
| --- | --- | --- | --- |
| Client→Server | username | `tyctyl02` | tester02 |
| Client→Server | mood | `yjxikctyh` | exhausted |
| Client→Server | concern | `O xiby vmt zyyv cnyydovg synn pml izmkt i emvtx. O noy isiwy…` | I have not been sleeping well for about a month. I lie awake until three in the morning thinking about everything that could go wrong and then I feel tired and irritable the whole day. |
| Server→Client | reply | `Tyctyl02, ot cmkvhc nowy amk'ly ctlkggnovg sotx ovcmevoi ivh…` | (full text below) |

Decrypted reply:

> Tester02, it sounds like you're struggling with insomnia and racing thoughts. This can be really tough to deal with. Try to focus on relaxation techniques, like deep breathing, progressive muscle relaxation, or guided imagery. You can find these online or through a meditation app. Additionally, establish a consistent sleep schedule, create a calming bedtime routine, and make your sleep environment comfortable, dark, quiet, and cool. Consider keeping a thought journal to write down your worries before bed, and see if that helps clear your mind. Remember, it's okay to take breaks and practice self-care during the day.
>
> This is not a substitute for professional help. If you are in crisis, please contact your local emergency services.

#### Session 3: loneliness (stream 2) · PASS

| Direction | Field | Ciphertext | Plaintext |
| --- | --- | --- | --- |
| Client→Server | username | `tyctyl03` | tester03 |
| Client→Server | mood | `nmvyna` | lonely |
| Client→Server | concern | `O embyh tm i vys qota pml kvobylcota ivh O hm vmt wvms ivamv…` | I moved to a new city for university and I do not know anyone here. Everyone else seems to already have friends and I spend most evenings alone in my room. |
| Server→Client | reply | `Ot qiv zy lyinna tmkgx tm ihfkct tm i vys dniqy ivh pyyn now…` | (full text below) |

Decrypted reply:

> It can be really tough to adjust to a new place and feel like you're missing out on social connections. First, know that it's normal to take some time to build new relationships, especially in a new city. Here are some suggestions to help you feel more connected:
>
> * Try joining a club or group that aligns with your interests at university. This way, you can meet people who share similar passions.
> * Attend campus events and gatherings, such as cultural festivals, concerts, or sports events. These can be great opportunities to meet new people.
> * Consider reaching out to your university's student union or counseling center for support and resources to connect with others.
>
> This is not a substitute for professional help. If you are in crisis, please contact your local emergency services.

#### Session 4: work pressure (stream 3) · PASS

| Direction | Field | Ciphertext | Plaintext |
| --- | --- | --- | --- |
| Client→Server | username | `tyctyl04` | tester04 |
| Client→Server | mood | `mbylsxyneyh` | overwhelmed |
| Client→Server | concern | `Ea eivigyl wyydc ihhovg vys hyihnovyc ivh O ie smlwovg nity …` | My manager keeps adding new deadlines and I am working late almost every night. I feel like I can never catch up and I have started to dread opening my email in the morning. |
| Server→Client | reply | `Ot cmkvhc nowy amk'ly pyynovg ctkqw ivh plkctlityh sotx amkl…` | (full text below) |

Decrypted reply:

> It sounds like you're feeling stuck and frustrated with your workload. It's normal to feel that way, especially when faced with a never-ending list of tasks and tight deadlines. Take a step back and assess what you can control. Prioritize your tasks, focusing on the most important ones first. Consider communicating with your manager about your workload and see if there's a way to adjust the deadlines or distribute tasks more evenly. Also, try to establish a healthy work-life balance by setting boundaries, such as not checking work emails during non-work hours.
>
> This is not a substitute for professional help. If you are in crisis, please contact your local emergency services.

#### Session 5: low motivation (stream 4) · PASS

| Direction | Field | Ciphertext | Plaintext |
| --- | --- | --- | --- |
| Client→Server | username | `tyctyl05` | tester05 |
| Client→Server | mood | `kvemtobityh` | unmotivated |
| Client→Server | concern | `O kcyh tm yvfma diovtovg ivh gmovg pml sinwc zkt nityna vmtx…` | I used to enjoy painting and going for walks but lately nothing feels interesting. I keep putting off simple tasks and I do not know how to get my energy back. |
| Server→Client | reply | `Ot cmkvhc nowy amk'ly pyynovg ctkqw ivh hocqmvvyqtyh plme iq…` | (full text below) |

Decrypted reply:

> It sounds like you're feeling stuck and disconnected from activities that used to bring you joy. It's normal to go through periods where motivation and energy seem to fade. One thing you can try is to take small, gentle steps towards your interests. For painting, start by setting up your space and picking up a brush again, even if it's just for a few minutes a day. Similarly, for walks, try to get outside and take a short walk around the block. Don't put pressure on yourself to do too much, just let yourself start small.
>
> This is not a substitute for professional help. If you are in crisis, please contact your local emergency services.

### 3.3.3 Identical plaintext, identical ciphertext

The cipher has no initialisation vector, nonce or per-message randomness: the same plaintext always produces
the same ciphertext, in every session.

| Plaintext | Sessions | Ciphertext (the same every time) |
| --- | --- | --- |
| *It sounds like you're feeling* | 1, 4, 5 | `Ot cmkvhc nowy amk'ly pyynovg` |
| *It's normal to* | 1, 4, 5 | `Ot'c vmlein tm` |
| *This is not a substitute for professional help.* | 1, 2, 3, 4, 5 | `Txoc oc vmt i ckzctotkty pml dlmpyccomvin xynd.` |

An eavesdropper does not even need the key to learn something: spotting the same ciphertext opener in
several sessions already reveals that the replies start the same way, and the fixed 118-character
disclaimer marks exactly where each reply ends. Combined with the key, all 20 intercepted messages,
including each patient's username, mood and private concern, are fully readable.
