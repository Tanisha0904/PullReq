import os
import argparse
import subprocess
import requests
from pprint import pprint
from secrets_1 import GITHUB_TOKEN



def create_repo(repo_name, username):
    try:
        repo_path = "D:\Temp_Repos"  #path to the directory where you want to create your repository in local computer  
        #below are some shell commands run in python using the os system functions to execute specific commands and os change directory 
        os.chdir(repo_path)    
        os.system('mkdir '+repo_name)
        os.chdir(repo_path+"\\"+repo_name)
        
        # Initialize Git repository
        os.system("git init")
        
        # Create README.md and text.txt files
        os.system("echo '# "+repo_name+"' >> README.md")    
        os.system("echo '# ahdasds"+repo_name+"' >> text.txt")   
        
        # Add files to staging area
        os.system("git add .")   
        
        # Commit files
        os.system('git commit -m "Initial Commit"')   
        
        # Set the branch to main (or master depending on your Git configuration)
        os.system("git branch -M main")   
        
        # Add remote origin and push
        os.system("git remote add origin https://github.com/"+username+"/"+repo_name+".git")
        os.system("git push -u origin main")
        print("Repository created successfully with the example text file.")

    except FileExistsError  as err:
        raise SystemExit(err)
    except subprocess.CalledProcessError as err:
        raise SystemExit("Error occurred while executing Git commands:", err)
    except Exception as err:
        raise SystemExit("An unexpected error occurred:", err)


def push_changes():
    try:
        # os.system("echo '   Hello' >> text.txt")
        os.system("git add .")   
            
            # Commit files
        os.system('git commit -m "files updated manually"')   
            
            # Set the branch to main (or master depending on your Git configuration)
        # os.system("git branch -M main")   
        os.system(" git pull --rebase origin main")   
            
            # Add remote origin and push
        os.system("git push -u origin main")
        print("changes pushed to github")

    except Exception as err:
        raise SystemExit("An unexpected error occurred:", err)




def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--name", "--n", type=str, dest="name", required=True)
    parser.add_argument("--private", "-p", dest="is_private", action="store_true")
    args=parser.parse_args()
    # print(args)

    username="Tanisha0904"
    repo_name=args.name
    is_private=args.is_private

    API_URL="https://api.github.com"

    # if is_private:
    #     payload='{"name": "'+repo_name+'", "private":true}'
        
    # else:
    #     payload='{"name": "'+repo_name+'", "private":false}'
        
    payload = '{"name": "' + repo_name + '"}' #repo created will be public by default

    # print(payload)
    # payload='{"name":"{repo_name}"}'


    headers={
        "Authorization":"token "+ GITHUB_TOKEN,
        "Accept": "application/vnd.github+json"
    }
    try:
        r=requests.post(API_URL+"/user/repos", data=payload, headers=headers)
        r.raise_for_status()

    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    # push_changes()
    create_repo(repo_name, username)

if __name__ == '__main__':
    main()
