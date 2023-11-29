from utils.gitlab_connector import GitlabConnector
import sys

if __name__ == '__main__':
    gc = GitlabConnector.factory()
    env = sys.argv[1:2] if len(sys.argv) > 2 else "production/the_exb"
    gc.get_changelog(env)
