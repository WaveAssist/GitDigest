import waveassist

# Initialize WaveAssist SDK (no check_credits flag in the starting node)
waveassist.init()

# Credits estimate for GitDigest
CREDITS_NEEDED_FOR_RUN = 0.3
# Estimated processing time per repository (in seconds)
# Accounts for: API calls, diff fetching, LLM analysis, report generation
PROCESSING_TIME_PER_REPO = 180  # ~3 minutes per repo

def fetch_credits_and_time_needed_for_run():
    """Calculate credits and estimated time needed for the run."""
    github_selected_resources = waveassist.fetch_data("github_selected_resources", default=[])
    if not isinstance(github_selected_resources, list):
        github_selected_resources = []
    number_of_repos = len(github_selected_resources)
    time_to_process = number_of_repos * PROCESSING_TIME_PER_REPO
    return CREDITS_NEEDED_FOR_RUN, time_to_process

print("GitDigest: Starting credits check and initialization...")

# Calculate credits and time needed
credits_needed_for_run, time_to_process = fetch_credits_and_time_needed_for_run()

# Check credits and notify if insufficient
success = waveassist.check_credits_and_notify(
    required_credits=CREDITS_NEEDED_FOR_RUN,
    assistant_name="GitDigest",
)

if not success:
    display_output = {
        "html_content": "<p>Credits were not available, the GitDigest run was skipped.</p>",
    }
    waveassist.store_data("display_output", display_output, run_based=True, data_type="json")
    raise Exception("Credits were not available, the GitDigest run was skipped.")
else:
    waveassist.store_data(
        "tentative_time_to_process", str(time_to_process), run_based=True, data_type="string"
    )

# Validate required inputs
project_name = waveassist.fetch_data("project_name", default="")
if not project_name or not str(project_name).strip():
    display_output = {
        "html_content": "<p>Project name is required but was not provided.</p>",
    }
    waveassist.store_data("display_output", display_output, run_based=True, data_type="json")
    raise Exception("Project name is required but was not provided.")

# Validate GitHub integration
github_access_token = waveassist.fetch_data("github_access_token", default="")
github_selected_resources = waveassist.fetch_data("github_selected_resources", default=[])

if not github_access_token:
    display_output = {
        "html_content": "<p>GitHub access token is required. Please connect your GitHub account.</p>",
    }
    waveassist.store_data("display_output", display_output, run_based=True, data_type="json")
    raise Exception("GitHub access token is required.")

if not isinstance(github_selected_resources, list) or len(github_selected_resources) == 0:
    display_output = {
        "html_content": "<p>No GitHub repositories selected. Please select at least one repository to track.</p>",
    }
    waveassist.store_data("display_output", display_output, run_based=True, data_type="json")
    raise Exception("No GitHub repositories selected.")

print(f"GitDigest: Initialized for project '{str(project_name).strip()}'")
print(f"GitDigest: Tracking {len(github_selected_resources)} repositories")
print("GitDigest: Credits check complete and initialization finished.")

