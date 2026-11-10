from io import BytesIO
from multiprocessing import Pool, cpu_count
from pikepdf import Pdf, PasswordError

# --- settings ---
FILENAME = "file.pdf"
MIN_DIGITS = 4
MAX_DIGITS = 4

# Read the file into memory once, at module level,
# so every worker process inherits it.
with open(FILENAME, "rb") as f:
    PDF_BYTES = f.read()


def try_password(pn):
    """Return the password if it matches, otherwise None."""
    try:
        with Pdf.open(BytesIO(PDF_BYTES), password=pn):
            return pn
    except PasswordError:
        return None


def crack(digits):
    n_max = 10 ** digits
    # password generator "0000", "0001", ... without keeping them all in memory
    candidates = (str(n).zfill(digits) for n in range(n_max))

    with Pool(processes=cpu_count()) as pool:
        # imap_unordered = results arrive as soon as they are ready
        for result in pool.imap_unordered(try_password, candidates, chunksize=100):
            if result is not None:
                pool.terminate()        # discard the remaining work
                return result
    return None


if __name__ == "__main__":          # REQUIRED for multiprocessing
    print("Cracking. Please wait...")
    found = None
    for digits in range(MIN_DIGITS, max(MIN_DIGITS, MAX_DIGITS) + 1):
        print(f"Trying {digits}-digit passwords on {cpu_count()} cores...")
        found = crack(digits)
        if found:
            break

    if found:
        print(f"Password is {found}")
    else:
        print("Could not crack the password")
