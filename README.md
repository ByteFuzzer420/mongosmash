![mongosmash](https://img.shields.io/github/license/kathuluman/mongosmash?color=blue&style=for-the-badge) ![Version](https://img.shields.io/github/v/tag/kathuluman/mongosmash?color=blue&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/version-3.0.0-green?style=for-the-badge)

## Overview

MongoSmash is a Python tool designed to scan a list of IP addresses, attempt to authenticate with MongoDB instances, and recursively download their databases if access is granted without authentication.

## Features

- **IP Address Scanning**: Efficiently scans a list of provided IP addresses.
- **MongoDB Authentication Attempts**: Tries to authenticate with each IP address.
- **Recursive Database Download**: Downloads databases recursively upon successful authentication.
- **Logging**: Detailed logging with Rich for better readability.
- **Multithreading**: Uses multiple threads to speed up the scanning process.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/kathuluman/mongosmash.git
    cd mongosmash
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare the IP List**:
    Create a text file containing the list of IP addresses, one per line.

2. **Run the Tool**:
    ```bash
    python3 mongosmash.py
    ```
    You will be prompted to enter the path to the file containing IP addresses and the number of threads to use.

## Example

```bash
$ python mongosmash.py
Enter the path to the file containing IP addresses: ips.txt
Enter the number of threads to use: 10
```

## Configuration

- **Logging**: Logs are displayed in the console using Rich.
- **Directories**: Data is stored in the `.mongosmash/collections` directory.
