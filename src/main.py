import sys

from utils.gitlab_connector import GitlabConnector

if __name__ == '__main__':
    gc = GitlabConnector.factory()
    env = sys.argv[1:2] if len(sys.argv) > 2 else "production/the_exb"
    dpls = gc.get_changelog(env, deployments_count=2)
    for d in dpls:
        print(f"{d.deployed_at} by {d.deployed_by}")
        for ch in d.changelog:
            print(f"  {ch.title} by {ch.author} ({ch.url})")
