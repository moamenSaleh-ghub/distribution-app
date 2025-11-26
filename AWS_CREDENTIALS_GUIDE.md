# Where to Add AWS Credentials

## Option 1: AWS CLI Configure (Easiest & Recommended) ✅

This is the **recommended method**. Run this command:

```bash
aws configure
```

This will:
1. Create `~/.aws/credentials` file (if it doesn't exist)
2. Create `~/.aws/config` file (if it doesn't exist)
3. Prompt you to enter:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region name: `eu-central-1`
   - Default output format: `json`

**Location of files:**
- Credentials: `~/.aws/credentials`
- Config: `~/.aws/config`

**Example of what it looks like:**

`~/.aws/credentials`:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

`~/.aws/config`:
```
[default]
region = eu-central-1
output = json
```

## Option 2: Manual File Creation

If you prefer to create the files manually:

1. **Create the AWS directory:**
```bash
mkdir -p ~/.aws
```

2. **Create credentials file:**
```bash
nano ~/.aws/credentials
```

Add:
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

3. **Create config file:**
```bash
nano ~/.aws/config
```

Add:
```
[default]
region = eu-central-1
output = json
```

4. **Set proper permissions:**
```bash
chmod 600 ~/.aws/credentials
chmod 600 ~/.aws/config
```

## Option 3: Environment Variables (Temporary)

For a single session, you can set environment variables:

```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_DEFAULT_REGION="eu-central-1"
```

**Note:** These only last for the current terminal session.

## Option 4: Add to Shell Profile (Persistent Environment Variables)

Add to `~/.zshrc` (since you're using zsh):

```bash
nano ~/.zshrc
```

Add at the end:
```bash
export AWS_ACCESS_KEY_ID="your-access-key-id"
export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
export AWS_DEFAULT_REGION="eu-central-1"
```

Then reload:
```bash
source ~/.zshrc
```

## Security Best Practices

1. **Never commit credentials to git** - They're already in `.gitignore`
2. **Use IAM users with minimal permissions** - Don't use root account credentials
3. **Rotate credentials regularly**
4. **Use AWS SSO for organizations** - More secure than access keys

## How to Get AWS Credentials

1. **Log into AWS Console**: https://console.aws.amazon.com
2. **Go to IAM** → Users → Your User → Security Credentials
3. **Create Access Key** → Download or copy the credentials
4. **Important**: Save the secret key immediately - you can't view it again!

## Verify Your Setup

After configuring, test with:
```bash
aws sts get-caller-identity
```

This should return your AWS account ID and user ARN.

## Recommended: Use `aws configure`

Just run:
```bash
aws configure
```

And follow the prompts. It's the easiest and most secure way!

