# API Error Troubleshooting

HTTP 401 indicates invalid authentication.

HTTP 403 indicates insufficient permissions.

HTTP 429 indicates rate limiting.

Clients should implement exponential backoff for retries.