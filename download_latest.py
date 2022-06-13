
import requests
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('-v', '--version',
                    help='Version to download. Defaults to latest version.',
                    default="latest",
                    )
parser.add_argument('-b', '--build',
                    help='Build to download. Defaults to latest version.',
                    default="latest",
                    )


args = parser.parse_args()

def getLatestVersion():
    url = "https://api.papermc.io/v2/projects/paper"
    response = requests.get(url=url)
    return response.json()['versions'][-1]

def getLatestBuild(version):
    url = "https://api.papermc.io/v2/projects/paper/versions/"+ str(version) +"/builds"
    response = requests.get(url=url)
    return response.json()["builds"][-1]["build"]

def getLatestDownloadLink(version, build):
    url = "https://api.papermc.io/v2/projects/paper/versions/"+ str(version) +"/builds/"+ str(build)
    response = requests.get(url=url)
    return response.json()["downloads"]["application"]["name"]

def getDownload(version, build, link):
    url = "https://api.papermc.io/v2/projects/paper/versions/"+ str(version) +"/builds/"+ str(build) + "/downloads/" + link
    response = requests.get(url=url)
    return response.content

if __name__ == "__main__":
    # Get version
    if args.version == "latest":
        version = getLatestVersion()
    else:
        version = args.version
    print("Latest Version: " + str(version))

    # Get build
    if args.build == "latest":
        build = getLatestBuild(version)
    else:
        build = args.build
    print("Latest Build: " + str(build))
        
    # Get download link
    downloadLink = getLatestDownloadLink(version, build)
    print("Download File: " + str(downloadLink))

    # Preform Download
    download = getDownload(version, build, downloadLink)
    with open(str(downloadLink), "wb") as f:
        f.write(download)
