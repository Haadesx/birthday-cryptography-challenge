# Birthday Cryptography Challenge - Vercel Deployment

This document provides information about deploying the Birthday Cryptography Challenge to Vercel.

## Deployment Steps

1. Push your code to GitHub
2. Log in to [Vercel](https://vercel.com)
3. Create a new project and import your GitHub repository
4. Use the following settings:
   - Build Command: Leave empty (it's specified in vercel.json)
   - Output Directory: Leave empty
   - Install Command: Leave empty
   - Framework Preset: Other

## Important Files for Vercel Deployment

- `vercel.json`: Configuration for Vercel deployment
- `wsgi.py`: The entry point for the Vercel deployment
- `runtime.txt`: Specifies Python 3.9
- `requirements.txt`: Lists all required Python packages
- `build_requirements.txt`: Basic requirements for the build process

## Troubleshooting

- If you encounter any issues with package installation, check the Vercel build logs
- The uploads directory is set to use `/tmp` in Vercel environment
- Note that files stored in `/tmp` will be lost when the function cold-starts

## Local Development

For local development, run:

```bash
python app.py
```

This will start the Flask development server. 