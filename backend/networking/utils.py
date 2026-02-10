"""
Networking utility functions for semantic attendee matching.
"""

import numpy as np
from typing import List, Tuple, Dict


def get_semantic_model():
    """
    Load and return the sentence transformers model.
    
    Returns:
        SentenceTransformer: Loaded model
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            "Sentence transformers not installed. "
            "Run: pip install sentence-transformers"
        )
    
    return SentenceTransformer('all-MiniLM-L6-v2')


def create_semantic_profile(interests: List[str], expertise: List[str], department: str = "") -> str:
    """
    Create a semantic profile string for matching.
    
    Args:
        interests: List of user interests
        expertise: List of user expertise areas
        department: Optional department name
    
    Returns:
        str: Formatted semantic profile
    """
    interests_str = ", ".join(interests) if interests else "General"
    expertise_str = ", ".join(expertise) if expertise else "General"
    dept_str = f" | Department: {department}" if department else ""
    
    return f"Interests: {interests_str} | Expertise: {expertise_str}{dept_str}"


def calculate_similarity_matches(
    user_profile: str,
    candidate_profiles: List[Tuple[int, str]],
    top_n: int = 5
) -> List[Dict]:
    """
    Calculate semantic similarity and find top matches.
    
    Args:
        user_profile: User's semantic profile string
        candidate_profiles: List of (id, profile_string) tuples
        top_n: Number of top matches to return
    
    Returns:
        List[Dict]: Sorted list of matches with scores
    """
    if not candidate_profiles:
        return []
    
    try:
        from sklearn.metrics.pairwise import cosine_similarity
    except ImportError:
        raise ImportError(
            "Scikit-learn not installed. "
            "Run: pip install scikit-learn"
        )
    
    model = get_semantic_model()
    
    # Get embeddings
    all_profiles = [user_profile] + [profile for _, profile in candidate_profiles]
    embeddings = model.encode(all_profiles)
    
    # Calculate similarity with user profile (first embedding)
    user_embedding = embeddings[0].reshape(1, -1)
    candidate_embeddings = embeddings[1:]
    
    similarities = cosine_similarity(user_embedding, candidate_embeddings).flatten()
    
    # Get top matches
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    
    matches = []
    for rank, idx in enumerate(top_indices, 1):
        user_id, _ = candidate_profiles[idx]
        matches.append({
            'rank': rank,
            'user_id': user_id,
            'match_score': float(similarities[idx])
        })
    
    return matches


def find_common_interests(
    interests1: List[str],
    interests2: List[str]
) -> List[str]:
    """
    Find common interests between two users.
    
    Args:
        interests1: List of first user's interests
        interests2: List of second user's interests
    
    Returns:
        List[str]: Common interests
    """
    set1 = set(interests1) if interests1 else set()
    set2 = set(interests2) if interests2 else set()
    return list(set1 & set2)


def generate_match_reason(
    interests1: List[str],
    interests2: List[str],
    expertise1: List[str],
    expertise2: List[str],
    department1: str = "",
    department2: str = ""
) -> str:
    """
    Generate a reason for the match.
    
    Args:
        interests1: First user's interests
        interests2: Second user's interests
        expertise1: First user's expertise
        expertise2: Second user's expertise
        department1: First user's department
        department2: Second user's department
    
    Returns:
        str: Reason for the match
    """
    common_interests = find_common_interests(interests1, interests2)
    common_expertise = find_common_interests(expertise1, expertise2)
    same_department = department1 == department2 and department1
    
    if same_department:
        return f"Same department ({department1})"
    elif common_interests:
        return f"Common interests in {', '.join(common_interests[:2])}"
    elif common_expertise:
        return f"Aligned expertise in {', '.join(common_expertise[:2])}"
    else:
        return "Complementary backgrounds"


def batch_calculate_matches(
    user_profiles: List[Dict],
    top_n_per_user: int = 3,
    include_reason: bool = True
) -> Dict[int, List[Dict]]:
    """
    Calculate matches for multiple users at once.
    
    Args:
        user_profiles: List of dicts with 'id', 'interests', 'expertise', 'department'
        top_n_per_user: Number of top matches per user
        include_reason: Whether to include match reason
    
    Returns:
        Dict[int, List[Dict]]: Matches keyed by user ID
    """
    matches_dict = {}
    
    for i, user in enumerate(user_profiles):
        user_id = user['id']
        
        # Create semantic profile for this user
        user_profile_str = create_semantic_profile(
            user.get('interests', []),
            user.get('expertise', []),
            user.get('department', '')
        )
        
        # Create candidate profiles (all others)
        candidates = []
        for j, candidate in enumerate(user_profiles):
            if i != j:  # Skip self
                candidate_profile_str = create_semantic_profile(
                    candidate.get('interests', []),
                    candidate.get('expertise', []),
                    candidate.get('department', '')
                )
                candidates.append((candidate['id'], candidate_profile_str, candidate))
        
        # Find matches
        if candidates:
            candidate_tuples = [(cand_id, cand_profile) for cand_id, cand_profile, _ in candidates]
            matches = calculate_similarity_matches(user_profile_str, candidate_tuples, top_n_per_user)
            
            # Add reason if requested
            if include_reason:
                candidate_map = {cand[0]: cand[2] for cand in candidates}
                for match in matches:
                    candidate = candidate_map[match['user_id']]
                    match['reason'] = generate_match_reason(
                        user.get('interests', []),
                        candidate.get('interests', []),
                        user.get('expertise', []),
                        candidate.get('expertise', []),
                        user.get('department', ''),
                        candidate.get('department', '')
                    )
            
            matches_dict[user_id] = matches
        else:
            matches_dict[user_id] = []
    
    return matches_dict
