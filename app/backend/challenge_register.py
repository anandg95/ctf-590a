import os
import json
import random
import subprocess

all_challenges = []

flag_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
flag_prefix = "SDAT"

def flag_gen(n=20):
    # creates a random flag of n chars long
    return flag_prefix + "{" + "".join(random.choices(flag_characters, k=n)) + "}"

challenge_dir = os.path.join(os.getcwd(), "challenges")
challenge_folders = os.listdir(challenge_dir)
details_file = "details.json"
flag_file = "flag.txt"
sh_file = "run.sh"
static_folder = "static"


## Loop through challenges and create flag.txt if not exists locally or within db_flags
def create_flags(db_flags: dict):
    print("Creating flags ...")
    for folder in challenge_folders:
        flag_path = os.path.join(challenge_dir, folder, flag_file)
        if not os.path.exists(flag_path):
            with open(flag_path, "w") as f:
                f.write(db_flags.get(folder, flag_gen()))
        



## Start all challenge services (flag will be persisted on main memory of the service)
def start_challenge_services():
    print("Starting up challenge services ...")
    for folder in challenge_folders:
        sh_path = os.path.join(challenge_dir, folder, sh_file)
        if os.path.exists(sh_path):
            sh_path = sh_path.replace(" ", "\ ")
            subprocess.Popen(sh_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)



## Loop through challenges and remove flag.txt if not needed further
def fetch_details():
    print("Fetching challenge details ...")
    all_details = []
    statics = {}
    for folder in challenge_folders:
        details_path = os.path.join(challenge_dir, folder, details_file)
        flag_path = os.path.join(challenge_dir, folder, flag_file)
        static_path = os.path.join(challenge_dir, folder, static_folder)

        with open(details_path) as f:
            details = json.loads(f.read())
        details.update(id=int(folder))
        with open(flag_path) as f:
            details.update(flag=f.read())
        
        try:
            statics[int(folder)] = {i: os.path.join(static_path, i) for i in os.listdir(static_path)}
        except FileNotFoundError:
            pass
        
        persist_flag = details.get("persist_flag", False) or os.path.exists(os.path.join(challenge_dir, folder, sh_file))
        if not persist_flag:
            os.remove(flag_path)

        all_details.append(details)
    all_details.sort(key=lambda x:x["id"])
    return all_details, statics





    

    
    
    
