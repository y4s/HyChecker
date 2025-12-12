<img width="160" height="160" alt="Group 31 (2)" src="https://github.com/user-attachments/assets/56ad96f3-1d63-4f82-a8e5-ccf501cbbcaa" />

# HyChecker
HyChecker is a Python script that allows you to check availability of multiple usernames with one click for the game [Hytale](https://hytale.com) by [Hypixel Studios](https://x.com/hypixel).

---

> **Download** the latest version of HyChecker [here](https://github.com/y4s/HyChecker/releases/tag/HyChecker).

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

> If ran correctly, the files: <i>available_names.txt</i>, <i>unavailable_names.txt</i> and <i>name_checked.txt</i> should appear

#### VSCode Folder <br>
<img width="172" height="134" alt="image" src="https://github.com/user-attachments/assets/6b605715-ca1d-4e05-97af-6fdf50bd36a4" />

#### Search Summary <br>
<img width="235" height="222" alt="image" src="https://github.com/user-attachments/assets/62c3e38e-690f-4f34-a550-b6bb5dd4a4c6" />


### 💡 Optional:
1. Run `refresh.py` to see if the names you're after are still available

> When ran, the list of names that are still available will remain in <i>available_names.txt</i>, otherwise moved to <i>unavailable_names.txt</i>

#### Refresh Summary <br>
<img width="211" height="155" alt="image" src="https://github.com/user-attachments/assets/ded92eb7-427c-44fb-9505-f7d41a5761e7" />


---

> [!TIP]
> The more names you add into your list, the longer it will take to search. This script is highly dependant on the API's ability to check for availability, and since I did NOT make the API, please use this tool with a grain of salt.

---

> [!NOTE]
> If you have any question feel free to DM me on Discord: `@yeson`

> [!IMPORTANT]
> This script was made possible due to [hytl.tools](https://hytl.tools)' public API made by [@JackGamesFTW](https://x.com/JackGamesFTW). <br>
> The logo was made by myself, using an artwork made by the artists at Hytale.

> [!CAUTION]
> This is an Unofficial tool, not affiliated with [Hytale](https://hytale.com).
