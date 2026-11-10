# PDF Password Brute Forcer

A small, multiprocessing-based Python script that recovers a numeric password of a
password-protected PDF by trying every combination of digits in a given range.

## How it works

- The PDF is read into memory once at module level so every worker process inherits it.
- A generator produces candidate passwords (`"0000"`, `"0001"`, …) without holding
  them all in memory.
- As soon as a password matches, the remaining work is discarded and the password is
  printed.

## Requirements

- Python 3.8+
- [pikepdf](https://pikepdf.readthedocs.io/)

```bash
pip install pikepdf
```

## Usage

1. Place the password-protected PDF next to the script.
2. Adjust the settings at the top of `opener.py`:

   ```python
   FILENAME = "file.pdf"   # the PDF to crack
   MIN_DIGITS = 4          # shortest password length to try
   MAX_DIGITS = 4          # longest password length to try
   ```

3. Run it:

   ```bash
   python opener.py
   ```

Example output:

```
Cracking. Please wait...
Trying 4-digit passwords on 8 cores...
Password is 1234
```

## Notes

- Only **numeric** passwords are supported (digits `0`–`9`).
- The search space grows by a factor of 10 for each extra digit, so longer passwords
  take dramatically longer to crack.
- Performance scales with the number of CPU cores available on your machine.
