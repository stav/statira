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
    "proposedEffectiveDt": first_of_next_month,
    "eligibility": "medicare",
    "eligibilitySource": "broker",
    "agentName": AGENT_NAME,
    "agentTIN": AGENT_TIN,
    "idcard": "",
}


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
    print(user)
    return user


def missing_data(row):
    return not (row["MBI"] and row["First Name"] and row["Last Name"] and row["DOB"])


def make_cache_filename(row):
    fname = row["First Name"].replace(" ", "")
    lname = row["Last Name"].replace(" ", "")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"output/cache/{fname}_{lname}_{timestamp}.json"
    return filename


def make_recent_filename(row):
    fname = row["First Name"].replace(" ", "")
    lname = row["Last Name"].replace(" ", "")
    filename = f"output/recent/{fname}_{lname}.json"
    return filename


def compare_contents(response_data, recent_filename):
    recent_file_contents = None
    try:
        with open(recent_filename, "r") as f:
            recent_file_contents = json.load(f)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("Error decoding JSON from file")

    print("recent_file_contents:", type(recent_file_contents), recent_file_contents)
    if recent_file_contents:
        response_data_copy = response_data.copy()
        recent_file_contents_copy = recent_file_contents.copy()
        response_data_copy.pop("transId", None)
        recent_file_contents_copy.pop("transId", None)
        print("Same?", response_data_copy == recent_file_contents_copy)
    else:
        print("Same?", False)


async def write_response_to_file(response, row):
    response_data = await response.json()
    print("response_data:", type(response_data), response_data)

    cache_filename = make_cache_filename(row)
    recent_filename = make_recent_filename(row)

    compare_contents(response_data, recent_filename)

    print("Writing to file:", cache_filename)
    with open(cache_filename, "w") as f:
        json.dump(response_data, f, indent=4)

    print("Writing to file:", recent_filename)
    with open(recent_filename, "w") as f:
        json.dump(response_data, f, indent=4)


async def main():

    async with aiohttp.ClientSession() as session:
        with open("clients.csv", mode="r") as infile:
            for row in csv.DictReader(infile):
                print("--------------------------------")
                if missing_data(row):
                    print("Skipping row due to missing data:", row)
                    continue

                user = assemble_user_data(row)

                async with session.post(url, headers=headers, json=user) as resp:
                    print(resp.status, resp.headers["content-type"])
                    if resp.status == 200:
                        await write_response_to_file(resp, row)
                    else:
                        print("Request failed", resp.reason)


if __name__ == "__main__":
    asyncio.run(main())
