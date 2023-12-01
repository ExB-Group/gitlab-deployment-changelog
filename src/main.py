import sys

from loguru import logger

from utils.gitlab_connector import GitlabConnector, Deployment
from utils.slack import send_to_slack

BUG_LABEL = "type::bug"
ICON_MR = ":gear:"
ICON_BUGFIX = ":negative_squared_cross_mark:"
ICON_FEATURE = ":star2:"


def _get_emoji_from_issue(changelog_entry) -> str:
    if not changelog_entry.issue_iid:
        # MR
        return ICON_MR
    if BUG_LABEL in changelog_entry.issue_labels:
        return ICON_BUGFIX
    return ICON_FEATURE


def slack_msg_from_deployment(dpl: Deployment) -> None:
    msg = (f":tada: New Deployment to *{dpl.environment}*, deployed at {dpl.deployed_at} by {dpl.deployed_by}.\n"
           f"It includes:\n")

    for changelog_entry in d.changelog:
        emoji = _get_emoji_from_issue(changelog_entry)
        msg += f"{emoji}<{changelog_entry.url}|*{changelog_entry.get_title()}*> by {changelog_entry.author}\n"
    msg += f"Legend: {ICON_MR} Merge request w/o issues; {ICON_BUGFIX} bugfix; "
    msg += f"{ICON_FEATURE} new feature or improvement"

    logger.debug(msg)
    send_to_slack(msg)


if __name__ == '__main__':
    gc = GitlabConnector.factory()
    env = sys.argv[1:2] if len(sys.argv) > 2 else "production/the_exb"
    deployments = gc.get_changelog(env, deployments_count=2)
    for d in deployments:
        slack_msg_from_deployment(d)
