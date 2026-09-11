import requests
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

BASES = [
    #mc3000
    "https://www.skyrc.com/download/",
    "https://www.skyrc.com/help/download/charger/mc3000/",

    #b6mini
    "https://www.skyrc.com/help/download/charger/B6mini/",
    "https://www.skyrc.com/help/download/charger/B6mini/firmware/",
    "https://www.skyrc.com/help/download/charger/Calibration/",
]

FILES = [
    #mc3000
    "MC3000_Firmware_Upgrade_V1.11.rar",
    "MC3000_Firmware_Update_V1_12.rar",
    "MC3000_Firmware_Update_V1.13.rar",
    "MC3000_Firmware_Update_V1.14.rar",
    "MC3000_Firmware_Update_V1.15_windows.zip",
    "MC3000_Firmware_Update_V1.15_MacOS.zip",

    #b6mini
    "B6mini_Firmware_Update_V1.19.zip",
    "B6mini_Upgrade_V1.14_Add_Calibration.rar",
    "B6mini_V1_13.rar",
    "B6mini_Firmware_Update_V1.20.zip",
]

# dodatkowe warianty nazw
for v in range(1, 30):
    FILES += [
        #mc3000
        f"MC3000_Firmware_Update_V1.{v:02d}.zip",
        f"MC3000_Firmware_Update_V1.{v:02d}.rar",
        f"MC3000_Firmware_Upgrade_V1.{v:02d}.zip",
        f"MC3000_Firmware_Upgrade_V1.{v:02d}.rar",

        f"MC3000_Firmware_Update_V1_{v:02d}.zip",
        f"MC3000_Firmware_Update_V1_{v:02d}.rar",
        f"MC3000_Firmware_Upgrade_V1_{v:02d}.zip",
        f"MC3000_Firmware_Upgrade_V1_{v:02d}.rar",

        f"MC3000_Firmware_Update__V1.{v:02d}.zip",
        f"MC3000_Firmware_Update__V1.{v:02d}.rar",
        f"MC3000_Firmware_Upgrade__V1.{v:02d}.zip",
        f"MC3000_Firmware_Upgrade__V1.{v:02d}.rar",

        f"MC3000_Firmware_Update__V1_{v:02d}.zip",
        f"MC3000_Firmware_Update__V1_{v:02d}.rar",
        f"MC3000_Firmware_Upgrade__V1_{v:02d}.zip",
        f"MC3000_Firmware_Upgrade__V1_{v:02d}.rar",

        ##b6mini
        f"B6mini_Upgrade_V1.{v:02d}_Add_Calibration.rar",
        f"B6mini_Upgrade_V1.{v:02d}_Add_Calibration.zip",
        f"B6mini_Upgrade__V1.{v:02d}_Add_Calibration.rar",
        f"B6mini_Upgrade__V1.{v:02d}_Add_Calibration.zip",
        f"B6mini_Upgrade_V1_{v:02d}_Add_Calibration.rar",
        f"B6mini_Upgrade_V1_{v:02d}_Add_Calibration.zip",
        f"B6mini_Upgrade__V1_{v:02d}_Add_Calibration.rar",
        f"B6mini_Upgrade__V1_{v:02d}_Add_Calibration.zip",

        f"B6mini_Firmware_Update_V1.{v:02d}.rar",
        f"B6mini_Firmware_Update_V1.{v:02d}.zip",
        f"B6mini_Firmware_Update__V1.{v:02d}.rar",
        f"B6mini_Firmware_Update__V1.{v:02d}.zip",
        f"B6mini_Firmware_Update_V1_{v:02d}.rar",
        f"B6mini_Firmware_Update_V1_{v:02d}.zip",
        f"B6mini_Firmware_Update__V1_{v:02d}.rar",
        f"B6mini_Firmware_Update__V1_{v:02d}.zip",

        f"B6mini_V1.{v:02d}.rar",
        f"B6mini_V1.{v:02d}.zip",
        f"B6mini__V1.{v:02d}.rar",
        f"B6mini__V1.{v:02d}.zip",
        f"B6mini_V1_{v:02d}.rar",
        f"B6mini_V1_{v:02d}.zip",
        f"B6mini__V1_{v:02d}.rar",
        f"B6mini__V1_{v:02d}.zip",
    ]

FILES = sorted(set(FILES))


def check(url):
    try:
        r = requests.get(
            url,
            stream=True,
            allow_redirects=True,
            timeout=15
        )

        return {
            "url": url,
            "status": r.status_code,
            "final_url": r.url,
            "type": r.headers.get("Content-Type", ""),
            "size": r.headers.get("Content-Length", "")
        }

    except Exception as e:
        return {
            "url": url,
            "status": "ERROR",
            "final_url": "",
            "type": "",
            "size": str(e)
        }


urls = [
    base + filename
    for base in BASES
    for filename in FILES
]


results = []

with ThreadPoolExecutor(max_workers=10) as executor:

    jobs = [executor.submit(check, url) for url in urls]

    for job in as_completed(jobs):

        result = job.result()

        if result["status"] == 200:
            print(
                "[FOUND]",
                result["url"],
                result["type"],
                result["size"]
            )

        results.append(result)


with open("skyrc_files.csv", "w",
          newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "url",
            "status",
            "final_url",
            "type",
            "size"
        ]
    )

    writer.writeheader()
    writer.writerows(results)


print()
print("Gotowe: skyrc_files.csv")
