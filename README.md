# Fake Profile Investigator
Coded by Cyber Security Engineer Mr Sabaz Ali Khan

A local Python desktop application for comparing manually collected public-profile information and user-provided photos. Includes the requested Unicode banner, a dark interface, JSON case saving/loading, CLI mode and standalone HTML reports.

## Windows quick start
1. Install Python 3.10 or newer with Tkinter (the standard Windows installer includes it).
2. Extract the entire ZIP. Open the extracted project folder in VS Code.
3. In its terminal run:

```powershell
py -3 -m pip install -r requirements.txt
py -3 app.py
```

Alternatively run INSTALL_WINDOWS.bat once, then START_WINDOWS.bat.
If `py` is unavailable, use `python` for both commands with the same Python installation.
If Pillow is missing, install `Pillow`, not a package named `PIL`.

## Linux
Install your distribution's Python Tkinter and venv packages (on Debian/Ubuntu: `sudo apt install python3-tk python3-venv`), then:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

## Workflow / Roman Urdu
- Reference mein independently trusted account ki information paste karein.
- Candidate mein jis profile ko review karna hai uski information paste karein.
- Source URL, observation date/time aur timezone record karein. App URL se information download nahi karta.
- Dono local photos choose karein, phir Compare profiles dabayein.
- Save case se JSON file save hoti hai. Open case se dobara khol sakte hain.
- Export HTML report browser mein kholein. Browser Print > Save as PDF bhi use kar sakte hain.
- Banner & guide tab mein aapka complete banner hai.
- Example case sirf fictional demonstration hai; Open case se example_case.json kholein.

## What results mean
Text comparison uses Unicode NFKC normalization, case folding, whitespace normalization and Python SequenceMatcher character overlap. A leading @ is ignored for usernames. Missing fields produce null, not a 0% match. Scores of at least 80% trigger a text-overlap clue. These are transparent heuristic thresholds, not validated fraud probabilities. Unicode normalization does not detect every cross-alphabet lookalike.

Photo analysis reports SHA-256 for exact file equality and a 64-bit difference hash for coarse image structure (distance 0–64; lower means closer). A distance at most 8 triggers a review clue only if neither image is low-detail. Low grayscale variation produces a warning; EXIF orientation is respected. Animated images use the first frame. Different encodings of the same picture may have different SHA-256 hashes. Cropping, backgrounds, compression, colors, logos and simple images can produce misleading hash results. Manually inspect originals. Maximum accepted photo size: 25 MB / 20 megapixels.

No face recognition, identification, reverse-image web search, private-profile access or automatic platform reporting. This is an offline comparison assistant, not an automated profile scraper. Similarity does not establish fraud, identity, ownership or authenticity. A reference account is trusted only to the extent you independently verified it.

## Data and evidence
Cases and reports are unencrypted local files. Photo files are not copied or embedded; JSON stores their paths. When moving a case to another computer, transfer photos separately and reselect paths. Saving records the current inputs, not a historical result; exported reports preserve that comparison snapshot. Save before closing or opening another case. Protect sensitive notes and ask the person you are helping before sharing reports. Hashes establish byte equality, not who posted a photo or when. Generated timestamps come from the computer clock.

## Command line
```bash
python app.py --case example_case.json --report example_report.html
python -m unittest discover -s tests -v
```

Files: app.py (GUI/CLI), core.py (comparison, case validation, report rendering), banner.txt, requirements.txt, example_case.json, tests/, Windows launchers.



⠀⠀⢀⣠⣴⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⢸⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀
⠀⣿⡿⣿⡟⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠛⢻⣿⣿⠀
⠀⣿⡿⠋⠉⠑⠒⠤⣉⠻⢿⣿⣿⡿⠋⠀⠀⠀⠁⠐⠳⢹⡇
⠀⣿⣷⣶⣦⣄⡀⠀⠀⠉⠺⡿⠿⠃⠀⠀⠀⣠⣴⣶⣶⣾⡇
⠀⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⣴⣇⠀⠀⣰⡿⠿⠿⢿⣿⢛⡇
⠀⣡⡌⠁⠀⠀⠀⠈⠉⠀⠈⣿⣷⠀⠀⠁⠀⠀⠀⠀⣠⣌⣿
⠀⢿⣿⣿⣶⣦⣴⣶⣾⣰⠄⣿⣿⠠⣸⣶⣶⣶⣶⣿⣿⣿⡇
⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⠃⣿⣿⠐⣿⢿⣿⣿⣟⣋⣠⡔⠀
⠀⠸⡀⠉⠉⣉⣍⣭⠹⢿⠁⣿⣿⡇⠿⠆⣭⣉⡉⠉⡁⢰⠀
⠀⠀⢷⡀⢀⠈⠻⠿⠶⠄⠀⠈⠉⠀⠠⠾⠿⠟⠁⠐⢠⠇⠀
⠀⠀⠈⢷⡀⠐⢤⣤⣀⡀⠀⠴⠷⠄⠀⣠⣤⡤⠌⠠⠋⠀⠀
⠀⠀⠀⠀⠱⣷⡄⢦⣍⣙⠛⠒⠒⠒⣉⣩⣤⠆⢔⠃⠀⠀⠀
⠀⠀⠀⠀⡀⠈⠛⣆⢻⣿⡇⠀⡄⠸⣿⡿⠣⡎⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣇⠀⠀⠈⠻⣿⣇⠀⠀⢸⣿⡤⠋⠀⢀⡆⠀⠀⠀
⠀⠀⠀⢘⣿⣦⣀⠀⠀⠈⠙⠀⠀⠟⠉⠀⠀⣠⣾⡿⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⣀⣴⣿⣿⣿⡏⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠗⠀⠀⠺⣿⣿⣿⣿⣿⠃⠀⠀⠀
⠀⠀⠀⠀⠈⣿⣿⣿⡟⠁⠀⠀⠀⠀⠈⢿⣿⣿⡿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⣿⠟⢠⣦⠀⠀⠀⠀⣴⡄⠻⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢡⡌⣰⣿⣿⡇⠀⠀⢸⣿⣧⣆⢁⠆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⣿⣿⡟⠀⠀⠀⠀⢻⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⣿⣿⠁⠀⠀⠀⠀⠈⣿⣿⡏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣿⣟⠀⠀⠀⠀⠀⠀⣿⣿⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠸⡇⠀⠀⠀⠀⠀⠀⢹⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀𝓒𝓸𝓭𝓮𝓭 𝓑𝔂 𝓬𝔂𝓫𝓮𝓻 𝓢𝓮𝓬𝓾𝓻𝓲𝓽𝔂 𝓔𝓷𝓰𝓲𝓷𝓮𝓮𝓻 𝓜𝓻 𝓢𝓪𝓫𝓪𝔃 𝓐𝓵𝓲 𝓴𝓱𝓪𝓷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀
