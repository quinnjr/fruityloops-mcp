# GitHub Pages Setup Guide

This guide explains how to configure GitHub Pages for the FL Studio MCP Server documentation.

## Quick Setup

The `gh-pages` branch has been created and pushed. Now configure GitHub Pages:

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings**
3. Scroll down to **Pages** (in the left sidebar under "Code and automation")
4. Under **Source**, select:
   - **Branch:** `gh-pages`
   - **Folder:** `/ (root)`
5. Click **Save**

### 2. Wait for Deployment

GitHub will automatically deploy the site. This takes 1-5 minutes.

You'll see a message: "Your site is published at https://quinnjr.github.io/fruityloops-mcp/"

### 3. Verify Deployment

Visit: **https://quinnjr.github.io/fruityloops-mcp/**

You should see the documentation site built with MkDocs Material.

## Automatic Deployment

The documentation is automatically deployed via GitHub Actions workflow `.github/workflows/docs.yml`.

**Documentation will be live at:**
🌐 **https://quinnjr.github.io/fruityloops-mcp/**

