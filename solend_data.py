import json
from solana.rpc.api import Client
from solana.publickey import PublicKey


def get_data(update_freq):
    client = Client("https://ssc-dao.genesysgo.net")
    solend_program = PublicKey("So1endDq2YkqhipRh3WViPa8hdiSpxWy6z3Z6tMCpAo")
    account_data = client.get_program_accounts(solend_program, encoding="base64")
    data = [i for i in account_data["result"]]
    solend_accounts = [i["pubkey"] for i in data]
    cnt = 0
    accounts = []
    for i in solend_accounts:
        try:
            signature = client.get_confirmed_signature_for_address2(i)["result"][-1][
                "signature"
            ]
            tx = client.get_transaction(signature)
            signer = tx["result"]["transaction"]["message"]["accountKeys"][0]
            accounts.append(signer)
            cnt += 1
            print(cnt)
            if cnt % update_freq == 0:
                with open("accounts.json", "r") as f:
                    obj = json.load(f)
                    f.close()
                updated_obj = obj + accounts

                with open("accounts.json", "w") as f:
                    json.dump(updated_obj, f)
                    f.close()
                accounts = []
        except:
            pass


if __name__ == "__main__":
    get_data(10000)
