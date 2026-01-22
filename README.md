<img width="160" height="160" alt="HyChecker Logo" src="https://github.com/user-attachments/assets/56ad96f3-1d63-4f82-a8e5-ccf501cbbcaa" />

# HyChecker
HyChecker is a Python script that allows you to check availability of multiple usernames with one click for the game [Hytale](https://hytale.com) by [Hypixel Studios](https://x.com/hypixel).

---

> **Download** the latest version of HyChecker [here](https://github.com/y4s/HyChecker/releases/tag/HyCheckerV2).

---

> [!WARNING]
> Dependencies Required:
> 1. [VSCode](https://code.visualstudio.com/) & [Python](https://www.python.org/downloads/)
> 2. Python's Requests Module <br>

#### ⬇️ Windows Terminal Installation for Python's Requests Module
<i>Open the terminal, copy & enter the following:</i>
```
pip install requests
```
```
pip3 install requests 
```
```
python -m pip install requests
```
---

### 🔍 How To Use:
1. Create a new folder 
2. Place `hychecker.py`, `name.txt` & `refresh.py` in the new folder you created
3. Open the folder you created in **VSCode**, your folder should contain: `hychecker.py`, `name.txt` & `refresh.py` 
4. Modify `name.txt` by entering the usernames you're after & save the file <i>(examples are given within the file itself)</i>
5. Run `hychecker.py`

> If ran correctly, the files: <i>available_names.txt</i>, <i>unavailable_names.txt</i>, <i>reserved_names.txt</i> and <i>name_checked.txt</i> should appear

#### VSCode Folder <br>
<img width="132" height="112" alt="image" src="https://github.com/user-attachments/assets/7f159f96-86a7-410d-b0e0-d91f1f6c5c37" />

#### Search Summary <br>
<img width="228" height="118" alt="image" src="https://github.com/user-attachments/assets/e6396b0b-f79f-4f75-a4bb-0acf5f8b99f7" />


### 💡 Optional:
- Run `refresh.py` to see if the names you're after are still available

> When ran, the list of names that are still available will remain in <i>available_names.txt</i>, otherwise moved to <i>unavailable_names.txt</i>. When reserved names become availabe, it will be moved from <i>reserved_names.txt</i> to <i>available_names.txt</i>

#### Refresh Summary <br>
<img width="340" height="273" alt="image" src="https://github.com/user-attachments/assets/bc872e27-74ad-4ff2-9dd0-35c3fb927e08" />


---

> [!TIP]
> The more names you add into your list, the longer it will take to search. This script is highly dependant on the API's ability to check for availability, and since I did NOT make the API, please use this tool with a grain of salt.

---

> [!NOTE]
> If you have any question feel free to DM me on Discord: `@yeson`

> [!IMPORTANT]
> - This script was made possible due to [hytl.tools](https://hytl.tools)' public API made by [@JackGamesFTW](https://x.com/JackGamesFTW). <br>
> - The logo was made by myself, using an artwork designed by the artists at Hytale.

> [!CAUTION]
> This is an Unofficial tool, not affiliated with [Hytale](https://hytale.com).
