"""
This module provides functionality to check Medicare and Medicaid eligibility
for users via the Anthem API. It reads user data from a CSV file, formats the
data, sends it to the API, and handles the response.

If a Medicaid ID or an SSN is provided, it checks for DSNP eligibility.
If only a Medicare ID is provided, it checks for Medicare eligibility.

User interface: https://mproducer.anthem.com/mproducer/dsnpeligibilitycheck

Functions:
    missing_data(row): Checks if any required data is missing in the given row.
    make_cache_filename(row): Generates a filename for caching the response data.
    make_noneqiv_filename(row): Generates a filename for storing non-equivalent response data.
    make_recent_filename(row): Generates a filename for storing the most recent response data.
    compare_contents(response_data, recent_filename, noneqiv_filename): Compares the response data with the recent file contents and writes to a non-equivalent file if they differ.
    write_response_to_file(response_data, row): Writes the API response data to cache, recent, and non-equivalent files.
    assemble_user_data(row): Assembles user data from the CSV row into the required format for the API request.
    send(session, row): Sends the user data to the API and handles the response.
    get_csv(content): Reads CSV content from a string or a file and returns a StringIO object.
    start(content): Uploads the CSV file, processes the content row by row, sends data to the API, and yields results.
    main(content): Main function to run start as a script.
"""

import csv
import json
import aiohttp
import asyncio

from io import StringIO
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
    return not (
        row.get("MBI")
        and row.get("First Name")
        and row.get("Last Name")
        and row.get("DOB")
    )


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

    if recent_file_contents:
        # Make copies so we can remove unneeded entries
        response_data_copy = response_data.copy()
        recent_file_contents_copy = recent_file_contents.copy()
        # Remove unneeded keys that change often
        for key in ["transId", "medicaidServiceDt"]:  # Keys to remove
            response_data_copy.pop(key, None)
            recent_file_contents_copy.pop(key, None)
        # Determine equivalence
        contents_equivalent = response_data_copy == recent_file_contents_copy

    if not contents_equivalent:
        print("Writing to non-equivalent file:", noneqiv_filename)
        with open(noneqiv_filename, "w") as f:
            json.dump(recent_file_contents, f, indent=4)


async def write_response_to_file(response_data, row):
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
    response_data: str = None

    async with session.post(url, headers=headers, json=user) as resp:
        print(resp.status, resp.headers["content-type"])
        if resp.status == 200:
            response_data = await resp.json()
            await write_response_to_file(response_data, row)
        else:
            print("Request failed", resp.reason)

    return user, response_data


def get_csv(content: str):
    if content is None:
        with open("clients.csv", mode="r") as infile:
            content = infile.read()

    return StringIO(content)


async def start(content: str = None):
    async with aiohttp.ClientSession() as session:
        p = r = 0

        for row in csv.DictReader(get_csv(content)):
            r += 1
            if missing_data(row):
                message = f"Skipping row due to missing data: {row}"
                yield dict(message=message, user={}, data={})
            else:
                user, data = await send(session, row)
                yield dict(user=user, data=data)
                p += 1

    message = f"Read {r} row{'' if r == 1 else 's'},  Processed: {p}"
    yield dict(message=message, user={}, data={})


async def main():
    return [m async for m in start()]


if __name__ == "__main__":
    asyncio.run(main())
