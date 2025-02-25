from github import Github
import openai
import os

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")
repo_owner = os.getenv("REPO_OWNER")
repo_name = os.getenv("REPO_NAME")
pr_number = int(os.getenv("PR_NUMBER"))

# Initialize GitHub API client
g = Github(github_token)
repo = g.get_user(repo_owner).get_repo(repo_name)
pr = repo.get_pull(pr_number)

# Retrieve diff
diff = pr.diff_url
diff_content = pr.get_files()

# Construct AI prompt for review
prompt = f"""
You are an expert code reviewer. Analyze the following Pull Request diff:
- Focus on: code performance, security vulnerabilities, and adherence to best practices.
- Provide feedback in a step-by-step manner (Chain-of-Thought reasoning).
- Suggest improvements clearly and concisely.

PR Diff Content:
{diff_content}

Respond with feedback suitable to post as a GitHub comment.
"""

# Generate feedback from OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "system", "content": "You are a senior code reviewer."},
              {"role": "user", "content": prompt}],
    temperature=0.2,
    max_tokens=500
)

feedback = response.choices[0].message["content"]

# Post feedback as a comment on the PR
pr.create_issue_comment(f"🤖 **AI Code Review Feedback:**\n\n{feedback}")
print("✅ Feedback posted successfully.")
