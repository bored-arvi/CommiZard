"""Error handler for Ollama API responses with user-friendly messages."""


def get_error_message(status_code: int) -> str:
    """
    Return user-friendly error message for Ollama HTTP status codes.

    Ollama follows standard REST API conventions with these common responses:
    - 200/201: Success / Can be ignored
    - 400: Bad Request (malformed request)
    - 403: Forbidden (access denied, check OLLAMA_ORIGINS)
    - 404: Not Found (model doesn't exist)
    - 500: Internal Server Error (model crashed or out of memory)
    - 503: Service Unavailable (Ollama not running)

    Args:
        status_code: HTTP status code from Ollama API

    Returns:
        User-friendly error message with troubleshooting suggestions
    """
    error_messages = {
        400: (
            "Bad Request - The request was malformed or contains invalid parameters.\n"
            "Suggestions:\n"
            "  • Check if your prompt is properly formatted\n"
            "  • Verify all required parameters are provided\n"
            "  • Ensure the model name is correct"
        ),
        403: (
            "Forbidden - Access to Ollama was denied.\n"
            "Suggestions:\n"
            "  • Check OLLAMA_ORIGINS environment variable\n"
            "  • Verify Ollama accepts requests from your application\n"
            "  • Ensure proper permissions to access the service"
        ),
        404: (
            "Model Not Found - The requested model doesn't exist.\n"
            "Suggestions:\n"
            "  • Install the model: ollama pull <model-name>\n"
            "  • Check available models with the 'list' command\n"
            "  • Verify the model name spelling"
        ),
        500: (
            "Internal Server Error - Ollama encountered an unexpected error.\n"
            "Suggestions:\n"
            "  • The model may have run out of memory (RAM/VRAM)\n"
            "  • Try restarting Ollama: ollama serve\n"
            "  • Check Ollama logs for detailed error information\n"
            "  • Consider using a smaller model if resources are limited"
        ),
        503: (
            "Service Unavailable - Ollama service is not responding.\n"
            "Suggestions:\n"
            "  • Start Ollama: ollama serve\n"
            "  • Check if Ollama is running: ps aux | grep ollama\n"
            "  • Verify the service is listening on port 11434\n"
            "  • Wait a moment if the service is starting up"
        ),
    }

    if status_code in error_messages:
        return f"Error {status_code}: {error_messages[status_code]}"

    # Generic fallback for unknown status codes
    return (
        f"Error {status_code}: Request failed.\n"
        "Check the Ollama documentation or server logs for more details."
    )
