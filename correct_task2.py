def count_valid_emails(emails):
    """
    Count valid email addresses in a list.
    
    Args:
        emails: List of email strings to validate
        
    Returns:
        int: Number of valid email addresses
        
    Notes:
        Validates basic email format: local@domain with at least one dot in domain.
        Skips non-strings, empty strings, and malformed emails gracefully.
    """
    if not emails:
        return 0
    
    count = 0
    
    for email in emails:
        # Skip non-strings
        if not isinstance(email, str):
            continue
        
        # Trim whitespace
        email = email.strip()
        
        # Skip empty strings
        if not email:
            continue
        
        # Must contain exactly one @ symbol
        if email.count('@') != 1:
            continue
        
        # Split and validate structure
        local_part, domain_part = email.split('@')
        
        # Both parts must be non-empty
        if not local_part or not domain_part:
            continue
        
        # Domain must contain at least one dot
        if '.' not in domain_part:
            continue
        
        # Domain shouldn't start or end with dot
        if domain_part.startswith('.') or domain_part.endswith('.'):
            continue
        
        # Domain's last part (TLD) should be at least 2 chars
        domain_parts = domain_part.split('.')
        if len(domain_parts[-1]) < 2:
            continue
        
        count += 1
    
    return count