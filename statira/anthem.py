import csv
import json
import aiohttp
import asyncio

from datetime import datetime, timedelta

from config import BEARER_TOKEN, AGENT_NAME, AGENT_TIN


url = "https://mproducer.anthem.com/mproducer/accessgateway/geteligibility"
headers = {
    "Accept": "application/json, text/plain",
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json",
    "Origin": "https://mproducer.anthem.com",
    "Referer": "https://mproducer.anthem.com/mproducer/dsnpeligibilitycheck",
}
# Calculate the first of next month
today = datetime.today()
next_month = today.replace(day=1) + timedelta(days=32)
first_of_next_month = next_month.replace(day=1).strftime("%Y-%m-%d")

data = {
    # "firstName": "JOHN",
    # "lastName": "SMITH",
    # "dob": "1950-01-01",
    # "medicareId": "1XV9WC5XP29",
    # "eligibility": "medicare|dsnp",
    # "medicaidId": "",
    # "state": "OH",
    # "ssn": "",
    "proposedEffectiveDt": first_of_next_month,
    "eligibilitySource": "broker",
    "agentName": AGENT_NAME,
    "agentTIN": AGENT_TIN,
    "idcard": "",
}


def missing_data(row):
    return not (row["MBI"] and row["First Name"] and row["Last Name"] and row["DOB"])


def make_cache_filename(row):
    fname = row["First Name"].replace(" ", "")
    lname = row["Last Name"].replace(" ", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"output/cache/{fname}_{lname}_{timestamp}.json"
    return filename


def make_noneqiv_filename(row):
    fname = row["First Name"].replace(" ", "")
    lname = row["Last Name"].replace(" ", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"output/change/{fname}_{lname}_{timestamp}.json"
    return filename


def make_recent_filename(row):
    fname = row["First Name"].replace(" ", "")
    lname = row["Last Name"].replace(" ", "")
    filename = f"output/recent/{fname}_{lname}.json"
    return filename


def compare_contents(response_data, recent_filename, noneqiv_filename):
    recent_file_contents = None
    try:
        with open(recent_filename, "r") as f:
            recent_file_contents = json.load(f)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Error decoding JSON from file")

    contents_equivalent = None

    print("recent_file_contents:", type(recent_file_contents), recent_file_contents)
    if recent_file_contents:
        response_data_copy = response_data.copy()
        recent_file_contents_copy = recent_file_contents.copy()
        response_data_copy.pop("transId", None)
        recent_file_contents_copy.pop("transId", None)
        contents_equivalent = response_data_copy == recent_file_contents_copy

    if not contents_equivalent:
        print("Writing to non-equivalent file:", noneqiv_filename)
        with open(noneqiv_filename, "w") as f:
            json.dump(recent_file_contents, f, indent=4)


async def write_response_to_file(response, row):
    response_data = await response.json()
    print("response_data:", type(response_data), response_data)

    cache_filename = make_cache_filename(row)
    recent_filename = make_recent_filename(row)
    noneqiv_filename = make_noneqiv_filename(row)

    compare_contents(response_data, recent_filename, noneqiv_filename)

    print("Writing to file:", cache_filename)
    with open(cache_filename, "w") as f:
        json.dump(response_data, f, indent=4)

    print("Writing to file:", recent_filename)
    with open(recent_filename, "w") as f:
        json.dump(response_data, f, indent=4)


def assemble_user_data(row):
    dob = datetime.strptime(row["DOB"], "%m/%d/%Y").strftime("%Y-%m-%d")
    user = data.copy()
    user.update(
        {
            "firstName": row["First Name"].strip().upper().strip(),
            "lastName": row["Last Name"].strip().upper().strip(),
            "medicareId": row["MBI"].replace("-", "").strip(),
            "dob": dob,
        }
    )
    if row.get("Medicaid"):
        user["medicaidId"] = row["Medicaid"].strip()
        user["eligibility"] = "dsnp"
        user["state"] = "OH"
    elif row.get("SSN"):
        user["ssn"] = row["SSN"].strip().replace("-", "")
        user["eligibility"] = "dsnp"
        user["medicaidId"] = ""
        user["state"] = "OH"
    else:
        user["eligibility"] = "medicare"

    print(user)

    return user


async def send(session, row):
    user = assemble_user_data(row)

    async with session.post(url, headers=headers, json=user) as resp:
        print(resp.status, resp.headers["content-type"])
        if resp.status == 200:
            await write_response_to_file(resp, row)
        else:
            print("Request failed", resp.reason)


async def main():
    async with aiohttp.ClientSession() as session:
        with open("clients.csv", mode="r") as infile:
            for row in csv.DictReader(infile):
                print("--------------------------------")
                if missing_data(row):
                    print("Skipping row due to missing data:", row)
                else:
                    await send(session, row)


if __name__ == "__main__":
    asyncio.run(main())
