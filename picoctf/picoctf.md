# [Challenge Name]

- **Event:** picoCTF
- **Category:** []
- **Difficulty:** []
- **Target / Instance:** `http://...` or `nc ...`

---

## Challenge Description

> Paste the exact picoCTF challenge description here so you still have the context even after the instance expires.

- **Provided Files / Credentials:** `username` / `file.zip`
- **Hint 1:** _(Optional - paste hint if used)_
- **Hint 2:** _(Optional - paste hint if used)_

---

## 1. Reconnaissance

Describe the very first things you checked (e.g., viewing page source with `Ctrl+U`, inspecting network traffic in DevTools, or checking file types).

![Initial Recon Screenshot](images/recon-screenshot.png)

### Key Findings

- Finding 1 (e.g., Found a hidden comment or encoded string in the HTML source)
- Finding 2 (e.g., Identified an interesting endpoint or script)

```html
<!-- Paste relevant source code, comments, or encoded strings here -->
```

---

## 2. Vulnerability Analysis

Explain how the application or challenge logic works behind the scenes and what makes it vulnerable.

```javascript
// Paste the specific function, script, or request header that reveals how to beat the challenge
```

### Troubleshooting / Initial Attempts

- **Attempt 1:** Tried sending `[command/input]` -> Failed because `[reason, e.g., wrong HTTP method or missing header]`.
- **Takeaway:** Realized the server expects `[specific format, endpoint, or payload]`.

---

## 3. Exploitation

Walk through the exact steps or commands used to exploit the vulnerability and retrieve the flag.

1. Step one (e.g., Decode the string using ROT13 / CyberChef)
2. Step two (e.g., Send a crafted `POST` request to `/login` with the custom header)

```bash
# Paste the exact working terminal command or exploit script here
curl -X POST \
  -H "Custom-Header: value" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}' \
  http://target-url:port/endpoint
```

### Server Response

```json
{
  "success": true,
  "flag": "picoCTF{example_flag_here}"
}
```

![Exploit Output Screenshot](images/exploit-screenshot.png)

---

## 4. Flag & Takeaways

**Flag:**

```text
picoCTF{example_flag_here}
```

### Key Takeaways & Tools Used

- **Tools:** `curl`, Firefox DevTools, CyberChef
- **What I Learned:**
  - Quick note on a new command flag, tool trick, or vulnerability concept you learned from this challenge so you can reference it in future CTFs.

