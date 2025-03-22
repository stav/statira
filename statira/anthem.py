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


async def main():

    async with aiohttp.ClientSession() as session:
        with open("clients.csv", mode="r") as infile:
            for row in csv.DictReader(infile):
                print("--------------------------------")
                if missing_data(row):
                    print("Skipping row due to missing data:", row)
                    continue

                user = assemble_user_data(row)
                async with session.post(url, headers=headers, json=user) as response:
                    print(response.status, response.headers["content-type"])
                    JSON = await response.json()
                    print("POST Response JSON:", JSON)
                    fname = row["First Name"].replace(" ", "")
                    lname = row["Last Name"].replace(" ", "")
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                    filename = f"output/{fname}_{lname}_{timestamp}.json"
                    with open(filename, "w") as f:
                        json.dump(JSON, f, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
