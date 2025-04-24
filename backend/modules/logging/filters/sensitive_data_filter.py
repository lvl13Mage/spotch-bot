import logging
import re

class SensitiveDataFilter(logging.Filter):
    """
    Filter class to redact sensitive data like OAuth codes, access tokens, and user credentials from logs.
    """

    # Define patterns to redact (add more if needed)
    PATTERNS = {
        "oauth": r"(code|access_token|refresh_token)=[\w-]+",
        "authorization": r"(Authorization: Bearer )[\w-]+",
        "api_keys": r"(client_secret|api_key|password)=[\w-]+"
    }

    def _redact(self, text: str) -> str:
        """Applies all redaction patterns to the given text."""
        for key, pattern in self.PATTERNS.items():
            text = re.sub(pattern, rf"{key.upper()}=REDACTED", text)
        return text

    def filter(self, record):
        """
        Redact sensitive data in both the log message and arguments.
        """
        # Redact the main message
        #record.msg = self._redact(record.getMessage())

        # redact the argument touple on third position
        record.args = tuple(self._redact(arg) if i == 2 else arg for i, arg in enumerate(record.args))

        # Return True to continue the filter chain
        
        return True
