# How to Get Your `credentials.json`

It looks like you are trying to manually fill in the JSON file. It is much easier to **download the full file** from Google.

## Steps to Download

1.  **Go to the Google Cloud Console**:
    [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)

2.  **Find your OAuth Client**:
    -   Look under the **"OAuth 2.0 Client IDs"** section.
    -   You should see the client you created (e.g., "Gmail Tracker Backend").

3.  **Click the Download Button**:
    -   On the far right of that row, there is a **Download icon** (an arrow pointing down).
    -   Click it to download the JSON file.

4.  **Use that File**:
    -   Rename the downloaded file to `credentials.json`.
    -   Replace the file in your `backend/` folder with this new file.

## If you MUST copy manually:
-   **Client ID**: Shown on the Credentials page.
-   **Client Secret**: Click the "Edit" (pencil) icon on your OAuth Client to reveal the secret.
-   **Redirect URIs**: Ensure you added `http://localhost` and `http://localhost:8000/auth/callback` in the "Authorized redirect URIs" section.
