# B12 Application Submission Guide

## Step-by-Step Setup Instructions

### Step 1: Verify the Project Structure
Ensure your repository has the following structure:
```
your-repo/
├── .github/
│   └── workflows/
│       └── b12-submit.yml
├── b12test.py
└── README.md
```

### Step 2: Push Files to GitHub
If you haven't already, add and commit these files to your repository:

```bash
# Navigate to your repository
cd /home/binaya/B12

# Initialize git (if not already initialized)
git init

# Add the workflow file and Python script
git add .github/workflows/b12-submit.yml
git add b12test.py
git add README.md

# Commit the changes
git commit -m "Add B12 application submission workflow"

# Push to main branch
git push origin main
```

### Step 3: Configure Your Information
Edit the workflow file (`.github/workflows/b12-submit.yml`) and update the default values:

In the `workflow_dispatch` section, modify these lines with your actual information:
```yaml
B12_NAME: ${{ github.event.inputs.name || 'Your Name' }}  # Replace 'Your Name'
B12_EMAIL: ${{ github.event.inputs.email || 'you@example.com' }}  # Replace with your email
B12_RESUME_LINK: ${{ github.event.inputs.resume_link || 'https://your-resume-link.com' }}  # Replace with your resume
```

### Step 4: Trigger the Workflow - Option A: Manual Trigger
1. Go to your GitHub repository
2. Click the **Actions** tab
3. Select **B12 Application Submission** from the left sidebar
4. Click **Run workflow** button
5. Fill in the input fields:
   - **Your name**: Your full name
   - **Your email**: Your email address
   - **Link to your resume**: URL to your resume (PDF, HTML, or LinkedIn profile)
6. Click **Run workflow**

### Step 5: Trigger the Workflow - Option B: Automatic on Push
Simply push to the `main` branch:
```bash
git push origin main
```
The workflow will automatically run with the default values you configured.

### Step 6: Monitor the Submission
1. Go to the **Actions** tab in your GitHub repository
2. Find the latest **B12 Application Submission** run
3. Click on it to view the logs
4. Wait for the job to complete (usually takes 30-60 seconds)

### Step 7: Retrieve Your Receipt
Once the workflow completes:
1. Click on the **Submit B12 Application** step to expand it
2. Look for the line starting with `Receipt:`
3. Copy the receipt string (format: `your-submission-receipt`)
4. Paste this receipt in the B12 application form to confirm your submission

## Workflow Triggers

### Manual Trigger (Recommended for First Submission)
- Go to Actions → B12 Application Submission → Run workflow
- Fill in your details each time
- Useful for submitting multiple times or testing

### Automatic on Push (Optional)
- Triggers whenever you push to the `main` branch
- Uses the default values configured in the workflow
- Good for CI/CD integration

## Understanding the Workflow

The workflow file does the following:

1. **Checks out your repository** - Downloads the latest code
2. **Sets up Python 3.11** - Prepares the Python environment
3. **Submits the application** - Runs the `b12test.py` script with:
   - Your name, email, and resume link
   - Repository URL (automatic)
   - Action run URL (automatic) - Used for verification
4. **Uploads logs** - Saves submission logs as artifacts (optional)

## Environment Variables Used

The workflow passes these variables to the Python script:
- `B12_NAME` - Your name
- `B12_EMAIL` - Your email address
- `B12_RESUME_LINK` - URL to your resume
- `B12_REPOSITORY_LINK` - Auto-populated: `github.com/your-username/your-repo`
- `B12_ACTION_RUN_LINK` - Auto-populated: Link to the specific workflow run

## Troubleshooting

### Workflow not appearing in Actions tab?
- Push the `.github/workflows/b12-submit.yml` file to your repository
- Wait a few seconds for GitHub to recognize it
- Refresh the page

### Submission failed with error?
- Check the step output for detailed error messages
- Verify all required fields are filled
- Ensure your resume link is publicly accessible

### Receipt not printing?
- Check the "Submit B12 Application" step output
- Look for lines starting with "Receipt:" or "✓"
- If not found, the submission may have failed (check error messages)

## Python Script Details

The `b12test.py` script:
- Accepts environment variables or command-line arguments
- Generates ISO 8601 timestamps automatically
- Computes HMAC-SHA256 signatures for security
- Sends properly formatted JSON to B12 servers
- Prints the receipt on successful submission

You can also run it manually:
```bash
python b12test.py "Your Name" "you@example.com" "https://resume-link" "https://repo-link" "https://action-run-link"
```

Or using environment variables:
```bash
export B12_NAME="Your Name"
export B12_EMAIL="you@example.com"
export B12_RESUME_LINK="https://resume-link"
export B12_REPOSITORY_LINK="https://repo-link"
export B12_ACTION_RUN_LINK="https://action-run-link"
python b12test.py
```
